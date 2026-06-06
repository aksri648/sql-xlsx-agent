import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.embeddings import Embeddings
import os
from typing import Any


class SimpleEmbeddings(Embeddings):
    def __init__(self):
        self.llm = ChatGroq(
            model="qwen/qwen3-32b",
            api_key=os.getenv("GROQ_API_KEY"),
        )

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] * 768 for _ in texts]

    def embed_query(self, text: str) -> list[float]:
        return [0.0] * 768


class ChromaManager:
    def __init__(self):
        self.client = chromadb.Client(Settings(
            chroma_api_impl="rest",
            chroma_server_host=os.getenv("CHROMA_HOST", "localhost"),
            chroma_server_http_port=int(os.getenv("CHROMA_PORT", 8000)),
            chroma_api_key=os.getenv("CHROMA_API_KEY"),
        ))
        self.embeddings = SimpleEmbeddings()

    def create_collections(self):
        collections = ["schemas", "documentation", "glossary", "query_examples"]
        for name in collections:
            self.client.get_or_create_collection(name=name)

    def add_schema(self, schema_data: dict, metadata: dict):
        collection = self.client.get_collection("schemas")
        collection.add(
            documents=[str(schema_data)],
            metadatas=[metadata],
            ids=[metadata.get("id", f"schema_{hash(str(schema_data))}")],
        )

    def add_documentation(self, doc_data: str, metadata: dict):
        collection = self.client.get_collection("documentation")
        collection.add(
            documents=[doc_data],
            metadatas=[metadata],
            ids=[metadata.get("id", f"doc_{hash(doc_data)}")],
        )

    def add_glossary(self, term: str, definition: str, metadata: dict):
        collection = self.client.get_collection("glossary")
        collection.add(
            documents=[f"{term}: {definition}"],
            metadatas=[metadata],
            ids=[metadata.get("id", f"glossary_{hash(term)}")],
        )

    def add_query_example(self, query: str, description: str, metadata: dict):
        collection = self.client.get_collection("query_examples")
        collection.add(
            documents=[f"{query} - {description}"],
            metadatas=[metadata],
            ids=[metadata.get("id", f"query_{hash(query)}")],
        )

    def retrieve(self, collection_name: str, query: str, top_k: int = 10) -> list[dict]:
        collection = self.client.get_collection(collection_name)
        results = collection.query(
            query_texts=[query],
            n_results=top_k,
        )

        retrieved = []
        if results and results.get("documents"):
            for i, doc in enumerate(results["documents"]):
                retrieved.append({
                    "content": doc,
                    "metadata": results["metadatas"][i] if i < len(results.get("metadatas", [[]])) else {},
                })

        return retrieved

    def get_relevant_context(self, query: str, top_k: int = 10) -> list[dict]:
        all_context = []

        for collection_name in ["schemas", "documentation", "glossary", "query_examples"]:
            try:
                results = self.retrieve(collection_name, query, top_k)
                all_context.extend(results)
            except Exception:
                pass

        return all_context[:top_k]