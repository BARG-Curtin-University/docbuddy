
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="docbuddy",
    version="0.1.0",
    description="CLI and web assistant for document collections using LLMs and RAG",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="DocBuddy Contributors",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/docbuddy",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        "typer[all]",
        "rich",
        "openai",
        "requests",
        "anthropic",
        "google-generativeai",
        "groq",
        "python-fasthtml",
        "python-dotenv",
        "textual>=0.52.1"
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "ruff",
            "black",
            "mypy",
        ],
        "embeddings": [
            "numpy",
            "sentence-transformers",
        ],
        "full": [
            "numpy",
            "sentence-transformers", 
            "pytest",
            "pytest-cov",
            "ruff",
            "black",
            "mypy",
        ]
    },
    entry_points={
        "console_scripts": [
            "atari-assist=atari_assist.cli.main:app",
            "atari-assist-web=atari_assist.web.app:serve_app",
            "docbuddy=docbuddy.cli.main:app"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="rag, llm, assistant, cli, web, documentation, chat, knowledge base",
)

