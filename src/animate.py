from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from time import sleep_ms

# Initialize I2C and OLED display
i2c = I2C(scl=Pin(5), sda=Pin(4))  # SCL=D1 (GPIO5), SDA=D2 (GPIO4)
oled = SSD1306_I2C(128, 64, i2c)

def load_bmp(filename):
    """Load a 1-bit 128x64 BMP into a 1024-byte display buffer."""
    ssd1306_buf = bytearray(1024)  # 128*64/8 = 1024
    
    with open(filename, "rb") as f:
        # Read header to validate
        f.seek(18)
        bmp_width = int.from_bytes(f.read(4), "little")
        bmp_height = int.from_bytes(f.read(4), "little")
        f.seek(28)
        bpp = int.from_bytes(f.read(2), "little")

        if bmp_width != 128 or abs(bmp_height) != 64 or bpp != 1:
            raise ValueError("Unsupported BMP format! Must be 128x64, 1-bit.")

        # Calculate how many bytes per row (rounded up to the nearest byte)
        row_size = (bmp_width + 7) // 8
        row_padding = (4 - (row_size % 4)) % 4

        f.seek(10)
        data_offset = int.from_bytes(f.read(4), "little")

        # Now read the image data, bottom to top for typical BMP
        for row_index in range(64):
            # The BMP’s first row in file is the bottom row on screen
            offset = (63 - row_index) * (row_size + row_padding)
            f.seek(data_offset + offset)
            row_data = f.read(row_size)

            # For each pixel x in [0..127], set or clear the correct bit
            for x in range(128):
                byte_index = x // 8       # which byte in row_data
                bit_index = 7 - (x % 8)   # bit within that byte
                pixel_color = (row_data[byte_index] >> bit_index) & 1

                # Translate (x, row_index) to SSD1306 buffer index
                page = row_index // 8
                bit_in_page = row_index % 8
                index_in_buffer = x + page * 128

                if pixel_color:
                    ssd1306_buf[index_in_buffer] |= (1 << bit_in_page)
                else:
                    ssd1306_buf[index_in_buffer] &= ~(1 << bit_in_page)
    
    return ssd1306_buf

def display_frame(frame_data):
    """Write 1024 bytes directly to the OLED's buffer and show."""
    # Copy the frame_data into oled's buffer
    for i in range(1024):
        oled.buffer[i] = frame_data[i]
    oled.show()

def play_animation(frames, durations):
    """Play animation using preloaded frames."""
    if len(frames) != len(durations):
        print("Frame array and durations array should have the same length")
        return

    oled.poweron()

    # Iterate over preloaded frames
    for frame_data, duration in zip(frames, durations):
        display_frame(frame_data)
        sleep_ms(duration)

    oled.poweroff()