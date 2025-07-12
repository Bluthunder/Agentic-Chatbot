from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def load_prompt(relative_path: str) -> str:
    """Reads and returns the contents of a prompt file."""
    try:
        # Get the root directory of the project
        base_dir = Path(__file__).resolve().parents[2]  # adjust depth based on structure
        prompt_path = base_dir / relative_path

        prompt_text = prompt_path.read_text()
        logger.debug(f"[PromptLoader] Loaded prompt from: {prompt_path}")
        return prompt_text

    except FileNotFoundError:
        logger.error(f"[PromptLoader] File not found: {relative_path}")
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    except Exception as e:
        logger.exception(f"[PromptLoader] Error reading prompt from {relative_path}: {e}")
        raise
