import math
from typing import List
from core.telemetry_frame import TelemetryFrame


def calc_drivetrain_output_speed(tf: TelemetryFrame) -> float:
    '''Calculate the average speed of driving wheels, in rad/s.'''
    if tf.Drivetrain == 0:  # FWD
        return (tf.WheelSpeedFL + tf.WheelSpeedFR) / 2
    elif tf.Drivetrain == 1:  # RWD
        return (tf.WheelSpeedRL + tf.WheelSpeedRR) / 2
    elif tf.Drivetrain == 2:  # AWD
        return (tf.WheelSpeedFL + tf.WheelSpeedFR + tf.WheelSpeedRL + tf.WheelSpeedRR) / 4
    else:
        return float('nan')


def calc_ratio(tf: TelemetryFrame) -> float:
    '''Calculate the gear ratio based on engine RPM and driving wheel speed.'''
    output_rads = calc_drivetrain_output_speed(tf)
    if output_rads == 0:
        return float('nan')
    input_rads = tf.RPM * (2 * math.pi / 60)
    return input_rads / output_rads


def analyze_gear_ratio(tfs: List[TelemetryFrame], gear: int) -> float:
    filtered = [tf for tf in tfs
                if tf.Gear == gear and tf.Clutch == 0
                and tf.WheelSpeedFL > 0 and tf.WheelSpeedFR > 0
                and tf.WheelSpeedRL > 0 and tf.WheelSpeedRR > 0
                and tf.Speed > 0 and tf.RPM > tf.IdleRPM * 1.5]
    ratios = [calc_ratio(tf) for tf in filtered]
    ratios = [r for r in ratios if not math.isnan(r) and not math.isinf(r)]
    if not ratios:
        return float('nan')
    # Remove outliers using simple z-score
    mean = sum(ratios) / len(ratios)
    std = (sum((r - mean) ** 2 for r in ratios) /
           len(ratios)) ** 0.5 if len(ratios) > 1 else 0
    filtered_ratios = [r for r in ratios if std ==
                       0 or abs((r - mean) / std) < 1]
    if not filtered_ratios:
        return float('nan')
    return sum(filtered_ratios) / len(filtered_ratios)


def analyze_gear_ratios(tfs: List[TelemetryFrame]) -> dict:
    # Find max gear number
    max_gear = max((int(tf.Gear) for tf in tfs), default=0)
    gear_ratios = {}
    for gear in range(1, max_gear + 1):
        gear_ratios[gear] = analyze_gear_ratio(tfs, gear)
    return gear_ratios
