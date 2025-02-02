from umqtt.simple import MQTTClient

BROKER = "10.0.0.193"
PORT = 1883
CLIENT_ID = "motion_detector_1"
USERNAME = "motion_detector_1"
PASSWORD = "get_detected"

mqtt_client = None

def connect_mqtt():
    global mqtt_client
    client = MQTTClient(
        CLIENT_ID,
        BROKER,
        PORT,
        USERNAME,
        PASSWORD
    )

    client.connect()
    print("Connected to MQTT broker")

    mqtt_client = client

def publish_sensor_trip():
    mqtt_client.publish(f"{CLIENT_ID}/motion_detected", "")