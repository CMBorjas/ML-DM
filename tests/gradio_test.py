import gradio as gr

def test_function(input_text):
    return f"Input: {input_text}"

gr.Interface(
    fn=test_function, inputs="text", outputs="text"
).launch(server_name="127.0.0.1", server_port=7860)
