#!/usr/bin/env python3
"""
Script to copy photos to an 'ordered' folder and rename them based on DateTimeOriginal
"""

import sys
from photo_stats import count_photo_orientations
from photos_copy import copy_photos


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "copy":
        copy_photos()
    elif command == "stats":
        count_photo_orientations()
    else:
        print(f"⚠️  Unknown command: {command}")
        print_usage()
        sys.exit(1)


def print_usage():
    """
    Print usage information for the script
    """
    print("Usage:")
    print(
        "  python main.py copy   - Copy photos to ordered folder with date-based renaming"
    )
    print(
        "  python main.py stats  - Show orientation statistics for photos in ordered folder"
    )


if __name__ == "__main__":
    main()
