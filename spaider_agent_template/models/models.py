from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


def build_oai_llm():
    return ChatOpenAI(verbose=True)


# simply input the model name from groq and it will return the llm
def build_groq_llm(model_name):
    return ChatGroq(
        model=model_name,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
