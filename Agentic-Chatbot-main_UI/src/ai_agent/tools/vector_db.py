"""
Vector Database utilities for semantic search and retrieval.
"""

import faiss
import numpy as np
from typing import List, Dict, Any

class VectorDB:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []
        
    def add_documents(self, documents: List[str], embeddings: List[List[float]]):
        """Add documents and their embeddings to the vector database."""
        if len(documents) != len(embeddings):
            raise ValueError("Number of documents must match number of embeddings")
            
        # Convert embeddings to numpy array
        embeddings_array = np.array(embeddings).astype('float32')
        
        # Add to FAISS index
        self.index.add(embeddings_array)
        
        # Store documents
        self.documents.extend(documents)
        
    def search(self, query_embedding: List[float], k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        query_array = np.array([query_embedding]).astype('float32')
        
        # Search the index
        distances, indices = self.index.search(query_array, k)
        
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.documents):
                results.append({
                    "document": self.documents[idx],
                    "distance": float(distance),
                    "index": int(idx)
                })
                
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        return {
            "total_documents": len(self.documents),
            "index_size": self.index.ntotal,
            "dimension": self.dimension
        }
