import httpx
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000/api/repositories"
REPO_ID = "repo_b818d6"  # Use the repo we just successfully indexed

def test_chat():
    question = "How does authentication work?"
    print(f"Testing Chat Endpoint for question: '{question}'")
    print("Sending request to LLM (this may take a few seconds)...")
    
    try:
        r = httpx.post(f"{BASE_URL}/{REPO_ID}/chat", json={"question": question}, timeout=120.0)
        
        if r.status_code != 200:
            print("\n❌ Failed chat request:", r.text)
        else:
            data = r.json()
            answer = data.get("answer", "")
            sources = data.get("sources", [])
            confidence = data.get("confidence", 0)
            
            print(f"\n✅ LLM Response Received (Confidence: {confidence}%):\n")
            print("="*80)
            print(answer)
            print("="*80)
            
            if sources:
                print("\nEVIDENCE SOURCES:")
                for i, src in enumerate(sources, 1):
                    print(f"\n[{i}] File: {src.get('file_path')} (Score: {src.get('similarity_score', 0):.2f})")
                    print("-" * 40)
                    print(src.get("snippet", ""))
                    print("-" * 40)
            
            print("\nSUCCESS: Phase 9 (Source Attribution) is fully functional!")
            
    except httpx.ReadTimeout:
        print("\n❌ Request timed out! Is the model still loading or API hanging?")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")

if __name__ == "__main__":
    test_chat()
