# Overview

This is a presentation I'm giving @ [Rust STL](https://www.meetup.com/stl-rust/events/311396006/) on December 4th.
It will cover the basics of actix web and a slight amount of custom stuff. I do not know that much about
actix web. I thought it would be cool to give a presentation on it.

The presentation aspect currently isn't fully ready but will be by the time of the presentation.

# How to build

## Manim Slides

Install [manim](https://docs.manim.community/en/stable/installation/uv.html) properly.

1) `uv venv`
2) Use the command it prints to activate the virtual environment. On Linux, it's `source .venv/bin/activate`
3) `uv sync`
4) `make render`
5) `make slides`

## Rust projects

1) Install [rust](https://rust-lang.org/tools/install/)
2) `cargo run --bin ##_example_file`. The examples can be found under the `src/bin` directory. Notice
  the lack of `.rs` at the end of the command above.

Either use the integrated tests in each file or create your own curl requests to query
the servers. The final `10_file_upload.rs` file has no `tests` module. I demonstrate this
with `scripts/test_upload.sh`.
