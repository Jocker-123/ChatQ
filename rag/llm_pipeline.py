from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
import os


use_model: int = 0
# model 0
llm_mistral = Ollama(model="mistral", temperature=0.2)

# model 1
llm_openai = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=400,
    timeout=None,
    max_retries=2,
    api_key=os.getenv("OPENAI_API_KEY", "key")
)


def run_rag_pipeline(query, vector_results, elastic_results, web_results):
    prompt = ChatPromptTemplate.from_template("""
You are an assistant helping with research.

User wants to know: {query}
------------------------------
The following are additional information, use it only if it relevant. Else ignore for response.
Vector DB results: {vector_data}
ElasticSearch results: {elastic_data}
Web Search:{web_data}
""")

    messages = prompt.format_messages(
        query=query,
        vector_data="\n".join(vector_results),
        elastic_data="\n".join(elastic_results),
        web_data="\n".join(web_results),
    )
    return llm(messages)


def llm(prompt):
    if use_model == 1:
        return llm_openai(prompt).content
    else:
        # default model
        return llm_mistral(prompt[0].content)
