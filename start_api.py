"""
Start API Server
Simple script to start the MLOps API server
"""
import subprocess
import sys
from pathlib import Path

def main():
    print("🚀 Starting MLOps API Server...")
    
    # Get the API file path
    api_file = Path(__file__).parent / "MLOps_Engineer3" / "api" / "serve.py"
    
    if not api_file.exists():
        print(f"❌ API file not found: {api_file}")
        return 1
    
    try:
        # Start the API server
        subprocess.run([sys.executable, str(api_file)], check=True)
    except KeyboardInterrupt:
        print("\n🛑 API server stopped")
        return 0
    except Exception as e:
        print(f"❌ Error starting API: {e}")
        return 1

if __name__ == "__main__":
    exit(main())