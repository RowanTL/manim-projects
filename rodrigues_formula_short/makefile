# Manim Makefile
# Change this variable to your Python file name
PYTHON_FILE = main.py

# This is the hardcoded list of scenes you want to render
# WARNING: The order of this list does matter!
SCENE_LIST = FormulaScene RotationScene DoTheMathScene

# The .PHONY declaration tells Make that these are not file names, but commands
.PHONY: render slides clean

# Default rule: runs the render command
all: render

# Rule to render Manim scenes using the `manim` command
render:
	manim $(PYTHON_FILE) $(SCENE_LIST)

# Rule to create a Manim slide show using the `manim-slides` command
slides:
	manim-slides $(SCENE_LIST)

# Rule to clean up all generated media files
# The --yes flag automatically confirms the deletion
clean:
	manim $(PYTHON_FILE) $(SCENE_LIST) --clean --yes
