import PyPDF2
import openai
from apiKey import api_key

def extract_text_from_pdf(pdf_path):
    """Extracts text from a given PDF file."""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def get_gpt4_recommendations(text):
    """Sends the extracted text to GPT-4 for recommendations on reducing carbon emissions."""
    openai.api_key = api_key # Replace with your OpenAI API key
    
    prompt = (
        "Based on the following electricity consumption report, provide detailed recommendations "
        "to reduce carbon emissions for this household. The response should include actionable steps "
        "try to include as many metrics and numeric figures as possible"
        "considering device-wise energy consumption.\n\n" + text
    )
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert in energy efficiency and sustainability."},
                  {"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    pdf_path = "Electricity Consumption Report.pdf"  # Replace with the actual path to the PDF
    report_text = extract_text_from_pdf(pdf_path)
    recommendations = get_gpt4_recommendations(report_text)
    
    print("\n**Carbon Emission Reduction Recommendations:**\n")
    print(recommendations)