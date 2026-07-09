# %% [markdown]
# ## Step 6: Integrating Everything
# Do: Combine all components into a complete simulator that runs continuously.

# %%
import random
import datetime
import time

# create a list of sensor objects as a class
class Sensor:
    def __init__(self, sensor_id, location, sensor_type, initial_value=None):
        self.id = sensor_id
        self.location = location
        self.type = sensor_type
        self.current_value = initial_value
        self.opened_at = None

    def read(self):
        sensor_type = self.type.lower()

        if sensor_type == "door":
            self.current_value = random.choice([True, False])
        elif sensor_type == "motion":
            self.current_value = random.choice([True, False])
        elif sensor_type == "smoke":
            self.current_value = random.choice([True, False])
        elif sensor_type == "temperature":
            self.current_value = round(random.uniform(30, 100), 1)

        return self.current_value

    def reset(self):
        self.current_value = None
        self.opened_at = None

    def isAbnormal(self):
        sensor_type = self.type.lower()
        if sensor_type in ["door", "motion", "smoke"]:
            return self.current_value is True
        elif sensor_type == "temperature":
            return self.current_value > 95 or self.current_value < 35
        return False

# %%
# Initialize a list of sensor objects with their respective attributes
def initialize_sensors():
    sensors = []
    sensors.append(Sensor("S1", "Front_Door", "door"))
    sensors.append(Sensor("S2", "Living_Room", "motion"))
    sensors.append(Sensor("S3", "Living_Room", "temperature"))
    sensors.append(Sensor("S4", "Living_Room", "smoke"))
    return sensors

# %%
# Creating an alert dictionary with sensor id, alert value, alert type, severity, message, and timestamp
def create_alert(sensor_id, alert_value, alert_type, alert_severity, message, timestamp):
    alert = {
        "sensor_id": sensor_id,
        "alert_value": alert_value,
        "alert_type": alert_type,
        "severity": alert_severity,
        "message": message,
        "timestamp": timestamp,
    }
    return alert

# Updates the alerts list by appending a new alert to it and returns the updated list
def update_alerts(alerts_list, alert):
    alerts_list.append(alert)
    return alerts_list

# Logs events with a timestamp and message to the event log list
def log_event(event_log, message):
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
    event_log.append(f"{timestamp} - {message}")
    return event_log

# %%
# Changing the check sensor function to use the class objects instaed of the dictionary based ones.
# This will allow for better encapsulation and object-oriented design.

# Check if the door sensor is active and return an intrusion alert.
def check_sensor_door(sensor, alerts_list, event_log):
    log_event(event_log, f"Checking sensor {sensor.id} at {sensor.location}")

    if sensor.current_value:
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

        print(f"Alert: Sensor {sensor.id} at {sensor.location} indicates a door opening! High risk of intrusion. timestamp: {timestamp}")

        new_alert = create_alert(
            sensor.id,
            sensor.current_value,
            "SECURITY",
            "HIGH",
            "Opened door",
            timestamp
        )
        update_alerts(alerts_list, new_alert)
        return new_alert

    return False

# Check if the motion sensor is active and return an intrusion alert.
def check_sensor_motion(sensor, alerts_list, event_log):
    log_event(event_log, f"Checking sensor {sensor.id} at {sensor.location}")

    if sensor.current_value:
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

        print(f"Alert: Sensor {sensor.id} at {sensor.location} detected movement. High risk of intrusion. timestamp: {timestamp}")

        new_alert = create_alert(
            sensor.id,
            sensor.current_value,
            "SECURITY",
            "HIGH",
            "Motion detected",
            timestamp
        )
        update_alerts(alerts_list, new_alert)
        return new_alert

    return False

# Check if the smoke sensor is active and return a fire alert.
def check_sensor_smoke(sensor, alerts_list, event_log):
    log_event(event_log, f"Checking sensor {sensor.id} at {sensor.location}")

    if sensor.current_value:
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

        print(f"Alert: Sensor {sensor.id} at {sensor.location} detected smoke. High risk of fire. timestamp: {timestamp}")

        new_alert = create_alert(
            sensor.id,
            sensor.current_value,
            "SAFETY",
            "HIGH",
            "Smoke detected",
            timestamp
        )
        update_alerts(alerts_list, new_alert)
        return new_alert

    return False

# Check if the temperature is dangerously high or low.
def check_sensor_temperature(sensor, alerts_list, event_log):
    log_event(event_log, f"Checking sensor {sensor.id} at {sensor.location}")

    if sensor.current_value > 95:
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

        print(
            f"Alert: Sensor {sensor.id} at {sensor.location} has triggered a high temperature alert! "
            f"Current value: {sensor.current_value} °F, Equipment failure risk. timestamp: {timestamp}"
        )

        new_alert = create_alert(
            sensor.id,
            sensor.current_value,
            "SAFETY",
            "MEDIUM",
            "High temperature",
            timestamp
        )
        update_alerts(alerts_list, new_alert)
        return new_alert

    elif sensor.current_value < 35:
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

        print(
            f"Alert: Sensor {sensor.id} at {sensor.location} has triggered a low temperature alert! "
            f"Current value: {sensor.current_value} °F, Frozen pipe risk. timestamp: {timestamp}"
        )

        new_alert = create_alert(
            sensor.id,
            sensor.current_value,
            "SAFETY",
            "MEDIUM",
            "Low temperature",
            timestamp
        )
        update_alerts(alerts_list, new_alert)
        return new_alert

    return False

# Check if the temperature is outside the comfort range in HOME mode.
def check_home_comfort_temperature(sensor, alerts_list, event_log):
    log_event(event_log, f"Checking sensor {sensor.id} at {sensor.location}")

    if sensor.current_value < 65:
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

        print(
            f"Notification: Sensor {sensor.id} at {sensor.location} reports a low comfort temperature. "
            f"Current value: {sensor.current_value} °F. Home may feel too cold. timestamp: {timestamp}"
        )

        new_alert = create_alert(
            sensor.id,
            sensor.current_value,
            "COMFORT",
            "LOW",
            "Temperature below comfort range",
            timestamp
        )
        update_alerts(alerts_list, new_alert)
        return new_alert

    elif sensor.current_value > 75:
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

        print(
            f"Notification: Sensor {sensor.id} at {sensor.location} reports a high comfort temperature. "
            f"Current value: {sensor.current_value} °F. Home may feel too warm. timestamp: {timestamp}"
        )

        new_alert = create_alert(
            sensor.id,
            sensor.current_value,
            "COMFORT",
            "LOW",
            "Temperature above comfort range",
            timestamp
        )
        update_alerts(alerts_list, new_alert)
        return new_alert

    return False

# Check if a door has been left open for more than 5 minutes in HOME mode and return a reminder notification.
def check_door_left_open(sensor, alerts_list, event_log):
    log_event(event_log, f"Checking sensor {sensor.id} at {sensor.location}")

    if sensor.current_value is True:
        if sensor.opened_at is None:
            sensor.opened_at = datetime.datetime.now()

        current_time = datetime.datetime.now()
        time_open = current_time - sensor.opened_at
        minutes_open = time_open.total_seconds() / 60

        if minutes_open > 5:
            timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Reminder: Sensor {sensor.id} at {sensor.location} has been left open for more than 5 minutes. Current open time: {int(minutes_open)} minutes. timestamp: {timestamp}")

            new_alert = create_alert(sensor.id, sensor.current_value, "COMFORT", "LOW", "Door left open", timestamp)
            update_alerts(alerts_list, new_alert)
            return new_alert
    else:
        sensor.opened_at = None

    return False

# %%
# Processing all sensors according to the system mode and triggering appropriate alerts or notifications
def process_sensor_by_mode(sensor, alerts_list, event_log, system_mode):
    sensor_type = sensor.type.lower()

    if system_mode == "AWAY":
        if sensor_type == "door":
            return check_sensor_door(sensor, alerts_list, event_log)
        elif sensor_type == "motion":
            return check_sensor_motion(sensor, alerts_list, event_log)
        elif sensor_type == "smoke":
            return check_sensor_smoke(sensor, alerts_list, event_log)
        elif sensor_type == "temperature":
            return check_sensor_temperature(sensor, alerts_list, event_log)

    elif system_mode == "HOME":
        if sensor_type == "door":
            return check_door_left_open(sensor, alerts_list, event_log)
        elif sensor_type == "smoke":
            return check_sensor_smoke(sensor, alerts_list, event_log)
        elif sensor_type == "temperature":
            danger_alert = check_sensor_temperature(sensor, alerts_list, event_log)
            if danger_alert:
                return danger_alert

            return check_home_comfort_temperature(sensor, alerts_list, event_log)

    return False

# %%
# Reading all sensors, logging events, and processing them based on the current system mode
def process_all_sensors(sensors, alerts_list, event_log, system_mode):
    for sensor in sensors:
        sensor.read()
        log_event(event_log, f"Sensor {sensor.id} at {sensor.location} generated reading: {sensor.current_value}")
        process_sensor_by_mode(sensor, alerts_list, event_log, system_mode)

# %%
def get_system_mode():
    while True:
        mode = input("Welcome to HomeGuard! Enter mode (HOME or AWAY): ").upper()
        if mode == "HOME" or mode == "AWAY":
            return mode
        print("Invalid mode. Please enter HOME or AWAY.")

# %%
def display_sensor_readings(sensors):
    print("\nCurrent Sensor Readings:")
    print("-" * 50)
    for sensor in sensors:
        print(f"Sensor ID: {sensor.id} | Type: {sensor.type} | Location: {sensor.location} | Value: {sensor.current_value}")

# %%
def display_alerts(alerts_list, start_index):
    new_alerts = alerts_list[start_index:]

    if new_alerts:
        print("\nNew Alerts:")
        print("-" * 50)
        for alert in new_alerts:
            print(f"[{alert['timestamp']}] {alert['alert_type']} - {alert['message']} "
                  f"(Sensor {alert['sensor_id']}, Severity: {alert['severity']}, Value: {alert['alert_value']})")
    else:
        print("\nNew Alerts:")
        print("-" * 50)
        print("No new alerts this cycle.")

# %% [markdown]
# 

# %%
def format_reading(sensor):
    sensor_type = sensor.type.lower()

    if sensor_type == "motion":
        status = "Motion detected" if sensor.current_value else "No activity"
        return f"[READING] {sensor.location.replace('_', ' ')} Motion: {status}"

    elif sensor_type == "door":
        status = "OPENED" if sensor.current_value else "CLOSED"
        return f"[READING] {sensor.location.replace('_', ' ')}: {status}"

    elif sensor_type == "temperature":
        if sensor.current_value < 35:
            status = "Low"
        elif sensor.current_value > 95:
            status = "High"
        elif sensor.current_value < 65 or sensor.current_value > 75:
            status = "Comfort warning"
        else:
            status = "Normal"

        return f"[READING] {sensor.location.replace('_', ' ')} Temperature: {sensor.current_value}°F ({status})"

    elif sensor_type == "smoke":
        status = "SMOKE DETECTED" if sensor.current_value else "CLEAR"
        return f"[READING] {sensor.location.replace('_', ' ')} Smoke: {status}"

    return f"[READING] {sensor.location.replace('_', ' ')}: {sensor.current_value}"

def format_alert(alert, sensor, system_mode):
    location = sensor.location.replace('_', ' ')
    sensor_type = sensor.type.lower()

    if sensor_type == "door" and system_mode == "AWAY":
        message = f"{location} opened while in AWAY mode!"

    elif sensor_type == "motion" and system_mode == "AWAY":
        message = f"Motion detected in {location} while in AWAY mode!"

    elif sensor_type == "smoke":
        message = f"Smoke detected in {location}!"

    elif sensor_type == "temperature":
        if alert["message"] == "High temperature":
            message = f"{location} temperature is too high!"
        elif alert["message"] == "Low temperature":
            message = f"{location} temperature is too low!"
        elif alert["message"] == "Temperature below comfort range":
            message = f"{location} feels too cold."
        elif alert["message"] == "Temperature above comfort range":
            message = f"{location} feels too warm."
        else:
            message = alert["message"]

    elif sensor_type == "door" and system_mode == "HOME":
        message = f"{location} has been left open too long."

    else:
        message = alert["message"]

    return f"[ALERT!] 🚨 {alert['severity']}: {alert['alert_type']}: {message}"

def format_log_message(message, current_time):
    return f"[LOG] [{current_time}] {message}"

import time

def run_simulator_step7():
    system_mode = get_system_mode()
    state = initialize_system_state(system_mode)

    sensors = state["sensors"]
    alerts_list = state["alerts_list"]
    event_log = state["event_log"]

    print("=== HomeGuard Security System ===")

    while True:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        print(f"\nTime: {current_time}")
        print(f"Mode: {system_mode}\n")

        old_alert_count = len(alerts_list)

        for sensor in sensors:
            sensor.read()
            print(format_reading(sensor))

            alert = process_sensor_by_mode(sensor, alerts_list, event_log, system_mode)

            if alert:
                print(format_alert(alert, sensor, system_mode))
                print(f"[LOG] [{current_time}] Sending notification to homeowner...")

        user_choice = input("\nPress Enter for next cycle, type CHANGE to switch mode, or STOP to exit: ").upper()

        if user_choice == "STOP":
            print("\nSimulator stopped.")
            break

        elif user_choice == "CHANGE":
            system_mode = get_system_mode()
            print(f"\n[LOG] [{datetime.datetime.now().strftime('%H:%M:%S')}] System mode changed to {system_mode}")

        time.sleep(1)