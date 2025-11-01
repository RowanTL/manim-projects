# Overview

This video shows how we modify a linear system of equations but nothing changes in reality
with respect to mathematical rules.

I had trouble grasping this when learning systems of equations a long while ago, so I hope
this helps.

**link soon**

## How to build

Install [uv](https://docs.astral.sh/uv/getting-started/installation/).
I run linux so mileage may vary for different systems.

1) `uv venv`
2) `source .venv/bin/activate`
3) `uv sync`
4) `bash build_video.sh`

The video should appear in the `media` folder.

### Notes on the build process

This video stacks two `4.5:16` videos on top of one another to create one `9:16`
video. `combine.py` combines these two videos.
