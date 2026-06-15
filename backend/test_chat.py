import httpx
import sys

BASE_URL = "http://127.0.0.1:8000/api/repositories"
REPO_ID = "repo_78a739"  # Use the same parsed repo we used in Phase 6

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
            
            print("\n✅ LLM Response Received:\n")
            print("="*80)
            print(answer)
            print("="*80)
            print("\nSUCCESS: Phase 7 is fully functional!")
            
    except httpx.ReadTimeout:
        print("\n❌ Request timed out! Is the model still loading or API hanging?")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")

if __name__ == "__main__":
    test_chat()
