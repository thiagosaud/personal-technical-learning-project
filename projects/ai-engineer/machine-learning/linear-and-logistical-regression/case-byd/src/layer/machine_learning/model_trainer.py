"""
Model Pipeline Module [MACHINE LEARNING LAYER].
Handles creating, training, and testing Machine Learning algorithms.
"""

import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression

from src.config.schema.data.vehicle import VehicleSchema

# Type alias combining accepted estimator types for the pipeline
ModelEstimator = LinearRegression | LogisticRegression


class ModelTrainerLayer:
    """Manages training tasks and validation scores for multiple architectural use cases."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.df = data
        self.simple_linear_model: LinearRegression | None = None
        self.multiple_linear_model: LinearRegression | None = None
        self.logistic_model: LogisticRegression | None = None

    def _fit_regression[T: ModelEstimator](
        self, model_instance: T, feature_columns: list[VehicleSchema], target_column: VehicleSchema
    ) -> tuple[T, float]:
        """Unified private helper to initialize, fit, and score any regression model."""
        X = self.df[[col.value for col in feature_columns]]
        y = self.df[target_column.value]

        model = model_instance.fit(X, y)
        score = float(model.score(X, y))

        return model, score

    def train_models(self) -> dict[str, float]:
        """Creates, trains and tests models on the dataset, returning validation scores."""
        # Case 1: Simple Linear Regression (Weight vs. Consumption)
        self.simple_linear_model, r2_case1 = self._fit_regression(
            model_instance=LinearRegression(),
            feature_columns=[VehicleSchema.WEIGHT_KG],
            target_column=VehicleSchema.CONSUMPTION_MJ_KM,
        )

        # Case 2: Multiple Linear Regression (Weight + Horsepower vs. Acceleration)
        self.multiple_linear_model, r2_case2 = self._fit_regression(
            model_instance=LinearRegression(),
            feature_columns=[VehicleSchema.WEIGHT_KG, VehicleSchema.POWER_CV],
            target_column=VehicleSchema.ACCELERATION_FROM_0_TO_100,
        )

        # Case 3: Logistic Regression (Battery Size vs. Powertrain Classification)
        self.logistic_model, acc_case3 = self._fit_regression(
            model_instance=LogisticRegression(),
            feature_columns=[VehicleSchema.BATTERY_KWH],
            target_column=VehicleSchema.IS_PURE_ELECTRIC,
        )

        return {"case1_r2": r2_case1, "case2_r2": r2_case2, "case3_acc": acc_case3}
