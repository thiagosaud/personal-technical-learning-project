"""Unit tests for VehicleSchema and ETLLayer."""

import pandas as pd

from src.config.schema.data.vehicle import VehicleSchema
from src.layer.data.etl import ETLLayer


def test_vehicle_schema_constants() -> None:
    """Verifies that enum values match the enterprise specification contract."""
    assert VehicleSchema.MODEL.value == "MODEL"
    assert VehicleSchema.WEIGHT_KG.value == "WEIGHT_KG"
    assert VehicleSchema.POWER_CV.value == "POWER_CV"
    assert VehicleSchema.ACCELERATION_FROM_0_TO_100.value == "ACCELERATION_FROM_0_TO_100"
    assert VehicleSchema.BATTERY_KWH.value == "BATTERY_KWH"
    assert VehicleSchema.CONSUMPTION_MJ_KM.value == "CONSUMPTION_MJ_KM"
    assert VehicleSchema.IS_PURE_ELECTRIC.value == "IS_PURE_ELECTRIC"


def test_etl_layer_execution() -> None:
    """Validates ETL transformation, structural sorting, and data integrity."""
    etl = ETLLayer()
    df = etl.run_etl()

    # Checks type and minimum content size
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df) == 17  # Total number of models in raw dataset

    # Verifies if sorting by weight was correctly applied (ascending order)
    weights = df[VehicleSchema.WEIGHT_KG.value].tolist()
    assert weights == sorted(weights)

    # Ensures all required schema columns are present
    for column in VehicleSchema:
        assert column.value in df.columns
