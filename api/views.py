import os
import requests
from django.shortcuts import render
from .forms import ScriptForm

# Load the API key securely (ideally from an environment variable)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Replace with a real key

def generate_script(prompt):
    """
    Generate a video script using Google Gemini API.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.7,  # Controls randomness
            "candidateCount": 1  # Number of responses to return
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        response_data = response.json()
        candidates = response_data.get("candidates")
        if candidates:
            content = candidates[0].get("content")
            if content and content.get("parts"):
                return content["parts"][0].get("text", "No response received")
            else:
                return "No content found in the response."
        else:
            return "No candidates found in the response."
    else:
        return f"Error: {response.status_code}, {response.text}"

def index(request):
    """
    Handle the homepage, process form submissions, and generate scripts.
    """
    form = ScriptForm(request.POST or None, request.FILES or None)
    generated_script = None

    if request.method == 'POST' and form.is_valid():
        prompt = form.cleaned_data['prompt']

        # Process the file if uploaded (e.g., PDF or text file)
        if form.cleaned_data.get('file'):
            file = form.cleaned_data['file']
            try: #Added try except block to handle file reading exceptions

                if file.name.endswith('.txt'):
                    content = file.read().decode('utf-8')  # Read text file content
                    prompt += f" {content}"
                elif file.name.endswith('.pdf'):
                    import pdfplumber
                    with pdfplumber.open(file) as pdf:
                        content = "".join([page.extract_text() for page in pdf.pages if page.extract_text()])
                    prompt += f" {content}"
            except Exception as e:
                generated_script = f"Error processing file: {str(e)}"
                return render(request, 'index.html', {'form': form, 'generated_script': generated_script})

        # Generate the script using Gemini API
        generated_script = generate_script(prompt)

    return render(request, 'index.html', {'form': form, 'generated_script': generated_script})