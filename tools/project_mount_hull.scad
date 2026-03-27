// OpenSCAD script to project the convex hull of a mount footprint.
// Usage: openscad -D "filename=\"...\"" -o output.svg tools/project_mount_hull.scad

filename = "dummy.stl"; // Overridden by command line

// Some mounts have recessed undersides where adhesive pads are likely applied
// separately. Use the projected convex hull as a simpler install proxy.
hull()
    projection(cut = true)
        translate([0, 0, -0.1])
            import(filename);
