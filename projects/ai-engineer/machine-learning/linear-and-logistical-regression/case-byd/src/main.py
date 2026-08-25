"""
Main Application Entry Point.
Coordinates pipelines execution and prints analytical telemetry results.
"""

import logging
from typing import Final

from src.layer.data.etl import ETLLayer
from src.layer.machine_learning.model_trainer import ModelTrainerLayer
from src.layer.visualizer.model_visualizer import ModelVisualizerLayer

# Configure standard enterprise logging infrastructure to replace print() natively
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger: Final[logging.Logger] = logging.getLogger(__name__)


def main() -> None:
    """Main orchestrator execution lifecycle."""
    logger.info("Initializing Data Engineering Pipeline [ETL]...")
    etl_pipeline = ETLLayer()
    processed_df = etl_pipeline.run_etl()

    logger.info("\nInitializing Machine Learning Modeling Pipeline [ML]...")
    ml_pipeline = ModelTrainerLayer(processed_df)
    metrics = ml_pipeline.train_models()

    logger.info("\n======================= TELEMETRY PERFORMANCE REPORT =======================")
    logger.info(">> Case 1 (Simple Linear Model)    | Training R² Score: %.4f", metrics["case1_r2"])
    logger.info(">> Case 2 (Multiple Linear Model)  | Training R² Score: %.4f", metrics["case2_r2"])
    logger.info(">> Case 3 (Logistic Classifier)     | Validation Accuracy: %.4f", metrics["case3_acc"])
    logger.info("============================================================================\n")
    logger.info("Initializing Analytics Graphics Generation Frontend [VISUALIZER]...")

    # ==========================================
    # TYPE NARROWING GUARD CLAUSES
    # ==========================================
    # Verifies that models are present to safely eliminate the "LinearRegression | None" type mismatch
    if ml_pipeline.simple_linear_model is None:
        raise ValueError("Simple linear model instance payload is missing.")

    if ml_pipeline.multiple_linear_model is None:
        raise ValueError("Multiple linear model instance payload is missing.")

    if ml_pipeline.logistic_model is None:
        raise ValueError("Logistic classification engine payload is missing.")

    reporter = ModelVisualizerLayer(processed_df)
    reporter.generate_case1_plot(ml_pipeline.simple_linear_model, metrics["case1_r2"])
    reporter.generate_case2_plot(ml_pipeline.multiple_linear_model, metrics["case2_r2"])
    reporter.generate_case3_plot(ml_pipeline.logistic_model, metrics["case3_acc"])

    logger.info("\nPipeline executed successfully with zero errors. Architecture validated.")


if __name__ == "__main__":
    main()
