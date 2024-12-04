import unittest
from app.routes import talk_to_npc_gradio

class TestGradioIntegration(unittest.TestCase):
    def test_gradio_interface(self):
        response = talk_to_npc_gradio("Azaavara Minstrel")
        self.assertIn("http://127.0.0.1:7860", response, "Gradio interface should launch successfully.")

if __name__ == "__main__":
    unittest.main()
