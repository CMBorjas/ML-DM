import gradio as gr
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# Initialize the chat model (e.g., OpenAI GPT or other language model)
chat_model = ChatOpenAI(temperature=0.7)

# Define a prompt template for generating NPC stats or responding to chat
npc_prompt = PromptTemplate(
    input_variables=["npc_name", "context"],
    template="""
    Create detailed stats for an NPC named {npc_name}.
    Context: {context}.
    Use Dungeons & Dragons style with armor class, hit points, abilities, saving throws, actions, and reactions.
    """
)

# Chat function for NPC generation
def generate_npc(npc_name, context):
    prompt = npc_prompt.format(npc_name=npc_name, context=context)
    response = chat_model.generate([prompt])
    return response[0]["text"]

# Gradio interface
def create_gradio_chat_interface():
    with gr.Blocks() as interface:
        gr.Markdown("# Dungeon Master Assistant AI Chat")
        with gr.Row():
            npc_name = gr.Textbox(label="NPC Name", placeholder="e.g., Dwarf Graveslayer")
            context = gr.Textbox(label="Context", placeholder="e.g., undead-slaying warrior, elite group")
        with gr.Row():
            response = gr.TextArea(label="AI Response")
        with gr.Row():
            generate_button = gr.Button("Generate NPC")
        generate_button.click(generate_npc, inputs=[npc_name, context], outputs=response)
    return interface
