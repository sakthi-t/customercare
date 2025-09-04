import gradio as gr
from agent.workflow import handle_query, identify_user

def intro(role, name, customer_id, email, history):
    msg = identify_user(role, name, customer_id, email)
    # Show as a bot/system message only
    history.append((None, msg))
    return history, history

def chat_interface(message, history):
    response = handle_query(message)
    history.append((message, response))
    return history, history

def build_ui():
    with gr.Blocks() as demo:
        gr.Markdown("## 🤖 Customer Support AI Agent")

        role = gr.Radio(["customer", "admin"], value="customer", label="Who are you?")
        name = gr.Textbox(label="Name")
        customer_id = gr.Textbox(label="Customer ID (for customers)", placeholder="Leave empty if admin")
        email = gr.Textbox(label="Email (for customers)", placeholder="Leave empty if admin")
        intro_btn = gr.Button("Introduce")

        # Explicitly stick to tuples to avoid the deprecation warning
        chatbot = gr.Chatbot(type="tuples")
        msg = gr.Textbox(placeholder="Ask about your orders...")
        clear = gr.Button("Clear")

        state = gr.State([])

        # intro takes 5 inputs, returns (chatbot, state)
        intro_btn.click(intro, [role, name, customer_id, email, state], [chatbot, state])

        # chat_interface takes (message, history), returns (chatbot, state)
        msg.submit(chat_interface, [msg, state], [chatbot, state])

        clear.click(lambda: ([], []), None, [chatbot, state])

    return demo
