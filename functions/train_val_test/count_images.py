import os
from PIL import Image
import pillow_heif

# Register HEIF format with PIL
pillow_heif.register_heif_opener()

def count_image_files_in_folder(folder_path, convert_heic=False):
    """
    Counts the number of unique image files (PNG, JPG, JPEG, HEIC) in the given folder.
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

    # Collect all image files (with full paths)
    image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(supported_extensions)]

    # Track unique file base names (excluding extensions)
    unique_files = set()

    if convert_heic:
        # Process HEIC files
        for image_file in image_files:
            if image_file.lower().endswith('.heic'):
                heic_path = image_file
                jpeg_path = os.path.splitext(heic_path)[0] + '.jpeg'

                if os.path.splitext(os.path.basename(heic_path))[0] not in unique_files:
                    # Convert HEIC to JPEG if not already converted
                    if not os.path.exists(jpeg_path):
                        try:
                            image = Image.open(heic_path)
                            image.save(jpeg_path, "JPEG")
                        except Exception as e:
                            print(f"Failed to convert {heic_path}: {e}")

                # Add the base name to the unique set
                unique_files.add(os.path.splitext(os.path.basename(heic_path))[0])
    else:
        # Process non-HEIC files
        for image_file in image_files:
            unique_files.add(os.path.splitext(os.path.basename(image_file))[0])

    return len(unique_files)
