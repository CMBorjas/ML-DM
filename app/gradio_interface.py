import os
import gradio as gr
import warnings
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Ignore deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Initialize your model
chat_model = ChatOpenAI(
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Define the prompt for the model
npc_prompt = PromptTemplate(
    input_variables=["npc_name", "context"],
    template="""
    Create stats for an NPC named {npc_name}.
    Context: {context}.
    Provide detailed stats including actions, saving throws, hit points, etc., formatted as in D&D style.
    """
)

# Function to generate NPC stats
def generate_npc(npc_name, context):
    prompt = npc_prompt.format(npc_name=npc_name, context=context)
    response = chat_model.generate([prompt])
    return response[0]['text']

# Gradio interface
def create_gradio_interface():
    with gr.Blocks() as interface:
        gr.Markdown("# Dungeon Master AI Assistant")
        with gr.Row():
            npc_name = gr.Textbox(label="NPC Name", placeholder="Enter NPC name (e.g., 'Dwarf Graveslayer')")
            context = gr.Textbox(label="Context", placeholder="Enter context (e.g., 'an elite undead-slaying warrior')")
        with gr.Row():
            output = gr.TextArea(label="Generated NPC Stats", interactive=False)
        with gr.Row():
            generate_button = gr.Button("Generate NPC")
        generate_button.click(generate_npc, inputs=[npc_name, context], outputs=output)
    return interface

# Create and launch the Gradio app
if __name__ == "__main__":
    interface = create_gradio_interface()
    interface.launch(share=False, server_name="0.0.0.0", server_port=7860)
