import gradio as gr
from agent import agent_chat



def respond(message, chat_history):
    if chat_history is None:
        chat_history = []

    # 从历史中获取上一轮推荐的商品（如果存在）
    last_products = None
    if chat_history and isinstance(chat_history[-1], dict) and "products" in chat_history[-1]:
        last_products = chat_history[-1]["products"]

    result = agent_chat(message, chat_history, last_products)

    chat_history.append({"role": "user", "content": message})
    chat_history.append({
        "role": "assistant",
        "content": result["reply"],
        "products": result["products"]
    })
    return "", chat_history



with gr.Blocks(title="AI购物Agent（百炼版）") as demo:
    gr.Markdown("# 🛍️ AI购物Agent（百炼版）")
    chatbot = gr.Chatbot(height=500)
    msg = gr.Textbox(label="输入需求")
    btn = gr.Button("发送")
    clear = gr.Button("清空对话")

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    btn.click(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: [], None, chatbot)

if __name__ == "__main__":
    demo.launch(server_port=7860)