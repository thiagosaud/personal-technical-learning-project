"""
Data Pipeline Module [ETL LAYER].
Handles Extraction, Transformation, and Loading (ETL) tasks.
"""

import pandas as pd

from src.config.schema.data.vehicle import VehicleSchema


class ETLLayer:
    """Responsible for structuring and cleaning raw data from BYD specs documents."""

    def __init__(self) -> None:
        # Raw specifications database structured using the official Schema contracts
        self._raw_data = {
            VehicleSchema.MODEL.value: [
                "Song Pro GL",
                "Song Pro GS",
                "Song Plus Premium",
                "Song Plus 1.5T",
                "Shark DMO",
                "King GL",
                "King GS",
                "Atto 8 DM-P",
                "Atto 2 GL",
                "Atto 2 GS",
                "Yuan Pro",
                "Yuan Plus AWD",
                "Tan",
                "Sealion 7",
                "Seal",
                "Han",
                "Dolphin Special",
            ],
            VehicleSchema.WEIGHT_KG.value: [
                1700,
                1760,
                2060,
                1970,
                2710,
                1515,
                1620,
                2625,
                1510,
                1620,
                1550,
                1990,
                2621,
                2340,
                2185,
                2250,
                1485,
            ],
            VehicleSchema.POWER_CV.value: [
                218,
                219,
                324,
                240,
                437,
                209,
                235,
                488,
                177,
                197,
                177,
                449,
                517,
                531,
                531,
                517,
                177,
            ],
            VehicleSchema.ACCELERATION_FROM_0_TO_100.value: [
                8.6,
                8.8,
                5.2,
                8.1,
                5.7,
                7.9,
                7.3,
                4.9,
                8.5,
                8.4,
                7.9,
                3.9,
                4.9,
                4.5,
                3.8,
                3.9,
                8.0,
            ],
            VehicleSchema.BATTERY_KWH.value: [
                13.1,
                18.3,
                26.6,
                26.6,
                29.6,
                8.3,
                18.3,
                35.6,
                7.85,
                18.03,
                45.12,
                74.88,
                108.8,
                82.5,
                82.56,
                85.4,
                45.12,
            ],
            VehicleSchema.CONSUMPTION_MJ_KM.value: [
                0.53,
                0.55,
                0.67,
                0.63,
                0.91,
                0.53,
                0.49,
                0.71,
                0.61,
                0.61,
                0.51,
                0.58,
                0.73,
                0.66,
                0.62,
                0.69,
                0.49,
            ],
            VehicleSchema.IS_PURE_ELECTRIC.value: [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        }

    def run_etl(self) -> pd.DataFrame:
        """Transforms raw dictionary into a structured, sorted and cleaned DataFrame."""
        df = pd.DataFrame(self._raw_data)
        processed_df = df.sort_values(by=VehicleSchema.WEIGHT_KG.value).reset_index(drop=True)

        return processed_df
