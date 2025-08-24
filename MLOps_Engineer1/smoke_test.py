from pathlib import Path
import json, sys, subprocess

def run(cmd):
    print("▶", " ".join(cmd))
    return subprocess.call(cmd)

def main():
    # 1) run pipeline
    code = run([sys.executable, "-m", "MLOps_Engineer1.core.pipelines.run_ingestion_validation"])
    if code != 0:
        print("❌ Pipeline execution failed"); sys.exit(1)

    # 2) verify artifacts
    json_path = Path("MLOps_Engineer1/artifacts/validation/validation_results.json")
    if not json_path.exists():
        print("❌ validation_results.json not found"); sys.exit(2)

    data = json.loads(json_path.read_text())
    print("▶ validation_results:", json.dumps(data, indent=2))
    if data.get("ok") is True:
        print("✅ Smoke test passed"); sys.exit(0)
    else:
        print("❌ Smoke test failed (ok=false)"); sys.exit(3)

if __name__ == "__main__":
    main()