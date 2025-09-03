# Overview

This is a presentation for a talk about Genetic Programming I am giving.

The presentation takes place on September 18th, 2025 6PM CST @ Tech Artista Central West End in Saint Louis, MO.

## How to build

A venv would be beneficial here. These instructions do not create one.

1) Follow the official instructions for !(Manim Community Edition)[https://docs.manim.community/en/stable/installation/uv.html]
2) `uv pip install -U manim-slides[manim]`
3) `make render`
4) `make slides`

At this point, a Qt looking window should appear with the presentation.
Use the arrow keys to move from slide to slide.

Note: I've had `step 3` freeze at the end while generating the reverse
animations. If this happens, `ctrl+c` then re-run the command.
