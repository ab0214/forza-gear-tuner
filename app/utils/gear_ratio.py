import math
from typing import List
from core.telemetry_frame import TelemetryFrame


def calc_drivetrain_output_speed(tf: TelemetryFrame) -> float:
    """Calculate the average speed of driving wheels, in rad/s."""
    match tf.Drivetrain:
        case 0:  # FWD
            return (tf.WheelSpeedFL + tf.WheelSpeedFR) / 2
        case 1:  # RWD
            return (tf.WheelSpeedRL + tf.WheelSpeedRR) / 2
        case 2:  # AWD
            return (
                tf.WheelSpeedFL + tf.WheelSpeedFR + tf.WheelSpeedRL + tf.WheelSpeedRR
            ) / 4
        case _:
            return float("nan")


def calc_ratio(tf: TelemetryFrame) -> float:
    """Calculate the gear ratio based on engine RPM and driving wheel speed."""
    output_rads = calc_drivetrain_output_speed(tf)
    if output_rads == 0:
        return float("nan")  # Avoid division by zero
    input_rads = tf.RPM * (2 * math.pi / 60)  # Convert RPM to rad/s
    return input_rads / output_rads  # Return input/output ratio


def analyze_gear_ratio(tfs: List[TelemetryFrame], gear: int) -> float:
    """Determine the gear ratio for a specific gear based on telemetry data."""
    # Select only frames with the specified gear
    # and conditions where the we can accurately calculate the ratio
    filtered = [
        tf
        for tf in tfs
        if tf.Gear == gear
        and tf.Clutch == 0
        and tf.WheelSpeedFL > 0
        and tf.WheelSpeedFR > 0
        and tf.WheelSpeedRL > 0
        and tf.WheelSpeedRR > 0
        and tf.Speed > 0
        and tf.RPM > tf.IdleRPM * 1.5
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
    max_gear = max((int(tf.Gear) for tf in tfs), default=0)  # Find top gear
    gear_ratios = []
    for gear in range(0, max_gear + 1):
        gear_ratios.append(analyze_gear_ratio(tfs, gear))
    return gear_ratios
