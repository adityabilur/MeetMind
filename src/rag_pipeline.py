from src.vector_store import search_documents
from src.gemini_service import ask_gemini


def answer_question(question, chat_history=None):

    if chat_history is None:
        chat_history = []

    # -----------------------------
    # Step 1: Build conversation context
    # -----------------------------

    conversation_context = ""

    for message in chat_history[-6:]:

        if message["role"] == "user":
            conversation_context += (
                f"User: {message['content']}\n"
            )

        elif message["role"] == "assistant":
            conversation_context += (
                f"MeetMind: {message['content']}\n"
            )

    # -----------------------------
    # Step 2: Create retrieval query
    # -----------------------------

    retrieval_query = f"""
Previous conversation:
{conversation_context}

Current question:
{question}
"""

    # -----------------------------
    # Step 3: Search ChromaDB
    # -----------------------------

    results = search_documents(
        retrieval_query,
        n_results=3
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # -----------------------------
    # Step 4: Build transcript context
    # -----------------------------

    context = "\n\n".join(documents)

    # -----------------------------
    # Step 5: Ask Gemini
    # -----------------------------

    prompt = f"""
You are MeetMind, an AI audio and video intelligence assistant.

Answer the user's current question using ONLY the
provided transcript context.

You may also use the previous conversation to understand
what the user is referring to.

If the answer is not present in the transcript context,
say:

"I could not find this information in the content."

Previous conversation:
{conversation_context}

Relevant transcript context:
{context}

Current user question:
{question}

Give a clear and concise answer.
"""

    answer = ask_gemini(prompt)

    return answer, documents, metadatas