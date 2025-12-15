#!/usr/bin/env python3
"""
Script to copy photos to an 'ordered' folder and rename them based on DateTimeOriginal
"""

import os
import sys
import shutil
from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
from datetime import datetime
from photo_stats import count_photo_orientations


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


def copy_photos(input_file="input", ordered_dir="ordered"):
    """
    Copy photos to an ordered folder and rename them based on DateTimeOriginal

    Args:
        input_file: Path to the input file containing folder paths (one per line)
        ordered_dir: Directory where organized photos will be copied
    """
    if not os.path.exists(input_file):
        print(f"⚠️  Input file '{input_file}' not found!")
        print("Please create an 'input' file with one folder path per line.")
        sys.exit(1)

    # Read folder paths from input file
    with open(input_file, "r") as f:
        folders = [line.strip() for line in f if line.strip()]

    if not folders:
        print(f"⚠️  No folder paths found in '{input_file}'")
        sys.exit(1)

    # Create ordered directory
    os.makedirs(ordered_dir, exist_ok=True)

    print("Photo Organizer - Copy by DateTimeOriginal")
    print("=" * 80)
    print(f"\nReading folder paths from '{input_file}'")
    print(f"Output directory: {ordered_dir}\n")

    process_folders(folders, ordered_dir)


def process_folders(folder_paths, ordered_dir):
    """
    Process all photos in the given folders and copy them to ordered directory
    """
    # Common image extensions
    image_extensions = {
        ".jpg",
        ".jpeg",
        ".JPG",
        ".JPEG",
        ".png",
        ".PNG",
        ".heic",
        ".HEIC",
    }

    total_copied = 0
    total_skipped = 0
    filename_counter = {}  # Track duplicate filenames

    for folder_path in folder_paths:
        print(f"\n{'=' * 80}")
        print(f"Processing folder: {folder_path}")
        print(f"{'=' * 80}\n")

        # Check if folder exists
        if not os.path.exists(folder_path):
            print(f"⚠️  Folder not found: {folder_path}\n")
            continue

        # Walk through the folder and subfolders
        photo_count = 0
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # Check if file has an image extension
                if Path(file).suffix in image_extensions:
                    photo_count += 1
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, folder_path)

                    # Get DateTime
                    datetime_info = get_photo_datetime(file_path)

                    if datetime_info and datetime_info.get("DateTimeOriginal"):
                        datetime_original = datetime_info["DateTimeOriginal"]
                        formatted_date = convert_to_utc_format(datetime_original)

                        if formatted_date:
                            # Create filename with .jpeg extension
                            base_filename = formatted_date

                            # Handle duplicate filenames
                            if base_filename in filename_counter:
                                filename_counter[base_filename] += 1
                                new_filename = f"{base_filename}_{filename_counter[base_filename]}.jpeg"
                            else:
                                filename_counter[base_filename] = 0
                                new_filename = f"{base_filename}.jpeg"

                            # Copy file to ordered directory
                            dest_path = os.path.join(ordered_dir, new_filename)
                            shutil.copy2(file_path, dest_path)

                            print(f"✓ {relative_path}")
                            print(f"  -> {new_filename}\n")
                            total_copied += 1
                        else:
                            print(f"⚠️  {relative_path}")
                            print(
                                f"  Could not parse DateTimeOriginal: {datetime_original}\n"
                            )
                            total_skipped += 1
                    else:
                        print(f"⚠️  {relative_path}")
                        print("  DateTimeOriginal not found in EXIF data\n")
                        total_skipped += 1

        if photo_count == 0:
            print("No photos found in this folder.\n")
        else:
            print(f"Photos processed: {photo_count}\n")

    print(f"\n{'=' * 80}")
    print("Summary:")
    print(f"  Total copied: {total_copied}")
    print(f"  Total skipped: {total_skipped}")
    print(f"{'=' * 80}\n")


def get_photo_datetime(image_path):
    """
    Extract all DateTime fields from a photo's EXIF data
    Returns a dictionary with DateTime, DateTimeOriginal, and DateTimeDigitized
    """
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()

        datetime_info = {
            # "DateTime": None,
            "DateTimeOriginal": None,
            # "DateTimeDigitized": None,
        }

        if exif_data:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                # Look for DateTime-related tags
                if tag in datetime_info:
                    datetime_info[tag] = value

        return datetime_info
    except Exception as e:
        return {"Error": str(e)}


def convert_to_utc_format(exif_datetime):
    """
    Convert EXIF datetime string to UTC format: yyyy-mm-dd-hh-mm-ss
    EXIF format is typically: "2024:03:15 14:30:22"
    """
    try:
        # Parse EXIF datetime format
        dt = datetime.strptime(exif_datetime, "%Y:%m:%d %H:%M:%S")
        # Format to UTC format
        return dt.strftime("%Y-%m-%d-%H-%M-%S")
    except Exception as e:
        return None


if __name__ == "__main__":
    main()
