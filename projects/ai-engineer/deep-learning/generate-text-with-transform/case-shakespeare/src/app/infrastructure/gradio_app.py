"""Optional local Gradio interface for interactive text generation."""

import sys
from pathlib import Path

import gradio as gr

from src.app.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def create_interface() -> gr.Interface:
    """Create the Gradio app that calls the generation pipeline."""
    pipeline = Pipeline()

    # Define a function to generate text using the pipeline with the provided parameters.
    def generate_text(prompt: str, temperature: float, top_k: int, num_tokens: int) -> str:
        """Generate text using the pipeline with the provided parameters."""
        return pipeline.generate(
            prompt=prompt,
            temperature=temperature,
            top_k=int(top_k),
            num_tokens=int(num_tokens),
            interactive=False,
        )

    # Create the Gradio interface with input fields and output display.
    demo = gr.Interface(
        fn=generate_text,
        inputs=[
            gr.Textbox(lines=3, label="Prompt", value="To be, or not to be"),
            gr.Slider(0.4, 1.3, value=0.75, step=0.05, label="Temperature"),
            gr.Slider(10, 100, value=40, step=5, label="Top-k"),
            gr.Slider(50, 500, value=200, step=10, label="Tokens"),
        ],
        outputs=gr.Textbox(lines=12, label="Generated Text"),
        title="Shakespeare Transformer",
        description="Generate text in the style of William Shakespeare.",
        flagging_mode="never",
    )

    return demo


# Launch the Gradio app if this script is run directly.
if __name__ == "__main__":
    app = create_interface()
    app.launch()
