import httpx
import sys

BASE_URL = "http://127.0.0.1:8000/api/repositories"
REPO_ID = "repo_78a739"  # from the user's chunks.json

def test_retrieval():
    query = "How does authentication work?"
    print(f"Testing retrieval for query: '{query}'")
    
    # Test 1: Search Endpoint
    print("\n--- Testing /search Endpoint ---")
    r = httpx.post(f"{BASE_URL}/{REPO_ID}/search", json={"query": query}, timeout=120.0)
    if r.status_code != 200:
        print("Failed search:", r.text)
    else:
        results = r.json().get("results", [])
        print(f"Found {len(results)} relevant chunks.")
        for chunk in results:
            print(f"- {chunk['file_path']} (Score: {chunk['similarity_score']:.4f})")
            
    # Test 2: Context Endpoint
    print("\n--- Testing /context Endpoint ---")
    r = httpx.post(f"{BASE_URL}/{REPO_ID}/context", json={"query": query}, timeout=120.0)
    if r.status_code != 200:
        print("Failed context:", r.text)
    else:
        data = r.json()
        context = data.get("context", "")
        sources = data.get("sources", [])
        print(f"Context length: {len(context)} characters")
        print("Sources extracted:")
        for source in sources:
            print(f"- {source['file_path']}")
            
        print("\nContext Preview (first 500 chars):")
        print(context[:500] + "..." if len(context) > 500 else context)
        
    print("\nSUCCESS: Retrieval layer is fully functional!")

if __name__ == "__main__":
    test_retrieval()
