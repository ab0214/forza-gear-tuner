import math
from typing import List

from core.telemetry_frame import TelemetryFrame


def calc_drivetrain_output_speed(tf: TelemetryFrame) -> float:
    """Calculate the average speed of driving wheels, in rad/s."""
    match tf.drivetrain:
        case 0:  # FWD
            return (tf.wheel_speed_fl + tf.wheel_speed_fr) / 2
        case 1:  # RWD
            return (tf.wheel_speed_rl + tf.wheel_speed_rr) / 2
        case 2:  # AWD
            return (
                tf.wheel_speed_fl
                + tf.wheel_speed_fr
                + tf.wheel_speed_rl
                + tf.wheel_speed_rr
            ) / 4
        case _:
            return float("nan")


def calc_ratio(tf: TelemetryFrame) -> float:
    """Calculate the gear ratio based on engine RPM and driving wheel speed."""
    output_rads = calc_drivetrain_output_speed(tf)
    if output_rads == 0:
        return float("nan")  # Avoid division by zero
    input_rads = tf.rpm * (2 * math.pi / 60)  # Convert RPM to rad/s
    return input_rads / output_rads  # Return input/output ratio


def analyze_gear_ratio(tfs: List[TelemetryFrame], gear: int) -> float:
    """Determine the gear ratio for a specific gear based on telemetry data."""
    # Select only frames with the specified gear
    # and conditions where the we can accurately calculate the ratio
    filtered = [
        tf
        for tf in tfs
        if tf.gear == gear
        and tf.clutch == 0
        and tf.wheel_speed_fl > 0
        and tf.wheel_speed_fr > 0
        and tf.wheel_speed_rl > 0
        and tf.wheel_speed_rr > 0
        and tf.speed > 0
        and tf.rpm > tf.idle_rpm * 1.5
        and tf.slip_ratio_fl < 0.1
        and tf.slip_ratio_fr < 0.1
        and tf.slip_ratio_rl < 0.1
        and tf.slip_ratio_rr < 0.1
    ]
    # Calculate the gear ratio for each valid frame
    ratios = [calc_ratio(tf) for tf in filtered]
    # Filter out invalid ratios (NaN, inf)
    ratios = [r for r in ratios if not math.isnan(r) and not math.isinf(r)]
    # If no valid ratios, return NaN
    if not ratios:
        return float("nan")
    # Remove outliers using simple z-score
    mean = sum(ratios) / len(ratios)
    std = (
        (sum((r - mean) ** 2 for r in ratios) / len(ratios)) ** 0.5
        if len(ratios) > 1
        else 0
    )
    ratios = [r for r in ratios if std == 0 or abs((r - mean) / std) < 1]
    if not ratios:
        return float("nan")
    # Return the average of the remaining ratios
    return sum(ratios) / len(ratios)


def analyze_gear_ratios(tfs: List[TelemetryFrame]) -> List[float]:
    """Determine gear ratios for all gears based on telemetry data."""
    max_gear = max((int(tf.gear) for tf in tfs), default=0)  # Find top gear
    gear_ratios = [float("nan")] * (max_gear + 1)  # Initialize all ratios as NaN
    for gear in range(0, max_gear + 1):
        gear_ratios[gear] = analyze_gear_ratio(tfs, gear)
    return gear_ratios


def calc_rpm_to_kmh_ratio(tf: TelemetryFrame) -> float:
    """Calculate the km/h per RPM ratio for a telemetry frame."""
    if tf.rpm == 0:
        return float("nan")  # Avoid division by zero
    return (tf.speed * 3.6) / tf.rpm  # Return km/h per RPM


def analyze_rpm_to_kmh_ratio(tfs: List[TelemetryFrame], gear: int) -> float:
    """Determine the rpm to km/h conversion ratio for a specific gear based on telemetry data."""
    # Select only frames with the specified gear
    # and conditions where we can accurately calculate the ratio
    filtered = [
        tf
        for tf in tfs
        if tf.gear == gear
        and tf.clutch == 0
        and tf.speed > 0
        and tf.rpm > tf.idle_rpm * 1.1
        and tf.slip_ratio_fl < 0.1
        and tf.slip_ratio_fr < 0.1
        and tf.slip_ratio_rl < 0.1
        and tf.slip_ratio_rr < 0.1
    ]
    # Calculate the rpm_to_kmh ratio for each valid frame
    ratios = [calc_rpm_to_kmh_ratio(tf) for tf in filtered]
    # Filter out invalid ratios (NaN, inf)
    ratios = [r for r in ratios if not math.isnan(r) and not math.isinf(r)]
    # If no valid ratios, return NaN
    if not ratios:
        return float("nan")
    # Remove outliers using simple z-score
    mean = sum(ratios) / len(ratios)
    std = (
        (sum((r - mean) ** 2 for r in ratios) / len(ratios)) ** 0.5
        if len(ratios) > 1
        else 0
    )
    ratios = [r for r in ratios if std == 0 or abs((r - mean) / std) < 1]
    if not ratios:
        return float("nan")
    # Return the average of the remaining ratios
    return sum(ratios) / len(ratios)


def analyze_rpm_to_kmh_ratios(tfs: List[TelemetryFrame]) -> List[float]:
    """Determine rpm to km/h conversion ratios for all gears based on telemetry data."""
    max_gear = max((int(tf.gear) for tf in tfs), default=0)  # Find top gear
    rpm_to_kmh_ratios = [float("nan")] * (max_gear + 1)  # Initialize all ratios as NaN
    for gear in range(0, max_gear + 1):
        rpm_to_kmh_ratios[gear] = analyze_rpm_to_kmh_ratio(tfs, gear)
    return rpm_to_kmh_ratios


def get_engine_max_rpm(tfs: List[TelemetryFrame]) -> float:
    """Get the maximum engine RPM observed in the telemetry data."""
    max_rpm = max((tf.engine_max_rpm for tf in tfs), default=0)
    return max_rpm


def get_engine_idle_rpm(tfs: List[TelemetryFrame]) -> float:
    """Get the engine idle RPM observed in the telemetry data."""
    idle_rpm = min((tf.idle_rpm for tf in tfs), default=0)
    return idle_rpm
