import chromadb
from chromadb.config import Settings
import uuid

class VectorMemory:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Oyun hafızası için koleksiyon. Cosine similarity metin tabanlı RAG için idealdir.
        self.collection = self.client.get_or_create_collection(
            name="campaign_memory",
            metadata={"hnsw:space": "cosine"} 
        )

    def add_memory(self, campaign_id: str, memory_text: str, event_type: str = "dialogue", metadata: dict = None):
        """
        Geçmiş oturum verilerini vektör veritabanına ekler.
        event_type: 'dialogue', 'lore', 'combat_summary'
        """
        if metadata is None:
            metadata = {}
        
        # Filtreleme yapabilmek için metadata içine campaign_id ve type ekleniyor
        metadata["campaign_id"] = str(campaign_id)
        metadata["event_type"] = event_type

        self.collection.add(
            documents=[memory_text],
            metadatas=[metadata],
            ids=[str(uuid.uuid4())]
        )

    def query_memory(self, campaign_id: str, query_text: str, n_results: int = 3, event_type: str = None):
        """
        RAG sistemi için bağlama uygun geçmiş kayıtları çeker.
        """
        where_clause = {"campaign_id": str(campaign_id)}
        if event_type:
            where_clause["event_type"] = event_type # Sadece lore veya sadece diyalog aranabilir

        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where_clause
        )
        
        return results["documents"][0] if results["documents"] else []

# Global bir instance oluşturup projede kullanılabilir
memory_db = VectorMemory()