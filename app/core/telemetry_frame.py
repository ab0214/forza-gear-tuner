import struct
from typing import Any
from pydantic import BaseModel, ConfigDict, Field, model_validator


class TelemetryFrame(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    @model_validator(mode="before")
    @classmethod
    def unpack_packet(cls, data: Any) -> tuple[Any, ...]:
        if isinstance(data, bytes):
            data_format = "<iIfffffffffffffffffffffffffffffffffffffffffffffffffff\
                iiiiiiIIfffffffffffffffffHBBBBBBbbb"
            values = struct.unpack(data_format, data[:323])
            return dict(zip(cls.model_fields.keys(), values))
        return data

    # Basic info
    is_race_on: bool = Field(alias="IsRaceOn")
    timestamp_ms: int = Field(alias="TimestampMS")  # can overflow to 0

    # Engine RPM
    engine_max_rpm: float = Field(alias="EngineMaxRpm")
    idle_rpm: float = Field(alias="EngineIdleRpm")
    rpm: float = Field(alias="CurrentEngineRpm")

    # Acceleration (m/s^2?), car's right, up, forward
    acceleration_x: float = Field(alias="AccelerationX")
    acceleration_y: float = Field(alias="AccelerationY")
    acceleration_z: float = Field(alias="AccelerationZ")

    # Linear velocity (m/s?), car's right, up, forward
    velocity_x: float = Field(alias="VelocityX")
    velocity_y: float = Field(alias="VelocityY")
    velocity_z: float = Field(alias="VelocityZ")

    # Angular velocity (rad/s?), car's right, up, forward
    angular_velocity_x: float = Field(alias="AngularVelocityX")
    angular_velocity_y: float = Field(alias="AngularVelocityY")
    angular_velocity_z: float = Field(alias="AngularVelocityZ")

    # Orientation
    yaw: float = Field(alias="Yaw")
    pitch: float = Field(alias="Pitch")
    roll: float = Field(alias="Roll")

    # Suspension normalized (0 = fully extended, 1 = fully compressed)
    susp_norm_fl: float = Field(alias="NormalizedSuspensionTravelFrontLeft")
    susp_norm_fr: float = Field(alias="NormalizedSuspensionTravelFrontRight")
    susp_norm_rl: float = Field(alias="NormalizedSuspensionTravelRearLeft")
    susp_norm_rr: float = Field(alias="NormalizedSuspensionTravelRearRight")

    # Slip ratio (0 = max grip, 1 = min grip)
    slip_ratio_fl: float = Field(alias="TireSlipRatioFrontLeft")
    slip_ratio_fr: float = Field(alias="TireSlipRatioFrontRight")
    slip_ratio_rl: float = Field(alias="TireSlipRatioRearLeft")
    slip_ratio_rr: float = Field(alias="TireSlipRatioRearRight")

    # Wheel speed (rad/s)
    wheel_speed_fl: float = Field(alias="WheelRotationSpeedFrontLeft")
    wheel_speed_fr: float = Field(alias="WheelRotationSpeedFrontRight")
    wheel_speed_rl: float = Field(alias="WheelRotationSpeedRearLeft")
    wheel_speed_rr: float = Field(alias="WheelRotationSpeedRearRight")

    # Surface info
    on_rumble_strip_fl: bool = Field(alias="WheelOnRumbleStripFrontLeft")
    on_rumble_strip_fr: bool = Field(alias="WheelOnRumbleStripFrontRight")
    on_rumble_strip_rl: bool = Field(alias="WheelOnRumbleStripRearLeft")
    on_rumble_strip_rr: bool = Field(alias="WheelOnRumbleStripRearRight")
    in_puddle_fl: bool = Field(alias="WheelInPuddleDepthFrontLeft")
    in_puddle_fr: bool = Field(alias="WheelInPuddleDepthFrontRight")
    in_puddle_rl: bool = Field(alias="WheelInPuddleDepthRearLeft")
    in_puddle_rr: bool = Field(alias="WheelInPuddleDepthRearRight")
    surface_rumble_fl: float = Field(alias="SurfaceRumbleFrontLeft")
    surface_rumble_fr: float = Field(alias="SurfaceRumbleFrontRight")
    surface_rumble_rl: float = Field(alias="SurfaceRumbleRearLeft")
    surface_rumble_rr: float = Field(alias="SurfaceRumbleRearRight")

    # Slip angles (0 = max grip, 1 = min grip)
    slip_angle_fl: float = Field(alias="TireSlipAngleFrontLeft")
    slip_angle_fr: float = Field(alias="TireSlipAngleFrontRight")
    slip_angle_rl: float = Field(alias="TireSlipAngleRearLeft")
    slip_angle_rr: float = Field(alias="TireSlipAngleRearRight")

    # Combined slip (longitudinal + lateral?)
    slip_combined_fl: float = Field(alias="TireCombinedSlipFrontLeft")
    slip_combined_fr: float = Field(alias="TireCombinedSlipFrontRight")
    slip_combined_rl: float = Field(alias="TireCombinedSlipRearLeft")
    slip_combined_rr: float = Field(alias="TireCombinedSlipRearRight")

    # Suspension absolute compression?, meters
    susp_abs_fl: float = Field(alias="SuspensionTravelMetersFrontLeft")
    susp_abs_fr: float = Field(alias="SuspensionTravelMetersFrontRight")
    susp_abs_rl: float = Field(alias="SuspensionTravelMetersRearLeft")
    susp_abs_rr: float = Field(alias="SuspensionTravelMetersRearRight")

    # Car info
    car_ordinal: int = Field(alias="CarOrdinal")  # unique make/model id
    car_class: int = Field(alias="CarClass")  # enum
    car_pi: int = Field(alias="CarPerformanceIndex")  # performance index
    drivetrain: int = Field(alias="DrivetrainType")  # enum
    cylinders: int = Field(alias="NumCylinders")  # 0-255
    car_type: int = Field(alias="CarType", default=0)  # enum

    # Unknown/placeholder
    placeholder2: int = Field(alias="Placeholder2", default=0)  # unknown
    placeholder3: int = Field(alias="Placeholder3", default=0)  # unknown

    # Position
    pos_x: float = Field(alias="PositionX")
    pos_y: float = Field(alias="PositionY")
    pos_z: float = Field(alias="PositionZ")

    # Dyno
    speed: float = Field(alias="Speed")  # m/s
    power: float = Field(alias="Power")  # W
    torque: float = Field(alias="Torque")  # Nm

    # Tire temperatures
    tire_temp_fl: float = Field(alias="TireTempFl")
    tire_temp_fr: float = Field(alias="TireTempFr")
    tire_temp_rl: float = Field(alias="TireTempRl")
    tire_temp_rr: float = Field(alias="TireTempRr")

    # Misc
    boost: float = Field(alias="Boost")  # PSI?
    fuel: float = Field(alias="Fuel")
    dist_traveled: float = Field(alias="Distance")

    # Race info
    best_lap_time: float = Field(alias="BestLapTime")
    last_lap_time: float = Field(alias="LastLapTime")
    current_lap_time: float = Field(alias="CurrentLapTime")
    current_race_time: float = Field(alias="CurrentRaceTime")
    lap_no: int = Field(alias="Lap")
    race_pos: int = Field(alias="RacePosition")

    # Inputs (0-255)
    throttle: int = Field(alias="Accelerator")
    brake: int = Field(alias="Brake")
    clutch: int = Field(alias="Clutch")
    handbrake: int = Field(alias="Handbrake")
    gear: int = Field(alias="Gear")  # 0-255
    steer: int = Field(alias="Steer")  # -127 to 127

    # Unknown
    driving_line: int = Field(alias="NormalDrivingLine")  # normalized
    ai_brake_diff: int = Field(alias="NormalAiBrakeDifference")  # normalized
