import httpx
import json

BASE_URL = "http://127.0.0.1:8000/api/repositories"
REPO_ID = "repo_78a739"  # Sindre Sorhus ky repo

def test_analysis():
    print(f"Testing Analysis Endpoint for repository: {REPO_ID}")
    print("Sending request to generate insights (this uses the LLM and may take a few moments)...")
    
    try:
        r = httpx.post(f"{BASE_URL}/{REPO_ID}/analyze", timeout=120.0)
        
        if r.status_code != 200:
            print("\n❌ Failed analysis request:", r.text)
        else:
            data = r.json()
            
            print("\n✅ Analysis Complete! Insights Generated:\n")
            print("="*80)
            
            print("### METRICS")
            metrics = data.get("metrics", {})
            for k, v in metrics.items():
                print(f"- {k}: {v}")
                
            print("\n### TECH STACK")
            stack = data.get("tech_stack", {})
            for k, v in stack.items():
                print(f"- {k.capitalize()}: {', '.join(v)}")
                
            print("\n### ENTRY POINTS")
            for ep in data.get("entrypoints", []):
                print(f"- {ep}")
                
            print("\n### IMPORTANT FILES")
            for f in data.get("important_files", []):
                print(f"- {f}")
                
            print("\n### ARCHITECTURE OVERVIEW")
            print(data.get("architecture_overview", ""))
            
            print("\n### REPOSITORY SUMMARY")
            print(data.get("summary", ""))
            
            print("="*80)
            print("\nSUCCESS: Phase 8 is fully functional!")
            
    except httpx.ReadTimeout:
        print("\n❌ Request timed out! Is the model still loading or API hanging?")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")

if __name__ == "__main__":
    test_analysis()
