import chromadb
from chromadb.config import Settings
from typing import Dict, List, Optional
from pathlib import Path

def discover_chroma_backends() -> Dict[str, Dict[str, str]]:
    """Discover available ChromaDB backends in the project directory"""
    backends = {}
    current_dir = Path(".")
    
   # Find directories beginning with "chroma"
    chroma_dirs = [
        d for d in current_dir.iterdir()
        if d.is_dir() and d.name.startswith("chroma")
    ]
   for directory in chroma_dirs:
        try:
            client = chromadb.PersistentClient(
                path=str(directory),
                settings=Settings(anonymized_telemetry=False)
            )
            collections = client.list_collections()
            for collection in collections:
                key = f"{directory.name}_{collection.name}"
                try:
                    count = collection.count()
                except Exception:
                    count = "Unknown"
                backends[key] = {
                    "directory": str(directory),
                    "collection_name": collection.name,
                    "display_name": f"{directory.name} → {collection.name} ({count} docs)"
                }
        except Exception as e:
            key = directory.name
            backends[key] = {
                "directory": str(directory),
                "collection_name": "",
                "display_name": f"{directory.name} (Error: {str(e)[:40]})"
            }

    return backends

def initialize_rag_system(chroma_dir: str, collection_name: str):
    """Initialize the RAG system with specified backend (cached for performance)"""

    # TODO: Create a chomadb persistentclient
    # TODO: Return the collection with the collection_name
    try:
        client = chromadb.PersistentClient(
            path=chroma_dir,
            settings=Settings(anonymized_telemetry=False)
        )
        collection = client.get_collection(collection_name)
        return collection, True, None
    except Exception as e:
        return None, False, str(e)

def retrieve_documents(collection, query: str, n_results: int = 3, 
                      mission_filter: Optional[str] = None) -> Optional[Dict]:
    """Retrieve relevant documents from ChromaDB with optional filtering"""

    # TODO: Initialize filter variable to None (represents no filtering)

    # TODO: Check if filter parameter exists and is not set to "all" or equivalent
    # TODO: If filter conditions are met, create filter dictionary with appropriate field-value pairs

    # TODO: Execute database query with the following parameters:
        # TODO: Pass search query in the required format
        # TODO: Set maximum number of results to return
        # TODO: Apply conditional filter (None for no filtering, dictionary for specific filtering)

    # TODO: Return query results to caller
    where = None

    if mission_filter and mission_filter.lower() != "all":
        where = {"mission": mission_filter}

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where
    )

    return results

def format_context(documents: List[str], metadatas: List[Dict]) -> str:
    """Format retrieved documents into context"""
    if not documents:
        return ""
    
    # TODO: Initialize list with header text for context section

    # TODO: Loop through paired documents and their metadata using enumeration
        # TODO: Extract mission information from metadata with fallback value
        # TODO: Clean up mission name formatting (replace underscores, capitalize)
        # TODO: Extract source information from metadata with fallback value  
        # TODO: Extract category information from metadata with fallback value
        # TODO: Clean up category name formatting (replace underscores, capitalize)
        
        # TODO: Create formatted source header with index number and extracted information
        # TODO: Add source header to context parts list
        
        # TODO: Check document length and truncate if necessary
        # TODO: Add truncated or full document content to context parts list

    # TODO: Join all context parts with newlines and return formatted string
    if not documents:
        return ""

    context_parts = ["Relevant NASA Documents:\n"]

    for i, (doc, metadata) in enumerate(zip(documents, metadatas), start=1):

        mission = metadata.get("mission", "Unknown").replace("_", " ").title()
        source = metadata.get("source", "Unknown")
        category = metadata.get(
            "document_category",
            "General"
        ).replace("_", " ").title()

        context_parts.append(
            f"[Source {i}] "
            f"Mission: {mission} | "
            f"Category: {category} | "
            f"File: {source}"
        )

        if len(doc) > 1200:
            context_parts.append(doc[:1200] + "...\n")
        else:
            context_parts.append(doc + "\n")

    return "\n".join(context_parts)    
