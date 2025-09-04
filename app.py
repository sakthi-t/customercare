import gradio as gr
from frontend.ui import build_ui

if __name__ == "__main__":
    demo = build_ui()
    demo.launch()

