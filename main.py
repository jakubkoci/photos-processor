#!/usr/bin/env python3
"""
Script to extract DateTime information from JPEG photos in multiple folders
"""

import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
from datetime import datetime


def main():
    # Read folders from input file
    input_file = "input"

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

    print("JPEG Photo DateTime Extractor")
    print("=" * 80)
    print(f"\nReading folder paths from '{input_file}'\n")

    process_folders(folders)


def process_folders(folder_paths):
    """
    Process all photos in the given folders
    """
    # Common image extensions
    image_extensions = {".jpg", ".jpeg", ".JPG", ".JPEG"}

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
                    datetime_value = get_photo_datetime(file_path)

                    if datetime_value:
                        print(f"📷 {relative_path}")
                        for key, value in datetime_value.items():
                            date_utc = convert_to_utc_format(value)
                            print(f"{key} {date_utc}")
                    else:
                        print(f"📷 {relative_path}")
                        print("   DateTime: Not found in EXIF data\n")

        if photo_count == 0:
            print("No JPEG photos found in this folder.\n")
        else:
            print(f"Total photos processed: {photo_count}\n")


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
