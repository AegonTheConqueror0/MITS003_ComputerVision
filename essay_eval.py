import base64
import requests
import json
import sys

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:4b"  

def encode_image_to_base64(image_path):
    """Encodes an image file to base64 string."""
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded

def query_gemma3_vision(image_path, prompt=\
    "You are a strict, hyper-critical IT Faculty Professor grading a Web Design assignment. \
    Analyze the attached UI screenshot mercilessly. Look for amateur design flaws. \
    Evaluate based on these exact expectations:\
    1. Visual Hierarchy: Are fonts, elements, and scales organized professionally, or is it chaotic and cluttered?\
    2. Contrast & Readability: Is text instantly legible? (Crucial: Light blue text on busy cloud backgrounds, or dark text on dark patterns is an automatic failure).\
    3. Layout Alignment: Is there a clean modern grid? Abuse of centered text, random icons, or unaligned elements must be penalized.\
    \
    Use this strict grading rubric:\
    90-100% (A): Professional-grade UI; flawless grid layout, perfect typographic hierarchy, and accessible color contrast.\
    80-89% (B): Good modern attempt; functional layout with only minor, nitpicky spacing or padding flaws.\
    70-79% (C): Amateur layout; lacks design polish, overuses centered alignment, or has minor readability strains.\
    60-69% (D): Poor layout; outdated aesthetics (like 90s clip-art style layouts), bad color contrast choices, or unstructured elements.\
    Below 60% (F): Completely broken UI; text layers bleed into busy background graphics, unreadable text contrast, or overlapping components.\
    \
    CRITICAL INSTRUCTION: If the design looks unpolished, uses outdated 90s design tropes (like random flags, stacked raw links, and loud tiling backgrounds), or forces blue text over a blue cloud background, you are forbidden from giving an A or B. You must grade it a D or F."):
    
    image_base64 = encode_image_to_base64(image_path)

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "images": [image_base64],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_ENDPOINT, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "No response text returned.")

    except requests.RequestException as e:
        return f"Request failed: {e}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python gemma3_vision_insight.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    insights = query_gemma3_vision(image_path)
    print("=== Insights Extracted ===")
    print(insights)


 