#!/usr/bin/env python3
"""
Module for analyzing photo statistics in the ordered folder
"""

import os
from pathlib import Path
from PIL import Image


def count_photo_orientations(ordered_dir="ordered"):
    """
    Count portrait and landscape photos in the ordered directory

    Args:
        ordered_dir: Directory containing organized photos

    Returns:
        dict: Dictionary with counts {'portrait': int, 'landscape': int, 'total': int}
    """
    orientation_counts = analyze_photos(ordered_dir)
    print_orientation_summary(orientation_counts)
    return orientation_counts


def analyze_photos(ordered_dir):
    """
    Analyze all photos in the ordered directory and determine their orientation

    Args:
        ordered_dir: Directory containing organized photos

    Returns:
        dict: Dictionary with counts {'portrait': int, 'landscape': int, 'total': int}
    """
    if not os.path.exists(ordered_dir):
        print(f"⚠️  Directory '{ordered_dir}' not found!")
        return {"portrait": 0, "landscape": 0, "total": 0}

    image_extensions = {".jpg", ".jpeg", ".png", ".heic"}
    counts = {"portrait": 0, "landscape": 0, "total": 0}

    for file in os.listdir(ordered_dir):
        if Path(file).suffix.lower() in image_extensions:
            file_path = os.path.join(ordered_dir, file)
            orientation = get_photo_orientation(file_path)

            if orientation:
                counts[orientation] += 1
                counts["total"] += 1

    return counts


def get_photo_orientation(image_path):
    """
    Determine if a photo is portrait or landscape based on dimensions

    Args:
        image_path: Path to the image file

    Returns:
        str: 'portrait' if height > width, 'landscape' if width >= height, None on error
    """
    try:
        with Image.open(image_path) as img:
            width, height = img.size

            if height > width:
                return "portrait"
            else:
                return "landscape"
    except Exception as e:
        print(f"⚠️  Error reading {image_path}: {e}")
        return None


def print_orientation_summary(counts):
    """
    Print a formatted summary of orientation counts

    Args:
        counts: Dictionary with portrait, landscape, and total counts
    """
    print("=" * 80)
    print("Photo Orientation Summary")
    print("=" * 80)
    print(f"\nPortrait photos:  {counts['portrait']}")
    print(f"Landscape photos: {counts['landscape']}")
    print(f"Total photos:     {counts['total']}")

    if counts["total"] > 0:
        portrait_percent = (counts["portrait"] / counts["total"]) * 100
        landscape_percent = (counts["landscape"] / counts["total"]) * 100
        print(f"\nPortrait:  {portrait_percent:.1f}%")
        print(f"Landscape: {landscape_percent:.1f}%")

    print("=" * 80)


if __name__ == "__main__":
    count_photo_orientations()
