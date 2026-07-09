import os


def get_vram_gb():
    # Check if manually set via environment variable
    manual_vram = os.environ.get("VRAM_GB")
    if manual_vram:
        return float(manual_vram)

    # Try nvidia-smi
    try:
        import subprocess
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            vram_mb = int(result.stdout.strip().split("\n")[0])
            return vram_mb / 1024
    except Exception:
        pass
    return 0


def get_best_model():
    vram = get_vram_gb()

    if vram >= 8:
        return "llama3.1:8b", f"High performance model (detected {vram:.1f}GB VRAM)"
    elif vram >= 4:
        return "llama3.2:3b", f"Balanced model (detected {vram:.1f}GB VRAM)"
    elif vram >= 2:
        return "llama3.2:1b", f"Lightweight model (detected {vram:.1f}GB VRAM)"
    else:
        return "llama3.2:1b", "Lightweight model (no GPU detected — running on CPU)"


def ensure_model_available(model_name: str):
    try:
        import ollama
        models = ollama.list()
        available = [m["name"] for m in models.get("models", [])]
        if not any(model_name in m for m in available):
            ollama.pull(model_name)
        return True
    except Exception:
        return False