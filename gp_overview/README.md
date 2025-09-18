# Overview

This is a presentation for a talk about Genetic Programming I am giving.

The presentation takes place on September 18th, 2025 6PM CST @ Tech Artista Central West End in Saint Louis, MO.

## How to build

1) Follow the official instructions for !(Manim Community Edition)[https://docs.manim.community/en/stable/installation/uv.html]
2) `uv venv`
3) `source .venv/bin/activate` or the appropriate command for your shell.
4) `uv pip install manim-slides[manim]`
5) `make render`
6) `make slides`

At this point, a Qt looking window should appear with the presentation.
Use the arrow keys to move from slide to slide.

### Notes

I've had `step 3` freeze at the end while generating the reverse
animations. If this happens, `ctrl+c` then re-run the command.

I'm using manim version 0.19.0.

### Quirks

I decided to program PushAlternation to be semi-random. There is no way to know
what exactly that slide will do. :)
