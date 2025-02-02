import sys
from PIL import Image

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_image>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = input_path.split(".")[0] + "_mono.bmp"

    # Open the image
    img = Image.open(input_path)

    # Convert to 1-bit monochrome
    img = img.convert("1")

    # Save the result
    img.save(output_path)
    print(f"Converted '{input_path}' to monochrome and saved as '{output_path}'.")

if __name__ == "__main__":
    main()