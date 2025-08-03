from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

MODEL = "llama3:instruct"
OLLAMA_URL = "http://localhost:11434"

llm = Ollama(model=MODEL, base_url=OLLAMA_URL)

prompt = ChatPromptTemplate.from_template("""
You are a legal assistant trained in Indian contract law.
Create a fair, clear, and legally sound contract based on this conversation:

--------------------
{conversation}
--------------------

Ensure the contract:
- Uses appropriate legal terms
- Is unbiased and professional
- Includes section headings
- Avoids ambiguity

Respond only with the contract. No explanation needed.
""")

chain: Runnable = prompt | llm

def generate_contract(conversation: str) -> str:
    return chain.invoke({"conversation": conversation})
