"""
Handbook indexer for RAG pipeline using FAISS vector store.
Indexes handbook content for similarity search with caching.
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

class HandbookIndex:
    def __init__(self, 
                 model_name: str = "all-MiniLM-L6-v2",
                 cache_dir: str = "cache"):
        self.encoder = SentenceTransformer(model_name)
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Initialize FAISS index
        self.dimension = self.encoder.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(self.dimension)
        
        # Store text chunks for retrieval
        self.texts: List[str] = []
        self.is_built = False

    def _get_cache_path(self, handbook_dir: str) -> Path:
        """Generate cache file path based on content hash"""
        content_hash = self._hash_directory(handbook_dir)
        return self.cache_dir / f"handbook_index_{content_hash}.npz"

    def _hash_directory(self, directory: str) -> str:
        """Create hash of directory contents for cache validation"""
        hasher = hashlib.sha256()
        
        for root, _, files in os.walk(directory):
            for filename in sorted(files):
                if filename.endswith('.md'):
                    file_path = os.path.join(root, filename)
                    with open(file_path, 'rb') as f:
                        hasher.update(f.read())
                        
        return hasher.hexdigest()[:12]

    def build(self, handbook_dir: str, force: bool = False) -> None:
        """Build or load index from handbook markdown files"""
        if self.is_built and not force:
            return

        cache_path = self._get_cache_path(handbook_dir)
        
        # Try loading from cache first
        if not force and cache_path.exists():
            cached = np.load(cache_path, allow_pickle=True)
            self.texts = cached['texts'].tolist()
            vectors = cached['vectors']
            self.index.add(vectors)
            self.is_built = True
            return

        # Process handbook files
        self.texts = []
        vectors = []
        
        for file_path in tqdm(list(Path(handbook_dir).glob("*.md"))):
            with open(file_path) as f:
                content = f.read()
                
            # Split into chunks (simple paragraph splitting for now)
            chunks = [c.strip() for c in content.split('\n\n') if c.strip()]
            
            # Encode chunks
            chunk_vectors = self.encoder.encode(chunks)
            
            vectors.append(chunk_vectors)
            self.texts.extend(chunks)

        # Combine all vectors
        vectors = np.vstack(vectors)
        
        # Add to FAISS index
        self.index.add(vectors)
        
        # Save cache
        np.savez(cache_path,
                 texts=np.array(self.texts),
                 vectors=vectors)
        
        self.is_built = True

    def search(self, query: str, k: int = 3) -> List[str]:
        """Search for most relevant text chunks"""
        if not self.is_built:
            raise RuntimeError("Index not built. Call build() first.")
            
        # Encode query
        query_vector = self.encoder.encode([query])
        
        # Search
        distances, indices = self.index.search(query_vector, k)
        
        # Return relevant texts
        return [self.texts[idx] for idx in indices[0]]

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--handbook-dir", default="handbook",
                       help="Directory containing handbook markdown files")
    parser.add_argument("--force", action="store_true",
                       help="Force rebuild index ignoring cache")
    parser.add_argument("--query", help="Optional query to test search")
    args = parser.parse_args()

    # Build index
    index = HandbookIndex()
    index.build(args.handbook_dir, force=args.force)
    
    # Test search if query provided
    if args.query:
        results = index.search(args.query)
        print("\nSearch results:")
        for i, text in enumerate(results, 1):
            print(f"\n{i}. {text}")

if __name__ == "__main__":
    main()
