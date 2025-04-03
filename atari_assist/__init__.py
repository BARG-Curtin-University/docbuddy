"""Atari Assist - A CLI and web assistant for Atari 2600 development.

This package provides functionality to ask questions about Atari 2600 development 
using different LLM backends.
"""

from atari_assist.core import ask_question, preview_matches

__version__ = "0.1.0"
__all__ = ["ask_question", "preview_matches"]
