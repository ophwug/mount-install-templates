#let template(
  mount-name: "Mount",
  svg-file: "dummy.svg",
  clearance-offset: 60mm,
) = {
  set page(paper: "us-letter", margin: 1cm)
  set text(font: "Helvetica", size: 12pt)

  align(center)[
    #text(size: 18pt, weight: "bold")[#mount-name Install Template]
    #v(1cm)

    #context {
      // Load image to get dimensions
      let img = image(svg-file)
      let size = measure(img)

      // Container box
      // We want to visualize the clearance offset ABOVE the mount.
      // We create a container that holds the clearance space + the mount.

      // Calculate total width/height for the visual block
      // We make it wide enough for the lines (e.g., 20cm or mount width + margin)
      let block-width = calc.max(size.width, 15cm) // Minimum width for lines
      let total-height = size.height + clearance-offset + 2cm // Extra space for text/arcs

      block(width: block-width, height: total-height, stroke: none)[

        // 1. Draw the Mount at the bottom center
        #place(bottom + center, img)

        // 2. Draw Clearance Line
        // It should be `clearance-offset` above the top of the mount.
        // Top of mount is at `total-height - size.height`.
        // So line is at `total-height - size.height - clearance-offset`.
        // Let's use relative positioning from bottom.

        #place(bottom + center, dy: -size.height - clearance-offset)[
          #line(length: block-width, stroke: (thickness: 2pt, paint: red, dash: "dashed"))
          #v(-5mm)
          #text(fill: red, size: 10pt)[Keep Clear Zone (#clearance-offset)]
        ]
      ]
    }

    #v(1fr) // Push credit card to bottom

    Please verify scale using a standard credit card.
    #v(0.5cm)
    // Credit Card
    #box(width: 85.60mm, height: 53.98mm, radius: 3.18mm, stroke: 1pt + black)[
      #align(center + horizon)[Credit Card Scale (86mm x 54mm)]
    ]
    #v(1cm) // Space at the bottom
  ]
}
