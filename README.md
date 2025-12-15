# Photos Processor

A Python tool to organize and analyze photos based on EXIF metadata.

## Features

- Copy photos to an organized folder with date-based renaming using EXIF DateTimeOriginal
- Analyze photo orientation statistics (portrait vs landscape)

## Installation

Install dependencies using uv:

```sh
uv sync
```

## Usage

### Copy Photos

Copy photos to an ordered folder and rename them based on their EXIF DateTimeOriginal:

```sh
uv run src/main.py copy
```

### Photo Statistics

Show orientation statistics for photos in the ordered folder:

```sh
uv run src/main.py stats
```

## Requirements

- Python >= 3.9
- Pillow >= 11.3.0
