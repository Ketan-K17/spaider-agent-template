from langchain_groq import ChatGroq

def BuildChatGroq(model: str, temperature: float):
    return ChatGroq(model=model, temperature=temperature)
