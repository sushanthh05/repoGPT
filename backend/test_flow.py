import httpx
import time
import sys

BASE_URL = "http://127.0.0.1:8000/api/repositories"

def test_flow():
    # 1. Analyze
    print("Analyzing repository...")
    r = httpx.post(f"{BASE_URL}/analyze", json={"repo_url": "https://github.com/sindresorhus/ky"})
    if r.status_code != 200:
        print("Failed analyze:", r.text)
        sys.exit(1)
    
    repo_id = r.json()["repository_id"]
    print(f"Repository ID: {repo_id}")

    # 2. Parse
    print("Parsing repository...")
    r = httpx.post(f"{BASE_URL}/{repo_id}/parse")
    if r.status_code != 200:
        print("Failed parse:", r.text)
        sys.exit(1)
    print("Parsed:", r.json())

    # 3. Chunk
    print("Chunking repository...")
    r = httpx.post(f"{BASE_URL}/{repo_id}/chunk")
    if r.status_code != 200:
        print("Failed chunk:", r.text)
        sys.exit(1)
    print("Chunked:", r.json())

    # 4. Index
    print("Indexing repository...")
    r = httpx.post(f"{BASE_URL}/{repo_id}/index", timeout=120.0)
    if r.status_code != 200:
        print("Failed index:", r.text)
        sys.exit(1)
    print("Indexed:", r.json())

    # 5. Search
    print("Testing search...")
    r = httpx.post(f"{BASE_URL}/{repo_id}/test-search", json={"query": "authentication"})
    if r.status_code != 200:
        print("Failed search:", r.text)
        sys.exit(1)
    print("Search Results:", r.json())
    print("SUCCESS")

if __name__ == "__main__":
    test_flow()
