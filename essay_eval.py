import base64
import requests
import json
import sys

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:4b"  # Change if you're using a different name

def encode_image_to_base64(image_path):
    """Encodes an image file to base64 string."""
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded

def query_gemma3_vision(image_path, prompt=\
    "Evaluate the attached essay based on the following expectations: \
    1. Talk about cultural practices of a particular country.\
    2. Talk about the issues in the cultural practices.\
    3. Provide your own opinion on the matter.\
    Use the rubric below to give a score:\
    90-100% (A): Exceptional work; demonstrates mastery of the assignment's objectives, using excellent grammar.\
    80-89% (B): Solid work; demonstrates a good understanding and fulfills most requirements, with good grammar.\
    70-79% (C): Satisfactory work; demonstrates an adequate understanding but may have some weaknesses, with some grammitcal problems.\
    60-69% (D): Below average work; demonstrates a limited understanding and has significant weaknesses, with unacceptable grammatical errors.\
    Below 60% (F): Unsatisfactory work; fails to meet the assignment's objectives; very problematic sentences unacceptable grammatical errors."):
    
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


 