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

# All Mounts
ALL_MOUNTS := $(C3_MOUNTS) $(C3X_MOUNTS) $(C4_MOUNTS)

# Output Lists
# We convert path/to/file.stl -> build/file.pdf
PDFS := $(patsubst %.stl,$(BUILD_DIR)/%.pdf,$(notdir $(ALL_MOUNTS)))

# Keep intermediate SVGs
.SECONDARY: $(PDFS:.pdf=.svg)

.PHONY: all clean update-hardware debug

all: $(PDFS)

debug:
	@echo "PDFS: $(PDFS)"

update-hardware:
	git submodule update --init --recursive

clean:
	rm -rf $(BUILD_DIR)

# Rule to generate SVG from STL
# We use a pattern rule but since source files are in different dirs, we need VPATH or specific rules.
# Simpler: Generate specific rules or use VPATH.

VPATH = hardware/comma_three/mount:hardware/comma_3X/mount:hardware/comma_four/mount

# Extra Flags for orient_stl.py
ORIENT_FLAGS = 
# Flip C4 mount
$(BUILD_DIR)/four_mount.svg: ORIENT_FLAGS += --flip

$(BUILD_DIR)/%.svg: %.stl | $(BUILD_DIR)
	@echo "Orienting $<..."
	./tools/orient_stl.py $(ORIENT_FLAGS) "$<" "$(BUILD_DIR)/$(notdir $<)"
	@echo "Generating SVG for $<..."
	$(OPENSCAD) -D "filename=\"$(shell pwd)/$(BUILD_DIR)/$(notdir $<)\"" -o $@ tools/project_mount.scad

# Rules for PDFs
# We need to pass the correct offset and name based on the file.
# We can use target-specific variables.

# Comma Three (60mm)
$(BUILD_DIR)/c3_mount.pdf: OFFSET=60mm
$(BUILD_DIR)/c3_mount.pdf: NAME="Comma Three Standard"

$(BUILD_DIR)/c3_mount_8deg.pdf: OFFSET=60mm
$(BUILD_DIR)/c3_mount_8deg.pdf: NAME="Comma Three 8°"

# Comma Three X (60mm)
$(BUILD_DIR)/c3x_mount.pdf: OFFSET=60mm
$(BUILD_DIR)/c3x_mount.pdf: NAME="Comma 3X Standard"

$(BUILD_DIR)/c3x_mount_8deg.pdf: OFFSET=60mm
$(BUILD_DIR)/c3x_mount_8deg.pdf: NAME="Comma 3X 8°"

# Comma Four (80mm)
$(BUILD_DIR)/four_mount.pdf: OFFSET=80mm
$(BUILD_DIR)/four_mount.pdf: NAME="Comma Four"

# General Rule for TYPST
# We construct a temporary typst file to call the template
$(BUILD_DIR)/%.pdf: $(BUILD_DIR)/%.svg
	@echo "Generating PDF for $*..."
	@echo '#import "/template.typ": template; #template(mount-name: $(NAME), svg-file: "$<", clearance-offset: $(OFFSET))' > $(BUILD_DIR)/$*.typ
	$(TYPST) compile $(BUILD_DIR)/$*.typ $@ --root . --font-path fonts
	rm $(BUILD_DIR)/$*.typ

$(BUILD_DIR):
	$(MKDIR) $(BUILD_DIR)
