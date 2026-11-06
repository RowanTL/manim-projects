# Manim Makefile
# Change this variable to your Python file name
PYTHON_FILE = main.py

# This is the hardcoded list of scenes you want to render
# WARNING: The order of this list does matter!
SCENE_LIST = NNVisualScene FloatingPointSubset NaiveNNDefinitionScene LayerFunctionsScene

# The .PHONY declaration tells Make that these are not file names, but commands
.PHONY: render pre clean

# Low quality preview settings (portrait, matching the aspect ratio in manim.cfg)
PRE_RESOLUTION = 540,960
PRE_FPS = 15

# Default rule: runs the render command
all: render

# Rule to render Manim scenes using the `manim` command
render:
	manim $(PYTHON_FILE) $(SCENE_LIST)

# Scenes given after `pre` on the command line, e.g. `make pre NNVisualScene BasicDeclarationScene`
PRE_SCENES = $(filter-out pre,$(MAKECMDGOALS))

# Swallow the scene names so make doesn't treat them as targets
ifneq ($(filter pre,$(MAKECMDGOALS)),)
$(PRE_SCENES):
	@:
endif

# Rule to render a fast, low quality preview (overrides resolution and fps from manim.cfg)
# With no scene names given, falls back to SCENE_LIST
pre:
	manim -p -r $(PRE_RESOLUTION) --fps $(PRE_FPS) $(PYTHON_FILE) $(or $(PRE_SCENES),$(SCENE_LIST))

# Rule to clean up all generated media files
# The --yes flag automatically confirms the deletion
clean:
	manim $(PYTHON_FILE) $(SCENE_LIST) --clean --yes
