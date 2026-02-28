"""GOAL:
1) Receives a folder.
2) Searches for images.
3) Checks if they are square.
4) Checks if they have valid power-of-two resolutions (256, 512, etc.).
5) If not valid → moves them.
6) Generates a report.
"""

from pathlib import Path
import sys
from PIL import Image
import shutil

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tga", ".bmp", ".tiff"}
VALID_SIZES = {256, 512, 1024, 2048, 4096, 8192}

print("-" * 30)
print("WELCOME TO PBR OPTIMIZER 2.0")
print("-" * 30)

# Ask the user for the folder path
user_path = input("Enter the path to the folder: ").strip().strip('"')
# strip() removes leading and trailing whitespace
# strip('"') removes quotation marks if the user includes them

# Create a Path object from the provided path
folder = Path(user_path)
# pathlib.Path is a class that provides methods to handle
# file system paths in a safer and more convenient way
# than traditional string-based path handling.
# It works independently of the operating system,
# improving code portability.

# Check if the folder exists and is a directory
if not folder.exists() or not folder.is_dir():
    print("The provided path does not exist or is not a directory.")

print("-" * 30)
print("[🔍 SEARCHING FOR FILES...]")
print("-" * 30)

# List items inside the folder
items = list(folder.iterdir())
# iterdir() is a pathlib.Path method that returns a generator
# producing Path objects for each item in the directory.
# It allows efficient iteration over files and subdirectories
# without loading everything into memory at once.

if not items:
    print("⚠ Folder is empty")
    sys.exit()

# Filter only valid image files
images = [
    im for im in items
    if im.is_file() and im.suffix.lower() in VALID_EXTENSIONS
]

if not images:
    print("There are no images in the folder")
    sys.exit()

print("\n TEXTURE VALIDATION REPORT")
print("-" * 60)
print(f"{'STATUS':<10} {'NAME':<25} {'SIZE':<10}")
print("-" * 60)

# Counters for the final report
ok_count = 0
wrong_count = 0

# Create folder for invalid images
wrong_folder = folder / "wrong_images"
wrong_folder.mkdir(exist_ok=True)
# exist_ok=True prevents an exception if the folder
# already exists, which is useful for repeated runs.

report_lines = []

# Validate each image and generate the report
for img_path in images:
    try:
        with Image.open(img_path) as img:
            width, height = img.size

        # Check if the image is square and has a valid size
        is_valid = width == height and width in VALID_SIZES
        status = "✅ VALID" if is_valid else "❌ INVALID"

        print(f"{status:<10} {img_path.name:<25} {width}x{height:<10}")

        report_lines.append(
            f"{status:<10} {img_path.name:<25} {width}x{height:<10}"
        )

        if is_valid:
            ok_count += 1
        else:
            wrong_count += 1
            shutil.move(img_path, wrong_folder / img_path.name)

            # shutil.move() moves a file or directory
            # from one location to another.

    except Exception as e:
        status = "⚠ ERROR"
        print(f"{status:<12} {img_path.name:<25} {'-':<12}")

        # If an error occurs while opening the image,
        # it is considered invalid and moved to the invalid folder.
        shutil.move(img_path, wrong_folder / img_path.name)

        # The error is logged in the report and counted as invalid.
        report_lines.append(
            f"{status:<12} {img_path.name:<25} {'-':<12}"
        )

        wrong_count += 1
        print("APPENDED:", img_path.name)
# After processing all images, we create a report summarizing the results.
report_folder = folder / "reports"
report_folder.mkdir(exist_ok=True)
# Create a "reports" folder to store the validation report.
report_path = report_folder / "validation_report.txt"

# Write the report to a text file
with open(report_path, "w", encoding="utf-8") as file:
    file.write("TEXTURE VALIDATION REPORT\n")
    file.write("-" * 60 + "\n")
    file.write(f"{'STATUS':<10} {'NAME':<25} {'SIZE':<10}\n")

    for line in report_lines:
        file.write(line + "\n")

    file.write("-" * 60 + "\n")
    file.write(f"TOTAL images: {len(images)}\n")
    file.write(f"VALID images: {ok_count}\n")
    file.write(f"INVALID images: {wrong_count}\n")


print("-" * 60)
print(f"TOTAL images: {len(images)}")
print(f"VALID images: {ok_count}")
print(f"INVALID images: {wrong_count}")
print("-" * 60)