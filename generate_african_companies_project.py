#!/usr/bin/env python3
"""
African Companies Assistant Project Codebase Generator

Usage:
    python generate_african_companies_project.py --project-name my-africa-assistant

This script creates a standard codebase structure for the business data extraction and assistant project.
"""

import os
from pathlib import Path
import argparse


def create_file(path, content=""):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(description="Generate codebase for African Companies Assistant project.")
    parser.add_argument(
        "--project-name",
        required=True,
        help="Name of the project directory to create."
    )
    parser.add_argument(
        "--base-path",
        default=".",
        help="Base directory to create the project in (default: current directory)."
    )
    args = parser.parse_args()

    project_root = Path(args.base_path) / args.project_name
    dirs = [
        "src",
        "src/api",
        "src/data",
        "src/utils",
        "data/raw",
        "data/processed",
        "notebooks",
        "tests",
        "scripts",
    ]
    files = {
        "README.md": f"""# {args.project_name}\n\nAssistant to extract and answer questions about African companies.\n\n## Quick Start\n\n1. Install dependencies:\n   ```bash\n   pip install -r requirements.txt\n   ```\n2. Run the assistant:\n   ```bash\n   python src/assistant.py\n   ```\n\n## Project Structure\n\n- `src/` - Main source code\n- `data/` - Data storage\n- `notebooks/` - Jupyter notebooks\n- `tests/` - Unit tests\n- `scripts/` - Utility scripts\n\n## License\nMIT\n""",
        ".gitignore": "__pycache__/\n.env\n.venv/\ndata/\n*.pyc\n*.pkl\n*.log\n.ipynb_checkpoints/\n",
        "requirements.txt": "requests\nbeautifulsoup4\nopenai\npython-dotenv\nrich\n",
        ".env.example": "OPENAI_API_KEY=your_openai_api_key_here\n",
        "src/__init__.py": "",
        "src/scraper.py": '''"""
Web scraping logic for extracting company data.
"""
import requests
from bs4 import BeautifulSoup

# Add your scraping functions here
''',
        "src/assistant.py": '''"""
Console assistant for answering questions about African companies.
"""
from src.company_profiles import load_profiles

def main():
    profiles = load_profiles()
    print("Welcome to the African Companies Assistant! Type 'exit' to quit.")
    while True:
        question = input("Ask a question: ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        # Add logic to answer questions using profiles
        print("[Stub] Answering: ", question)

if __name__ == "__main__":
    main()
''',
        "src/company_profiles.py": '''"""
Data models and storage for company profiles.
"""
from typing import List, Dict

def load_profiles() -> List[Dict]:
    # Replace with actual loading logic
    return []
''',
        "src/data/__init__.py": "",
        "src/utils/__init__.py": "",
        "tests/__init__.py": "",
        "tests/test_assistant.py": '''"""
Unit tests for the assistant.
"""
def test_stub():
    assert True
''',
        "scripts/__init__.py": "",
    }

    # Create directories
    for d in dirs:
        (project_root / d).mkdir(parents=True, exist_ok=True)

    # Create files
    for rel_path, content in files.items():
        create_file(project_root / rel_path, content)

    print(f"✅ Project '{args.project_name}' created at {project_root.resolve()}")
    print("Next steps:")
    print(f"  cd {args.project_name}")
    print("  pip install -r requirements.txt")
    print("  cp .env.example .env")
    print("  # Edit .env with your OpenAI API key")
    print("  python src/assistant.py")


if __name__ == "__main__":
    main() 