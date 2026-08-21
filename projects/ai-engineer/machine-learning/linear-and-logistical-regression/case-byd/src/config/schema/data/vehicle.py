"""
Data Schema Module.
Defines the enterprise data contracts for vehicle attributes.
"""

from enum import StrEnum


class VehicleSchema(StrEnum):
    """
    Contract for Dataframe Column Names.
    Centralizes and guarantees structural consistency across all pipeline layers.
    """

    MODEL = "MODEL"
    WEIGHT_KG = "WEIGHT_KG"
    POWER_CV = "POWER_CV"
    ACCELERATION_FROM_0_TO_100 = "ACCELERATION_FROM_0_TO_100"
    BATTERY_KWH = "BATTERY_KWH"
    CONSUMPTION_MJ_KM = "CONSUMPTION_MJ_KM"
    IS_PURE_ELECTRIC = "IS_PURE_ELECTRIC"
