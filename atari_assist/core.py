from atari_assist.llm import get_llm
from atari_assist.utils import load_documents, get_best_chunks, build_prompt

SOURCE_DIR = "atari_docs"

def ask_question(question: str, model: str = "openai"):
    docs = load_documents(SOURCE_DIR)
    chunks = get_best_chunks(docs, question)
    prompt = build_prompt(chunks, question)
    llm = get_llm(model)
    return llm.ask(prompt)

def preview_matches(question: str, top_n: int = 4):
    docs = load_documents(SOURCE_DIR)
    chunks = get_best_chunks(docs, question, top_n)
    return [(c["filename"], c["content"][:200]) for c in chunks]
