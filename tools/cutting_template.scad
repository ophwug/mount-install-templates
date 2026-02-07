// OpenSCAD script to generate adhesive cutting templates with internal supports
// Usage: openscad -D "filename=\"...\"" -D "mount_name=\"...\"" -D "bridge_type=\"horizontal\"" -o output.stl tools/cutting_template.scad

filename = "dummy.stl"; // Oriented STL filename
mount_name = "mount"; // Name for the label
bridge_type = "radial"; // "none", "radial", or "horizontal"
bridge_gap = 0; // Gap in the middle of the bridge
is_solid = false; // If true, generate a solid silhouette without internal holes

thickness = 2; // Thickness of the template
margin = 5; // Margin around the footprint
depth = 1; // Depth of the text debossing
bridge_width = 1.2; // Width of support bridges

// Projection of the footprint (raw, with holes)
module footprint_raw() {
  projection(cut=false)
    intersection() {
      translate([0, 0, -0.1])
        import(filename);
      // Capture the bottom 3mm of the geometry to get a robust footprint
      // even if the bottom surface is slightly curved.
      // 3mm is chosen to ensure we capture the base but avoid the main stalk.
      translate([0, 0, 1.5])
        cube([300, 300, 3], center=true);
    }
}

// Module for support bridges
module bridges() {
  if (bridge_type == "radial") {
    difference() {
      for (i = [0:45:359]) {
        rotate([0, 0, i])
          translate([-100, -bridge_width / 2, 0])
            square([200, bridge_width]);
      }
      if (bridge_gap > 0) {
        circle(d=bridge_gap, $fn=50);
      }
    }
  } else if (bridge_type == "horizontal") {
    // Split horizontal bar
    difference() {
      translate([-100, -bridge_width / 2, 0])
        square([200, bridge_width]);
      if (bridge_gap > 0) {
        square([bridge_gap, bridge_width + 1], center=true);
      }
    }
  }
}

// Main template
union() {
  difference() {
    // Base plate (solid frame around the footprint)
    minkowski() {
      linear_extrude(height=thickness)
        offset(r=margin)
          hull() footprint_raw();
      // Slightly rounded edges for better handling
      cylinder(r=1, h=0.01, $fn=20);
    }

    // Cutout for the adhesive footprint
    translate([0, 0, -1]) {
      if (is_solid) {
        linear_extrude(height=thickness + 2)
          hull() footprint_raw();
      } else {
        linear_extrude(height=thickness + 2)
          footprint_raw();
      }
    }

    // Text label (debossed)
    // Positioned below the hull
    translate([0, -35, thickness - depth])
      linear_extrude(height=depth + 0.1)
        text(mount_name, size=5, halign="center", valign="center", font="DejaVu Sans Mono:style=Bold");
  }

  // Add bridges back in, but only within the footprint area
  // This connects internal islands to the main frame
  if (!is_solid && bridge_type != "none") {
    intersection() {
      linear_extrude(height=thickness)
        bridges();

      linear_extrude(height=thickness)
        hull() footprint_raw();
    }
  }
}
