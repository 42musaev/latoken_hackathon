import argparse
import os

import openai
# from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


# def generate_gpt_response(user_text, model_name="GPT-4o"):
#     import os
#     from openai import OpenAI
#
#     client = OpenAI(
#         api_key=os.environ.get("OPENAI_API_KEY"),
#     )
#
#     chat_completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": user_text,
#             }
#         ],
#         model=model_name,
#     )
#     return chat_completion.choices[0].message.content


def generate_local_response(query_text: str):
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")

    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.7:
        # return generate_gpt_response(query_text)
        return "Пока нет доступа к ЧАТГПТ ВИКА) (лимит кончился)"
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = ChatOpenAI()
    response_text = model.predict(prompt)

    return response_text
