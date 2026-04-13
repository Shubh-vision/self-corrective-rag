
def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)


def summarize_chat(question, answer):
    return f"User: {question} | AI: {answer[:100]}"