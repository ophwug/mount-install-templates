# Makefile for Install Templates

# Tools
OPENSCAD := openscad
TYPST := typst
MKDIR := mkdir -p

# Directories
BUILD_DIR := build

# Mount Files
C3_MOUNTS := hardware/comma_three/mount/c3_mount.stl
C3X_MOUNTS := hardware/comma_3X/mount/c3x_mount.stl
C4_MOUNTS := hardware/comma_four/mount/four_mount.stl
C4_MOUNT_STEM := c4_mount

# All Mounts
ALL_MOUNTS := $(C3_MOUNTS) $(C3X_MOUNTS) $(C4_MOUNTS)

# Output Lists
PDFS := $(patsubst %.stl,$(BUILD_DIR)/%_letter.pdf,$(notdir $(ALL_MOUNTS)))
PNGS := $(patsubst %.stl,$(BUILD_DIR)/%_letter.png,$(notdir $(ALL_MOUNTS)))
PDFS_A4 := $(patsubst %.stl,$(BUILD_DIR)/%_a4.pdf,$(notdir $(ALL_MOUNTS)))
PNGS_A4 := $(patsubst %.stl,$(BUILD_DIR)/%_a4.png,$(notdir $(ALL_MOUNTS)))
PNGS_BW := $(patsubst %.stl,$(BUILD_DIR)/%_letter_bw.png,$(notdir $(ALL_MOUNTS)))
PNGS_A4_BW := $(patsubst %.stl,$(BUILD_DIR)/%_a4_bw.png,$(notdir $(ALL_MOUNTS)))
CUTTING_TEMPLATES := $(BUILD_DIR)/c3_cutting_template.stl $(BUILD_DIR)/c3x_cutting_template.stl $(BUILD_DIR)/c4_cutting_template.stl \
                     $(BUILD_DIR)/c3x_cutting_template_solid.stl $(BUILD_DIR)/c4_cutting_template_solid.stl
CUTTING_PREVIEWS := $(BUILD_DIR)/c3_cutting_template_preview.png $(BUILD_DIR)/c3x_cutting_template_preview.png $(BUILD_DIR)/c4_cutting_template_preview.png

# Manual overrides for comma four naming
PDFS := $(subst four_mount,c4_mount,$(PDFS))
PNGS := $(subst four_mount,c4_mount,$(PNGS))
PDFS_A4 := $(subst four_mount,c4_mount,$(PDFS_A4))
PNGS_A4 := $(subst four_mount,c4_mount,$(PNGS_A4))
PNGS_BW := $(subst four_mount,c4_mount,$(PNGS_BW))
PNGS_A4_BW := $(subst four_mount,c4_mount,$(PNGS_A4_BW))


# Keep intermediate SVGs, TYP files, and oriented STLs
.SECONDARY: $(PDFS:.pdf=.svg) $(PDFS:.pdf=.typ) $(PDFS_A4:.pdf=.typ) $(BUILD_DIR)/c3_mount.stl $(BUILD_DIR)/c3x_mount.stl $(BUILD_DIR)/c4_mount.stl $(BUILD_DIR)/c3_mount.svg $(BUILD_DIR)/c3x_mount.svg $(BUILD_DIR)/c4_mount.svg

.PHONY: all clean update-hardware debug

all: $(PDFS) $(PNGS) $(PDFS_A4) $(PNGS_A4) $(PNGS_BW) $(PNGS_A4_BW) vehicles cutting-templates cutting-previews
	@echo "All templates built successfully."

cutting-templates: $(CUTTING_TEMPLATES)
	@echo "All cutting templates built successfully."

cutting-previews: $(CUTTING_PREVIEWS)
	@echo "All cutting template previews built successfully."

verify: all
	@echo "Verifying templates with Gemini..."
	uv run tools/verify_build.py

debug:
	@echo "PDFS (Letter Landscape): $(PDFS)"
	@echo "PDFS (A4 Landscape): $(PDFS_A4)"

update-hardware:
	git submodule update --init --recursive


clean:
	rm -rf $(BUILD_DIR)

$(BUILD_DIR):
	$(MKDIR) $(BUILD_DIR)


# Rule to generate SVG from STL
# We use a pattern rule but since source files are in different dirs, we need VPATH or specific rules.
# Simpler: Generate specific rules or use VPATH.

VPATH = hardware/comma_three/mount:hardware/comma_3X/mount:hardware/comma_four/mount

# Extra Flags for orient_stl.py
ORIENT_FLAGS = 
$(BUILD_DIR)/c4_mount.stl: hardware/comma_four/mount/four_mount.stl | $(BUILD_DIR)
	@echo "Orienting comma four mount..."
	uv run ./tools/orient_stl.py --flip "$<" "$@"

$(BUILD_DIR)/c4_mount.svg: $(BUILD_DIR)/c4_mount.stl
	@echo "Generating SVG for comma four mount..."
	$(OPENSCAD) -D "filename=\"$(shell pwd)/$<\"" -o $@ tools/project_mount.scad

$(BUILD_DIR)/c3_mount.stl: hardware/comma_three/mount/c3_mount.stl | $(BUILD_DIR)
	@echo "Orienting comma three mount..."
	uv run ./tools/orient_stl.py "$<" "$@"

$(BUILD_DIR)/c3x_mount.stl: hardware/comma_3X/mount/c3x_mount.stl | $(BUILD_DIR)
	@echo "Orienting comma 3x mount..."
	uv run ./tools/orient_stl.py "$<" "$@"

$(BUILD_DIR)/%.svg: $(BUILD_DIR)/%.stl
	@echo "Generating SVG for $*..."
	$(OPENSCAD) -D "filename=\"$(shell pwd)/$<\"" -o $@ tools/project_mount.scad

# Default layout parameters
OFFSET=60mm
MIN_RADIUS=500mm
TOP_PADDING=2cm

# Comma Three (35mm)
$(BUILD_DIR)/c3_mount_letter.typ $(BUILD_DIR)/c3_mount_letter_landscape.typ $(BUILD_DIR)/c3_mount_a4.typ $(BUILD_DIR)/c3_mount_a4_landscape.typ: OFFSET=35mm
$(BUILD_DIR)/c3_mount_letter.typ $(BUILD_DIR)/c3_mount_letter_landscape.typ $(BUILD_DIR)/c3_mount_a4.typ $(BUILD_DIR)/c3_mount_a4_landscape.typ: NAME="comma three"

# Comma Three X (35mm)
$(BUILD_DIR)/c3x_mount_letter.typ $(BUILD_DIR)/c3x_mount_letter_landscape.typ $(BUILD_DIR)/c3x_mount_a4.typ $(BUILD_DIR)/c3x_mount_a4_landscape.typ: OFFSET=35mm
$(BUILD_DIR)/c3x_mount_letter.typ $(BUILD_DIR)/c3x_mount_letter_landscape.typ $(BUILD_DIR)/c3x_mount_a4.typ $(BUILD_DIR)/c3x_mount_a4_landscape.typ: NAME="comma 3x"

# Comma Four (80mm)
$(BUILD_DIR)/c4_mount_letter.typ $(BUILD_DIR)/c4_mount_letter_landscape.typ $(BUILD_DIR)/c4_mount_a4.typ $(BUILD_DIR)/c4_mount_a4_landscape.typ: OFFSET=44mm
$(BUILD_DIR)/c4_mount_letter.typ $(BUILD_DIR)/c4_mount_letter_landscape.typ $(BUILD_DIR)/c4_mount_a4.typ $(BUILD_DIR)/c4_mount_a4_landscape.typ: NAME="comma four"

# Cutting templates
$(BUILD_DIR)/c3_cutting_template.stl: NAME=comma three
$(BUILD_DIR)/c3_cutting_template.stl: BRIDGE_TYPE=none
$(BUILD_DIR)/c3_cutting_template.stl: BRIDGE_GAP=0
$(BUILD_DIR)/c3_cutting_template.stl: ORIENTED_STL=$(BUILD_DIR)/c3_mount.stl
$(BUILD_DIR)/c3x_cutting_template.stl: NAME=comma 3x
$(BUILD_DIR)/c3x_cutting_template.stl: BRIDGE_TYPE=horizontal
$(BUILD_DIR)/c3x_cutting_template.stl: BRIDGE_GAP=41.2
$(BUILD_DIR)/c3x_cutting_template.stl: ORIENTED_STL=$(BUILD_DIR)/c3x_mount.stl
$(BUILD_DIR)/c4_cutting_template.stl: NAME=comma four
$(BUILD_DIR)/c4_cutting_template.stl: BRIDGE_TYPE=horizontal
$(BUILD_DIR)/c4_cutting_template.stl: BRIDGE_GAP=35.0
$(BUILD_DIR)/c4_cutting_template.stl: ORIENTED_STL=$(BUILD_DIR)/c4_mount.stl

$(BUILD_DIR)/%_cutting_template.stl: IS_SOLID=false
$(BUILD_DIR)/%_cutting_template.stl: tools/cutting_template.scad | $(BUILD_DIR)
	@echo "Generating cutting template for $(NAME) with bridge_type=$(BRIDGE_TYPE), gap=$(BRIDGE_GAP), is_solid=$(IS_SOLID)..."
	$(OPENSCAD) -D 'filename="$(shell pwd)/$(ORIENTED_STL)"' -D 'mount_name="$(NAME)"' -D 'bridge_type="$(BRIDGE_TYPE)"' -D 'bridge_gap=$(BRIDGE_GAP)' -D 'is_solid=$(IS_SOLID)' -o $@ tools/cutting_template.scad

# Solid Variants
$(BUILD_DIR)/%_cutting_template_solid.stl: IS_SOLID=true
$(BUILD_DIR)/%_cutting_template_solid.stl: BRIDGE_TYPE=none
$(BUILD_DIR)/%_cutting_template_solid.stl: BRIDGE_GAP=0

$(BUILD_DIR)/c3x_cutting_template_solid.stl: NAME=comma 3x (solid)
$(BUILD_DIR)/c3x_cutting_template_solid.stl: ORIENTED_STL=$(BUILD_DIR)/c3x_mount.stl
$(BUILD_DIR)/c4_cutting_template_solid.stl: NAME=comma four (solid)
$(BUILD_DIR)/c4_cutting_template_solid.stl: ORIENTED_STL=$(BUILD_DIR)/c4_mount.stl

$(BUILD_DIR)/%_cutting_template_solid.stl: tools/cutting_template.scad | $(BUILD_DIR)
	@echo "Generating solid cutting template for $(NAME)..."
	$(OPENSCAD) -D 'filename="$(shell pwd)/$(ORIENTED_STL)"' -D 'mount_name="$(NAME)"' -D 'bridge_type="$(BRIDGE_TYPE)"' -D 'bridge_gap=$(BRIDGE_GAP)' -D 'is_solid=$(IS_SOLID)' -o $@ tools/cutting_template.scad

$(BUILD_DIR)/c3_cutting_template_preview.png: NAME=comma three
$(BUILD_DIR)/c3_cutting_template_preview.png: BRIDGE_TYPE=none
$(BUILD_DIR)/c3_cutting_template_preview.png: BRIDGE_GAP=0
$(BUILD_DIR)/c3_cutting_template_preview.png: ORIENTED_STL=$(BUILD_DIR)/c3_mount.stl
$(BUILD_DIR)/c3x_cutting_template_preview.png: NAME=comma 3x
$(BUILD_DIR)/c3x_cutting_template_preview.png: BRIDGE_TYPE=horizontal
$(BUILD_DIR)/c3x_cutting_template_preview.png: BRIDGE_GAP=41.2
$(BUILD_DIR)/c3x_cutting_template_preview.png: ORIENTED_STL=$(BUILD_DIR)/c3x_mount.stl
$(BUILD_DIR)/c4_cutting_template_preview.png: NAME=comma four
$(BUILD_DIR)/c4_cutting_template_preview.png: BRIDGE_TYPE=horizontal
$(BUILD_DIR)/c4_cutting_template_preview.png: BRIDGE_GAP=35.0
$(BUILD_DIR)/c4_cutting_template_preview.png: ORIENTED_STL=$(BUILD_DIR)/c4_mount.stl

# Cutting template previews dependencies
$(BUILD_DIR)/c3_cutting_template_preview.png: $(BUILD_DIR)/c3_mount.stl
$(BUILD_DIR)/c3x_cutting_template_preview.png: $(BUILD_DIR)/c3x_mount.stl
$(BUILD_DIR)/c4_cutting_template_preview.png: $(BUILD_DIR)/c4_mount.stl

# Cutting template previews
$(BUILD_DIR)/%_cutting_template_preview.png: tools/cutting_template.scad | $(BUILD_DIR)
	@echo "Generating preview for $(NAME)..."
	$(OPENSCAD) --imgsize=1024,1024 --render --autocenter --viewall -D 'filename="$(shell pwd)/$(ORIENTED_STL)"' -D 'mount_name="$(NAME)"' -D 'bridge_type="$(BRIDGE_TYPE)"' -D 'bridge_gap=$(BRIDGE_GAP)' -D 'is_solid=false' -o $@ tools/cutting_template.scad

# Git Info
GIT_COMMIT := $(shell git rev-parse --short HEAD)
GIT_REV := $(shell git rev-list --count HEAD)
GIT_DATE := $(shell git log -1 --format=%cd --date=short)
# Convert git@github.com:org/repo.git to https://github.com/org/repo
GIT_URL := $(shell git config --get remote.origin.url | sed -e 's/git@github.com:/https:\/\/github.com\//' -e 's/\.git$$//')

# Generate Typst source
$(BUILD_DIR)/%_letter.typ: $(BUILD_DIR)/%.svg template.typ
	@echo "Generating Typst source for $*..."
	@echo '#import "/template.typ": template; #template(mount-name: $(NAME), svg-file: "$<", clearance-offset: $(OFFSET), repo-url: "$(GIT_URL)", commit-hash: "$(GIT_COMMIT)", commit-date: "$(GIT_DATE)", revision: "$(GIT_REV)", min-radius: $(MIN_RADIUS), top-padding: $(TOP_PADDING))' > $@

$(BUILD_DIR)/%_a4.typ: $(BUILD_DIR)/%.svg template.typ
	@echo "Generating A4 Typst source for $*..."
	@echo '#import "/template.typ": template; #template(mount-name: $(NAME), svg-file: "$<", clearance-offset: $(OFFSET), repo-url: "$(GIT_URL)", commit-hash: "$(GIT_COMMIT)", commit-date: "$(GIT_DATE)", revision: "$(GIT_REV)", paper-size: "a4", min-radius: $(MIN_RADIUS), top-padding: $(TOP_PADDING))' > $@

# General Rules for compiling Typst to PDF and PNG
$(BUILD_DIR)/%.pdf: $(BUILD_DIR)/%.typ template.typ
	@echo "Compiling PDF for $*..."
	$(TYPST) compile $< $@ --root . --font-path fonts

$(BUILD_DIR)/%.png: $(BUILD_DIR)/%.typ template.typ
	@echo "Compiling PNG for $*..."
	$(TYPST) compile $< $@ --root . --font-path fonts --ppi 144

$(BUILD_DIR)/%_bw.png: $(BUILD_DIR)/%.png
	@echo "Converting $< to greyscale..."
	uv run tools/grayscale.py $< $@



VEHICLES_DIR := vehicles
VEHICLES := $(notdir $(wildcard $(VEHICLES_DIR)/*))

# Target lists
VEHICLE_PDFS :=
VEHICLE_PNGS :=

# Helper to generate targets for a vehicle
# Args: 1=vehicle_name
define generate_vehicle_targets
VEHICLE_PDFS += $(BUILD_DIR)/vehicles/$(1)/c3_mount_letter.pdf $(BUILD_DIR)/vehicles/$(1)/c3_mount_a4.pdf
VEHICLE_PDFS += $(BUILD_DIR)/vehicles/$(1)/c3x_mount_letter.pdf $(BUILD_DIR)/vehicles/$(1)/c3x_mount_a4.pdf
VEHICLE_PDFS += $(BUILD_DIR)/vehicles/$(1)/c4_mount_letter.pdf $(BUILD_DIR)/vehicles/$(1)/c4_mount_a4.pdf

VEHICLE_PNGS += $(BUILD_DIR)/vehicles/$(1)/c3_mount_letter.png $(BUILD_DIR)/vehicles/$(1)/c3_mount_a4.png
VEHICLE_PNGS += $(BUILD_DIR)/vehicles/$(1)/c3x_mount_letter.png $(BUILD_DIR)/vehicles/$(1)/c3x_mount_a4.png
VEHICLE_PNGS += $(BUILD_DIR)/vehicles/$(1)/c4_mount_letter.png $(BUILD_DIR)/vehicles/$(1)/c4_mount_a4.png

VEHICLE_PNGS += $(BUILD_DIR)/vehicles/$(1)/c3_mount_letter_bw.png $(BUILD_DIR)/vehicles/$(1)/c3_mount_a4_bw.png
VEHICLE_PNGS += $(BUILD_DIR)/vehicles/$(1)/c3x_mount_letter_bw.png $(BUILD_DIR)/vehicles/$(1)/c3x_mount_a4_bw.png
VEHICLE_PNGS += $(BUILD_DIR)/vehicles/$(1)/c4_mount_letter_bw.png $(BUILD_DIR)/vehicles/$(1)/c4_mount_a4_bw.png

# Explicit Compilation Rules for this vehicle
$(BUILD_DIR)/vehicles/$(1)/c3_mount_letter.pdf $(BUILD_DIR)/vehicles/$(1)/c3_mount_a4.pdf: $(BUILD_DIR)/c3_mount.svg
$(BUILD_DIR)/vehicles/$(1)/c3x_mount_letter.pdf $(BUILD_DIR)/vehicles/$(1)/c3x_mount_a4.pdf: $(BUILD_DIR)/c3x_mount.svg
$(BUILD_DIR)/vehicles/$(1)/c4_mount_letter.pdf $(BUILD_DIR)/vehicles/$(1)/c4_mount_a4.pdf: $(BUILD_DIR)/c4_mount.svg

$(BUILD_DIR)/vehicles/$(1)/c3_mount_letter.png $(BUILD_DIR)/vehicles/$(1)/c3_mount_a4.png: $(BUILD_DIR)/c3_mount.svg
$(BUILD_DIR)/vehicles/$(1)/c3x_mount_letter.png $(BUILD_DIR)/vehicles/$(1)/c3x_mount_a4.png: $(BUILD_DIR)/c3x_mount.svg
$(BUILD_DIR)/vehicles/$(1)/c4_mount_letter.png $(BUILD_DIR)/vehicles/$(1)/c4_mount_a4.png: $(BUILD_DIR)/c4_mount.svg

$(BUILD_DIR)/vehicles/$(1)/%.pdf: $(BUILD_DIR)/vehicles/$(1)/%.typ
	@echo "Compiling Vehicle PDF for $$*..."
	$(MKDIR) $(dir $$@)
	$(TYPST) compile $$< $$@ --root . --font-path fonts

$(BUILD_DIR)/vehicles/$(1)/%.png: $(BUILD_DIR)/vehicles/$(1)/%.typ
	@echo "Compiling Vehicle PNG for $$*..."
	$(MKDIR) $(dir $$@)
	$(TYPST) compile $$< $$@ --root . --font-path fonts --ppi 144
endef

$(foreach v,$(VEHICLES),$(eval $(call generate_vehicle_targets,$v)))

vehicles: $(VEHICLE_PDFS) $(VEHICLE_PNGS)

# Target-specific variables for mount types
$(BUILD_DIR)/vehicles/%/c3_mount_letter.typ $(BUILD_DIR)/vehicles/%/c3_mount_a4.typ: MOUNT_NAME_PREFIX="comma three"
$(BUILD_DIR)/vehicles/%/c3_mount_letter.typ $(BUILD_DIR)/vehicles/%/c3_mount_a4.typ: OFFSET=35mm
$(BUILD_DIR)/vehicles/%/c3_mount_letter.typ $(BUILD_DIR)/vehicles/%/c3_mount_a4.typ: SVG_SOURCE=$(BUILD_DIR)/c3_mount.svg

$(BUILD_DIR)/vehicles/%/c3x_mount_letter.typ $(BUILD_DIR)/vehicles/%/c3x_mount_a4.typ: MOUNT_NAME_PREFIX="comma 3x"
$(BUILD_DIR)/vehicles/%/c3x_mount_letter.typ $(BUILD_DIR)/vehicles/%/c3x_mount_a4.typ: OFFSET=35mm
$(BUILD_DIR)/vehicles/%/c3x_mount_letter.typ $(BUILD_DIR)/vehicles/%/c3x_mount_a4.typ: SVG_SOURCE=$(BUILD_DIR)/c3x_mount.svg

$(BUILD_DIR)/vehicles/%/c4_mount_letter.typ $(BUILD_DIR)/vehicles/%/c4_mount_a4.typ: MOUNT_NAME_PREFIX="comma four"
$(BUILD_DIR)/vehicles/%/c4_mount_letter.typ $(BUILD_DIR)/vehicles/%/c4_mount_a4.typ: OFFSET=44mm
$(BUILD_DIR)/vehicles/%/c4_mount_letter.typ $(BUILD_DIR)/vehicles/%/c4_mount_a4.typ: SVG_SOURCE=$(BUILD_DIR)/c4_mount.svg


# AI/Gen Pipeline Rules
$(VEHICLES_DIR)/%/gen/offsets.svg: $(VEHICLES_DIR)/%/gen/trace.svg
	@echo "Generating offsets for $*..."
	uv run tools/vehicle_specific/generate_offsets.py $<

$(VEHICLES_DIR)/%/gen/trace.svg: $(VEHICLES_DIR)/%/gen/raw_trace.svg
	@echo "Refining trace for $*..."
	uv run tools/vehicle_specific/refine_trace.py $<

# Manual Annotation Rule
# Usage: make annotate-2020_corolla
annotate-%:
	@echo "Annotating scan for $*..."
	$(MKDIR) $(VEHICLES_DIR)/$*/ai
	uv run tools/vehicle_specific/annotate_scan.py $(VEHICLES_DIR)/$*/raw/scan.png $(VEHICLES_DIR)/$*/ai/annotated_scan.png

$(VEHICLES_DIR)/%/gen/raw_trace.svg: $(VEHICLES_DIR)/%/ai/annotated_scan.png
	@echo "Processing annotation for $*..."
	$(MKDIR) $(dir $@)
	uv run tools/vehicle_specific/process_annotation.py $< $@

# Typst Generation Rules
# Stem % matches vehicle name

# Recipe for generating Typst source
define generate_typst
	@echo "Generating Typst for $*..."
	$(MKDIR) $(dir $@)
	@echo '#import "/vehicles/$*/template.typ": template; #template(mount-name: "$(MOUNT_NAME_PREFIX) ($(shell cat vehicles/$*/name.txt))", svg-file: "$(SVG_SOURCE)", clearance-offset: $(OFFSET), custom-clearance-svg: "/vehicles/$*/gen/offsets.svg", repo-url: "$(GIT_URL)", commit-hash: "$(GIT_COMMIT)", commit-date: "$(GIT_DATE)", revision: "$(GIT_REV)", min-radius: $(MIN_RADIUS), top-padding: $(TOP_PADDING)$(PAPER_SIZE_ARG))' > $@
endef

# Letter Landscape
$(BUILD_DIR)/vehicles/%/c3_mount_letter.typ: SVG_SOURCE=$(BUILD_DIR)/c3_mount.svg
$(BUILD_DIR)/vehicles/%/c3_mount_letter.typ: MOUNT_NAME_PREFIX=comma three
$(BUILD_DIR)/vehicles/%/c3_mount_letter.typ: OFFSET=35mm

$(BUILD_DIR)/vehicles/%/c3x_mount_letter.typ: SVG_SOURCE=$(BUILD_DIR)/c3x_mount.svg
$(BUILD_DIR)/vehicles/%/c3x_mount_letter.typ: MOUNT_NAME_PREFIX=comma 3x
$(BUILD_DIR)/vehicles/%/c3x_mount_letter.typ: OFFSET=35mm

$(BUILD_DIR)/vehicles/%/c4_mount_letter.typ: SVG_SOURCE=$(BUILD_DIR)/c4_mount.svg
$(BUILD_DIR)/vehicles/%/c4_mount_letter.typ: MOUNT_NAME_PREFIX=comma four
$(BUILD_DIR)/vehicles/%/c4_mount_letter.typ: OFFSET=44mm
$(BUILD_DIR)/vehicles/%/c4_mount_letter.typ: SVG_SOURCE=$(BUILD_DIR)/c4_mount.svg


$(BUILD_DIR)/vehicles/%/c3_mount_letter.typ: $(VEHICLES_DIR)/%/gen/offsets.svg $(VEHICLES_DIR)/%/template.typ $(SVG_SOURCE)
	$(generate_typst)
$(BUILD_DIR)/vehicles/%/c3x_mount_letter.typ: $(VEHICLES_DIR)/%/gen/offsets.svg $(VEHICLES_DIR)/%/template.typ $(SVG_SOURCE)
	$(generate_typst)
$(BUILD_DIR)/vehicles/%/c4_mount_letter.typ: $(VEHICLES_DIR)/%/gen/offsets.svg $(VEHICLES_DIR)/%/template.typ $(SVG_SOURCE)
	$(generate_typst)

# A4 Landscape
$(BUILD_DIR)/vehicles/%/c3_mount_a4.typ: SVG_SOURCE=$(BUILD_DIR)/c3_mount.svg
$(BUILD_DIR)/vehicles/%/c3_mount_a4.typ: MOUNT_NAME_PREFIX=comma three
$(BUILD_DIR)/vehicles/%/c3_mount_a4.typ: OFFSET=35mm
$(BUILD_DIR)/vehicles/%/c3_mount_a4.typ: PAPER_SIZE_ARG=, paper-size: "a4"

$(BUILD_DIR)/vehicles/%/c3x_mount_a4.typ: SVG_SOURCE=$(BUILD_DIR)/c3x_mount.svg
$(BUILD_DIR)/vehicles/%/c3x_mount_a4.typ: MOUNT_NAME_PREFIX=comma 3x
$(BUILD_DIR)/vehicles/%/c3x_mount_a4.typ: OFFSET=35mm
$(BUILD_DIR)/vehicles/%/c3x_mount_a4.typ: PAPER_SIZE_ARG=, paper-size: "a4"

$(BUILD_DIR)/vehicles/%/c4_mount_a4.typ: SVG_SOURCE=$(BUILD_DIR)/c4_mount.svg
$(BUILD_DIR)/vehicles/%/c4_mount_a4.typ: MOUNT_NAME_PREFIX=comma four
$(BUILD_DIR)/vehicles/%/c4_mount_a4.typ: OFFSET=44mm
$(BUILD_DIR)/vehicles/%/four_mount_a4.typ: PAPER_SIZE_ARG=, paper-size: "a4"

$(BUILD_DIR)/vehicles/%/c3_mount_a4.typ: $(VEHICLES_DIR)/%/gen/offsets.svg $(VEHICLES_DIR)/%/template.typ $(SVG_SOURCE)
	$(generate_typst)
$(BUILD_DIR)/vehicles/%/c3x_mount_a4.typ: $(VEHICLES_DIR)/%/gen/offsets.svg $(VEHICLES_DIR)/%/template.typ $(SVG_SOURCE)
	$(generate_typst)
$(BUILD_DIR)/vehicles/%/c4_mount_a4.typ: $(VEHICLES_DIR)/%/gen/offsets.svg $(VEHICLES_DIR)/%/template.typ $(SVG_SOURCE)
	$(generate_typst)


# Vehicle Phony Targets matching README
.PHONY: $(VEHICLES)
$(VEHICLES): %:
	@echo "Building templates for $*..."
	$(MAKE) $(filter %/$*/c3_mount_letter.pdf,$(PDFS)) $(filter %/$*/c3_mount_a4.pdf,$(PDFS_A4)) \
            $(filter %/$*/c3x_mount_letter.pdf,$(PDFS)) $(filter %/$*/c3x_mount_a4.pdf,$(PDFS_A4)) \
            $(filter %/$*/c4_mount_letter.pdf,$(PDFS)) $(filter %/$*/c4_mount_a4.pdf,$(PDFS_A4))
