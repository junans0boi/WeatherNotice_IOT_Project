import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

def set_api_key():
    os.environ["GOOGLE_API_KEY"] = "AIzaSyBZfOhQ0aVyQllnUIGB4KbTlUZZRVE8mVQ"


def get_llm_answer(prompt: str) -> str:
    model = ChatGoogleGenerativeAI(model="gemini-pro")
    output_parser = StrOutputParser()
    chain = ChatGoogleGenerativeAI(model="gemini-pro") | output_parser
    return chain.invoke(prompt)

if __name__ == "__main__":
    set_api_key()
    answer = get_llm_answer("응~니얼굴~")
    print(answer)
