from animate import display_frame, play_animation, load_bmp
from machine import Pin
from time import sleep
from network_helper import connect_mqtt, publish_sensor_trip

def main():
    try:
        connect_mqtt()
        motion_detector = Pin(14, Pin.IN)
        frames = [
            load_bmp("eye_blink_1_mono.bmp"),
            load_bmp("eye_blink_2_mono.bmp"),
            load_bmp("eye_blink_3_mono.bmp"),
            load_bmp("eye_blink_4_mono.bmp"),
            load_bmp("eye_blink_5_mono.bmp"),
        ]
        frames = frames + frames[3::-1]
        durations = [
            1000,
            10,
            10,
            10,
            10,
            10,
            10,
            10,
            1000
        ]

        prev_state = False

        while True:
            current_state = motion_detector.value()

            if current_state == 1 and prev_state == 0:
                play_animation(frames, durations)
                # publish_sensor_trip()
            
            sleep(1)

    except Exception as e:
        print("Error:", e)

main()