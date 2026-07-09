import os
import sys
import requests
import json

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def _call_gemini(prompt, response_json=True):
    if not GEMINI_API_KEY:
        print("[ERROR] GEMINI_API_KEY environment variable is not set.")
        sys.exit(1)
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    if response_json:
        payload["generationConfig"] = {"responseMimeType": "application/json"}
        
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        print(f"[ERROR] Gemini API Error: {response.status_code}")
        print(f"[DEBUG] Server response: {response.text}")
        sys.exit(1)
        
    res_json = response.json()
    return res_json["candidates"][0]["content"]["parts"][0]["text"]

def analyze_codebase(file_list, file_contents):
    prompt = f"""
    You are an expert code reviewer. Analyze the following repository context completely.
    
    Repository Structure / File List:
    {json.dumps(file_list, indent=2)}
    
    Main Files Content:
    {json.dumps(file_contents, indent=2)}
    
    Provide your analysis STRICTLY in JSON format with the following keys:
    - "summary": A brief text description of what this project does.
    - "technologies": An array of strings listing technologies, languages, and libraries used.
    - "strengths": An array of strings highlighting the project's strong points, good architectural patterns, and code quality practices.
    - "issues": An array of strings identifying any bugs, security risks, or code quality problems.
    - "recommendations": An array of strings providing actionable improvement suggestions.
    """
    ai_text_response = _call_gemini(prompt, response_json=True)
    return json.loads(ai_text_response)

def analyze_pull_request(diff_text):
    prompt = f"""
    You are an expert senior code reviewer. Analyze the following Pull Request diff changes and provide an automated review.
    
    Pull Request Diff:
    {diff_text}
    
    Provide your review analysis STRICTLY in JSON format with the following keys:
    - "summary": A concise description of the changes introduced in this PR.
    - "bugs": An array of strings identifying potential bugs, security flaws, or unhandled edge cases.
    - "style_and_architecture": An array of strings commenting on naming, readability, patterns, and code structure.
    - "optimization": An array of strings proposing efficiency, memory, or performance gains.
    - "approved": A boolean value (true/false) representing whether this PR looks good to merge.
    """
    ai_text_response = _call_gemini(prompt, response_json=True)
    return json.loads(ai_text_response)
