from PIL import Image

# Load the BMP file
image = Image.open("eye_blink_1_mono.bmp")

# Check the mode
print(f"Image format: {image.format}")
print(f"Image mode: {image.mode}")  # Example output: "1", "L", or "P"
print(f"Image size: {image.size}")  # Example output: (128, 64)
print(f"Image info: {image.info}")