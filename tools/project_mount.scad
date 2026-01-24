// OpenSCAD script to project mount footprint
// Usage: openscad -D "filename=\"...\"" -o output.svg tools/project_mount.scad

filename = "dummy.stl"; // Overridden by command line

// Projection cut at slightly above 0 to get the footprint
projection(cut = true)
    translate([0, 0, -0.1])
        import(filename);
