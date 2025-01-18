import os
from PIL import Image
import pillow_heif

# Register HEIF format with PIL
pillow_heif.register_heif_opener()

def count_image_files_in_folder(folder_path, convert_heic=False):
    """
    Counts the number of image files (PNG, JPG, JPEG, HEIC) in the given folder.
    Optionally converts HEIC files to JPEG.

    Parameters:
    folder_path (str): The path to the folder containing the image files.
    convert_heic (bool): If True, converts HEIC files to JPEG and includes them in the count.

    Returns:
    int: The number of unique image files in the folder.
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder does not exist: {folder_path}")

    # List of supported extensions
    supported_extensions = ('.png', '.jpg', '.jpeg', '.heic')
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(supported_extensions)]

    converted_files = set()  # To keep track of converted HEIC files

    if convert_heic:
        # Convert HEIC files to JPEG
        heic_files = [f for f in image_files if f.lower().endswith('.heic')]
        for heic_file in heic_files:
            heic_path = os.path.join(folder_path, heic_file)
            jpeg_path = os.path.splitext(heic_path)[0] + '.jpeg'
            try:
                # Check if the JPEG file already exists to avoid duplication
                if not os.path.exists(jpeg_path):
                    # Open HEIC file and save as JPEG
                    image = Image.open(heic_path)
                    image.save(jpeg_path, "JPEG")
                converted_files.add(jpeg_path)  # Track the converted file
            except Exception as e:
                print(f"Failed to convert {heic_file}: {e}")

    # Remove duplicates: count only unique files (originals + converted)
    unique_files = set(image_files) | converted_files
    return len(unique_files)
