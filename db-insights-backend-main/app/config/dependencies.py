from crewai.llm import LLM
from app import settings

def get_llm():
    llm = LLM(
        model=settings.azure_openai_deployment,
        base_url=settings.azure_openai_endpoint,
        api_version=settings.azure_openai_version,
        api_key=settings.azure_openai_api_key,
        temperature=0.1,        
    )

    

    return llm
