# Overview

This is a short I'd like to upload speaking over the basics of Rodrigues' formula

Not sure when this is gonna be uploaded.

It is possible to make short form content with manim.

## How to build

1) Follow the official instructions for !(Manim Community Edition)[https://docs.manim.community/en/stable/installation/uv.html]
2) `uv venv`
3) `source .venv/bin/activate` or the appropriate command for your shell.
4) `uv pip install manim manim-slides[manim] PyQt6`
5) `make render` (does this by default with just `make`)
6) `make slides`
7) (Optional) `make clean` to get rid of any files when done

### Notes

I'm using manim version 0.19.0.

## Outline of the video

- Start by showing the equation
  - Show it in action first and then move onto the derivation
  - Stick with the book's version
  - Show what [n_\times] looks like
- Show an example of the equation in action with a simple 3D matrix
  - Illustrate rotation somehow
    - Draw a circle with theta following it perhaps
  - Maybe rotate `PI / 2` or `3PI / 2` if crazy
- Then show math book derivation for those who are interested
