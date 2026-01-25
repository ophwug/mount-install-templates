#import "@preview/cades:0.3.1": qr-code

#let template(
  mount-name: "Mount",
  svg-file: "dummy.svg",
  clearance-offset: 60mm,
  repo-url: none,
  commit-hash: none,
  commit-date: none,
  paper-size: "us-letter",
  min-radius: 300mm,
  top-padding: 4cm,
) = {
  set page(paper: paper-size, margin: 1cm, flipped: true)
  set text(font: "DejaVu Sans Mono", size: 12pt)

  // Helper to format length in mm
  let to-mm-str(len) = {
    let mm-val = calc.round(len.mm())
    str(mm-val) + "mm"
  }

  align(center)[

    #context {
      // Load image to get dimensions
      let img = image(svg-file)
      let size = measure(img)

      // Layout Constants
      // 100% width might be constrained by margin, which is fine.
      let block-width = 100%
      // Ensure height accommodates everything.
      // We add some space at the top (8cm) to show the arcs "radiating upwards"
      let total-height = size.height + clearance-offset + top-padding

      block(width: block-width, height: total-height, stroke: none, clip: true)[

        // -------------------------------------------------------------
        // Coordinates (All relative to TOP center)
        // -------------------------------------------------------------
        #let line-y = top-padding
        #let mount-top-y = line-y + clearance-offset

        // -------------------------------------------------------------
        // 1. Mount (Centered below line)
        // -------------------------------------------------------------
        #place(top + center, dy: mount-top-y, img)
        #place(top + center, dy: mount-top-y)[
          #box(width: size.width, height: size.height)[
            #align(center + horizon)[
              #text(weight: "bold", size: 14pt)[comma \ mount]
            ]
          ]
        ]

        // -------------------------------------------------------------
        // 2. Dimension Line (Mount Top to Clearance Start)
        // -------------------------------------------------------------
        #place(top + center)[
          // Line
          #place(line(start: (0pt, mount-top-y), end: (0pt, line-y), stroke: 1pt + black))

          // Arrowheads
          #place(dx: 0pt, dy: mount-top-y, polygon(fill: black, (0pt, 0pt), (-2pt, -4pt), (2pt, -4pt)))
          #place(dx: 0pt, dy: line-y, polygon(fill: black, (0pt, 0pt), (-2pt, 4pt), (2pt, 4pt)))

          // Label
          #place(dx: 5mm, dy: (mount-top-y + line-y) / 2)[
            #text(size: 10pt)[#to-mm-str(clearance-offset)]
          ]
        ]

        // -------------------------------------------------------------
        // 3. Keep Clear Zone Arcs (Contour Lines)
        // -------------------------------------------------------------
        // "Smile" Orientation (Concave UP).
        // Center is ABOVE the tangent point.
        // Visually, circle bottom touches the line. Sides curve UP.
        // Center Y position: Tangent Y - Radius.
        // Tangent Y is `line-y`.
        // Top of circle (size 2r) is at Tangent Y - 2*Radius.

        #let all-radii = (300mm, 400mm, 500mm, 600mm, 700mm, 800mm, 900mm, 1000mm)
        #let radii = all-radii.filter(r => r >= min-radius)

        #for r in radii [
          // Circle Placement
          // top of circle = Center - r = (line-y - r) - r = line-y - 2r
          #place(top + center, dy: line-y - 2 * r)[
            #circle(radius: r, stroke: (thickness: 1pt, dash: "dashed", paint: red))
          ]
        ]

        // Add "Vehicle's Original Camera Housing" Text (At the clearance line)
        #place(top + center, dy: line-y - 20mm)[
          #text(fill: red, size: 10pt, weight: "bold")[Vehicle's Original Camera Housing]
        ]

        // Add Horizontal Reference Line (Solid)
        #place(top + center, dy: line-y)[
          #line(length: 15cm, stroke: (thickness: 2pt, paint: red, dash: "solid"))
        ]
      ]
    }

    #place(bottom + center)[
      #grid(
        columns: (1fr, 1fr, 1fr),
        gutter: 1cm,
        align: horizon,
        // Column 1: Print Instructions & Credit Card Scale
        stack(dir: ttb, spacing: 0.3cm)[
          #set align(center)
          #text(size: 9pt)[
            *Print at 100%.* Do not scale to fit. \
            Place credit card here to verify scale.
          ]
          #box(width: 85.60mm, height: 53.98mm, radius: 3.18mm, stroke: 1pt + black)[
            #align(center + horizon)[
              Credit Card Scale (86mm x 54mm) \
              #v(0.1cm)
              #text(size: 8pt, fill: gray)[You won't be charged]
            ]
          ]
        ],
        // Column 2: Title and Git Info
        stack(dir: ttb, spacing: 0.2cm)[
          #set align(center)
          #text(size: 18pt, weight: "bold")[#mount-name\ Install Template]
          #v(0.1cm)
          #if (
            (repo-url != none and repo-url != "")
              or (commit-hash != none and commit-hash != "")
              or (commit-date != none and commit-date != "")
          ) [
            #text(size: 8pt)[
              #if repo-url != none and repo-url != "" [
                #link(repo-url)[#repo-url.replace("https://", "")] \
              ]
              #if commit-hash != none and commit-hash != "" [Commit: #commit-hash | ]
              #if commit-date != none and commit-date != "" [Date: #commit-date]
            ]
            #if repo-url != none and repo-url != "" {
              v(0.2cm)
              qr-code(repo-url, width: 2cm)
            }
          ]
        ],
        // Column 3: "Why" and "Tape" Instructions
        stack(dir: ttb, spacing: 0.3cm)[
          #set align(center)
          #text(weight: "bold")[Tape template to the OUTSIDE of your windshield!]

          #text(size: 9pt)[
            This is a template to help people mount comma devices in the most standardized way for maximum performance.
          ]
        ],
      )
    ]
  ]
}
