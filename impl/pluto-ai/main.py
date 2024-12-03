
import asyncio
from agents import aggregator, twitter_poster
from agency.agency import Agency
# from llama_parse import LlamaParse
# from llama_index.llms.ollama import Ollama

# from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# from huggingface_hub import HfFolder

# token = HfFolder.get_token()


async def main():
    
    # LLAMA_CLOUD_API_KEY =  "llx-owzYtE9Fic0pVNqgf5Ni7WzxFeGB6snsqFWNvm1Xw6xs3DLe"


    # hf_token = HfFolder.get_token()

    # print(f"HF Token: {token}")

    # llm = Ollama(model="artifish/llama3.2-uncensored", request_timeout=30.0)

    # print(f"LLM : {llm}")

    # parser = LlamaParse(result_type="markdown", api_key=LLAMA_CLOUD_API_KEY)

    # file_extractor = {".pdf": parser}

    # documents = SimpleDirectoryReader("./data", file_extractor=file_extractor).load_data()

    # # Use a Hugging Face embedding model
    # embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # vector_index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)

    # query_engine = vector_index.as_query_engine(llm=llm)

    # result = query_engine.query("who is the arthor of the book and what is it about?")
    # print(result)

    agency = Agency([aggregator,twitter_poster])

    resp = await agency.run()

    print(f"Response from Agency: {resp}")

if __name__ == "__main__":
    asyncio.run(main())
