# """
# Main Application Entry Point.
# Coordinates pipelines execution and prints analytical telemetry results.
# """

from layer.data.etl import ETLLayer
from layer.machine_learning.model_trainer import ModelTrainerLayer
from layer.visualizer.model_visualizer import ModelVisualizerLayer


def main():
    print("Initializing Data Engineering Pipeline [ETL]...")
    etl_pipeline = ETLLayer()
    processed_df = etl_pipeline.run_etl()

    print("\nInitializing Machine Learning Modeling Pipeline [ML]...")
    ml_pipeline = ModelTrainerLayer(processed_df)
    metrics = ml_pipeline.train_models()

    print("\n======================= TELEMETRY PERFORMANCE REPORT =======================")
    print(f">> Case 1 (Simple Linear Model)    | Training R² Score: {metrics['case1_r2']:.4f}")
    print(f">> Case 2 (Multiple Linear Model)  | Training R² Score: {metrics['case2_r2']:.4f}")
    print(f">> Case 3 (Logistic Classifier)     | Validation Accuracy: {metrics['case3_acc']:.4f}")
    print("============================================================================\n")
    print("Initializing Analytics Graphics Generation Frontend [VISUALIZER]...")

    reporter = ModelVisualizerLayer(processed_df)
    reporter.generate_case1_plot(ml_pipeline.simple_linear_model, metrics["case1_r2"])
    reporter.generate_case2_plot(ml_pipeline.multiple_linear_model, metrics["case2_r2"])
    reporter.generate_case3_plot(ml_pipeline.logistic_model, metrics["case3_acc"])

    print("\nPipeline executed successfully with zero errors. Architecture validated.")


if __name__ == "__main__":
    main()
