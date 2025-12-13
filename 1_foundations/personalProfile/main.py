"""
Main entry point for the personal profile chatbot.
Launches a Gradio web interface for interacting with the chatbot.
"""
import gradio as gr
from logging import getLogger, basicConfig, INFO

from chatbot import create_chat_function
from personal_data import NAME

# Configure logging
basicConfig(level=INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = getLogger(__name__)


def main():
    """Main function to launch the Gradio chatbot interface."""
    logger.info(f"Starting personal profile chatbot for {NAME}")
    
    # Create the chat function
    chat = create_chat_function(name=NAME)
    
    # Launch Gradio interface
    interface = gr.ChatInterface(
        chat,
        title=f"{NAME}'s Personal Chatbot",
        description=f"Chat with {NAME}'s AI representative. Ask questions about career, background, skills, and experience.",
    )
    
    interface.launch(share=False)


if __name__ == "__main__":
    main()