from nicegui import ui
from core.telemetry_frame import TelemetryFrame
from core.udp_listener import UdpListener

# UI
rpm_display = ui.label("RPM: ")
speed_display = ui.label("Speed: ")
throttle_display = ui.label("Throttle: ")
brake_display = ui.label("Brake: ")
gear_display = ui.label("Gear: ")
steer_display = ui.label("Steer: ")


def toggle_recording():
    if listener.running:
        toggle_button.text = "Start"
        listener.stop()
    else:
        toggle_button.text = "Pause"
        listener.start()


def update_ui(tf: TelemetryFrame):
    rpm_display.text = f"RPM: {tf.rpm:.0f}"
    speed_display.text = f"Speed: {tf.speed:.1f} m/s"
    throttle_display.text = f"Throttle: {tf.throttle}"
    brake_display.text = f"Brake: {tf.brake}"
    gear_display.text = f"Gear: {tf.gear}"
    steer_display.text = f"Steer: {tf.steer}"


# Listener
listener = UdpListener(require_race_on=False)
listener.subscribe(update_ui)

# ui.timer(0.1, update_ui)

toggle_button = ui.button("Pause", on_click=toggle_recording)

ui.run()
