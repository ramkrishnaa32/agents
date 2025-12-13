"""
Load and manage personal data (LinkedIn PDF and summary).
"""
from pathlib import Path
from PyPDF2 import PdfReader
from logging import getLogger

logger = getLogger(__name__)

# Path to personal data files (relative to this module)
BASE_DIR = Path(__file__).parent.parent
LINKEDIN_PDF_PATH = BASE_DIR / "me" / "linkedin.pdf"
SUMMARY_TXT_PATH = BASE_DIR / "me" / "summary.txt"

# Default name
NAME = "KR Achary"


def load_linkedin_profile() -> str:
    """
    Load LinkedIn profile text from PDF file.
    
    Returns:
        String containing all text from the LinkedIn PDF
    
    Raises:
        FileNotFoundError: If the LinkedIn PDF file is not found
    """
    if not LINKEDIN_PDF_PATH.exists():
        raise FileNotFoundError(f"LinkedIn PDF not found at: {LINKEDIN_PDF_PATH}")
    
    linkedin = ""
    reader = PdfReader(str(LINKEDIN_PDF_PATH))
    for page in reader.pages:
        text = page.extract_text()
        if text:
            linkedin += text
    
    logger.info(f"Loaded LinkedIn profile ({len(linkedin)} characters)")
    return linkedin


def load_summary() -> str:
    """
    Load summary text from file.
    
    Returns:
        String containing the summary text
    
    Raises:
        FileNotFoundError: If the summary file is not found
    """
    if not SUMMARY_TXT_PATH.exists():
        raise FileNotFoundError(f"Summary file not found at: {SUMMARY_TXT_PATH}")
    
    with open(SUMMARY_TXT_PATH, "r", encoding="utf-8") as f:
        summary = f.read()
    
    logger.info(f"Loaded summary ({len(summary)} characters)")
    return summary


def get_system_prompt(name: str = NAME) -> str:
    """
    Generate the system prompt for the chatbot.
    
    Args:
        name: The name of the person the chatbot represents
    
    Returns:
        Complete system prompt string
    """
    try:
        summary = load_summary()
        linkedin = load_linkedin_profile()
    except FileNotFoundError as e:
        logger.error(f"Error loading personal data: {e}")
        raise
    
    system_prompt = (
        f"You are acting as {name}. You are answering questions on {name}'s website, "
        f"particularly questions related to {name}'s career, background, skills and experience. "
        f"Your responsibility is to represent {name} for interactions on the website as faithfully as possible. "
        f"You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. "
        f"Be professional and engaging, as if talking to a potential client or future employer who came across the website. "
        f"If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. "
        f"If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "
    )
    
    system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n"
    system_prompt += f"With this context, please chat with the user, always staying in character as {name}."
    
    return system_prompt

