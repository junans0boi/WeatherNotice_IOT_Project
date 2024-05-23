import getpass
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyBZfOhQ0aVyQllnUIGB4KbTlUZZRVE8mVQ"

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

model = ChatGoogleGenerativeAI(model="gemini-pro")
output_parser = StrOutputParser()

chain = model | output_parser

dick = chain.invoke("응~니얼굴~")
print(dick)