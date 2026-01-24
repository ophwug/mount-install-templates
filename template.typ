#let template(
  mount-name: "Mount",
  svg-file: "dummy.svg",
  clearance-offset: 60mm,
) = {
  set page(paper: "us-letter", margin: 1cm)
  set text(font: "New Computer Modern Sans", size: 12pt)

  // Helper to format length in mm
  let to-mm-str(len) = {
    let mm-val = calc.round(len.mm())
    str(mm-val) + "mm"
  }

  align(center)[
    #v(1cm)

    #context {
      // Load image to get dimensions
      let img = image(svg-file)
      let size = measure(img)

      // Layout Constants
      // 100% width might be constrained by margin, which is fine.
      let block-width = 100%
      // Ensure height accommodates everything.
      let total-height = size.height + clearance-offset + 3cm

      block(width: block-width, height: total-height, stroke: none)[

        // -------------------------------------------------------------
        // 1. Mount (Bottom Center)
        // -------------------------------------------------------------
        #place(bottom + center, img)

        // -------------------------------------------------------------
        // 2. Dimension Line (Mount Top to Clearance Start)
        // -------------------------------------------------------------
        #let dim-x = 0pt
        #let mount-top-y = -size.height
        #let clear-y = -size.height - clearance-offset

        #place(bottom + center)[
          // Line
          #place(line(start: (0pt, mount-top-y), end: (0pt, clear-y), stroke: 1pt + black))

          // Arrowheads
          #place(dx: 0pt, dy: mount-top-y, polygon(fill: black, (0pt, 0pt), (-2pt, -4pt), (2pt, -4pt)))
          #place(dx: 0pt, dy: clear-y, polygon(fill: black, (0pt, 0pt), (-2pt, 4pt), (2pt, 4pt)))

          // Label
          #place(dx: 5mm, dy: (mount-top-y + clear-y) / 2)[
            #text(size: 10pt)[#to-mm-str(clearance-offset)]
          ]
        ]

        // -------------------------------------------------------------
        // 3. Keep Clear Zone Arcs (Contour Lines)
        // -------------------------------------------------------------
        // "Frown" Orientation (Concave Down).
        // Center is BELOW the tangent point.
        // Visually, circle top touches the line. Sides curve down.
        // Center Y position: Tangent Y + Radius (since (+) is DOWN).
        // Tangent Y is `clear-y`.

        #let radii = (300mm, 400mm, 500mm, 600mm)

        #for r in radii {
          // Circle Center
          place(bottom + center, dy: clear-y + r)[
            #circle(radius: r, stroke: (thickness: 1pt, dash: "dashed", paint: red))
          ]

          // Labels for radii?
          // Maybe add small text near the top apex
          // place(bottom + center, dy: clear-y + 2mm)[#text(size:6pt, fill:gray)[R#to-mm-str(r)]]
        }

        // Add "Keep Clear Zone" Text (At the clearance line)
        #place(bottom + center, dy: clear-y - 2mm)[
          #text(fill: red, size: 10pt, weight: "bold")[Keep Clear Zone]
        ]

        // Add Horizontal Reference Line (Solid)
        #place(bottom + center, dy: clear-y)[
          #line(length: 15cm, stroke: (thickness: 2pt, paint: red, dash: "solid"))
        ]
      ]
    }

    #v(1fr)

    Please verify scale using a standard credit card.
    #v(0.5cm)
    #box(width: 85.60mm, height: 53.98mm, radius: 3.18mm, stroke: 1pt + black)[
      #align(center + horizon)[Credit Card Scale (86mm x 54mm)]
    ]
    #v(1cm)
    #text(size: 18pt, weight: "bold")[#mount-name Install Template]
  ]
}
