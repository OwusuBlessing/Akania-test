"""
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
