
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="atari-assist",
    version="0.1.0",
    description="CLI and web assistant for Atari 2600 development using LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Atari Assist Contributors",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/atari-assist",
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
        "python-dotenv"
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
            "atari-assist-web=atari_assist.web.app:serve_app"
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
    keywords="atari, 2600, llm, assistant, cli, web, rag",
)

