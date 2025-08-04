import struct
from dataclasses import dataclass

@dataclass
class TelemetryFrame:
    
    @classmethod
    def from_packet(cls, packet: bytes) -> "TelemetryFrame":
        data_format = '<iIfffffffffffffffffffffffffffffffffffffffffffffffffffiiiiiiIIfffffffffffffffffHBBBBBBbbb'
        values = struct.unpack(data_format, packet[:323])
        return cls(*values)


    # Basic info
    IsRaceOn: int
    TimestampMS: int  # can overflow to 0

    # Engine RPM
    MaxRPM: float
    IdleRPM: float
    RPM: float

    # Acceleration (m/s^2?), car's right, up, forward
    AccelX: float
    AccelY: float
    AccelZ: float

    # Linear velocity (m/s?), car's right, up, forward
    LinVelX: float
    LinVelY: float
    LinVelZ: float

    # Angular velocity (rad/s?), car's right, up, forward
    AngVelX: float
    AngVelY: float
    AngVelZ: float

    # Orientation
    Yaw: float
    Pitch: float
    Roll: float

    # Suspension normalized (0 = fully extended, 1 = fully compressed)
    SuspNormFL: float
    SuspNormFR: float
    SuspNormRL: float
    SuspNormRR: float

    # Slip ratio (0 = max grip, 1 = min grip)
    SlipRatioFL: float
    SlipRatioFR: float
    SlipRatioRL: float
    SlipRatioRR: float

    # Wheel speed (rad/s)
    WheelSpeedFL: float
    WheelSpeedFR: float
    WheelSpeedRL: float
    WheelSpeedRR: float

    # Surface info
    OnRumbleStripFL: int
    OnRumbleStripFR: int
    OnRumbleStripRL: int
    OnRumbleStripRR: int
    InPuddleFL: int
    InPuddleFR: int
    InPuddleRL: int
    InPuddleRR: int
    SurfaceRumbleFL: int
    SurfaceRumbleFR: int
    SurfaceRumbleRL: int
    SurfaceRumbleRR: int

    # Slip angles (0 = max grip, 1 = min grip)
    SlipAngleFL: float
    SlipAngleFR: float
    SlipAngleRL: float
    SlipAngleRR: float

    # Combined slip (longitudinal + lateral?)
    SlipCombinedFL: float
    SlipCombinedFR: float
    SlipCombinedRL: float
    SlipCombinedRR: float

    # Suspension absolute compression?, meters
    SuspAbsFL: float
    SuspAbsFR: float
    SuspAbsRL: float
    SuspAbsRR: float

    # Car info
    CarOrdinal: int  # unique make/model id
    CarClass: int    # enum
    CarPI: int       # performance index
    Drivetrain: int  # enum
    Cylinders: int   # 0-255
    CarType: int     # enum

    # Unknown/placeholder
    Placeholder2: int  # unknown
    Placeholder3: int  # unknown

    # Position
    PosX: float
    PosY: float
    PosZ: float
    
    # Dyno
    Speed: float     # m/s
    Power: float     # W
    Torque: float    # Nm

    # Tire temperatures
    TireTempFL: float
    TireTempFR: float
    TireTempRL: float
    TireTempRR: float

    # Misc
    Boost: float     # PSI?
    Fuel: float
    DistTraveled: float

    # Race info
    BestLapTime: float
    LastLapTime: float
    CurLapTime: float
    CurRaceTime: float
    LapNo: int
    RacePos: int

    # Inputs (0-255)
    Throttle: int
    Brake: int
    Clutch: int
    Handbrake: int
    Gear: int       # 0-255
    Steer: int      # -127 to 127

    # Unknown
    DrivingLine: int # normalized
    AIBrakeDiff: int # normalized
