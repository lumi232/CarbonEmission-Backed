```python
import PyPDF2
import openai
from apiKey import api_key
import csv

def extract_text_from_pdf(pdf_path):
    """Extracts text from a given PDF file."""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_data_from_csv(csv_path):
    """Extracts data from a given CSV file."""
    text = ""
    try:
        with open(csv_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                text += ",".join(row) + "\n"
    except FileNotFoundError:
        return f"Error: CSV file not found at path: {csv_path}"
    except Exception as e:
        return f"Error reading CSV file: {e}"
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
    file_path = "Electricity Consumption Report.pdf"  # You can later make this a command-line argument

    if file_path.lower().endswith(".pdf"):
        report_text = extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(".csv"):
        report_text = extract_data_from_csv(file_path)
    else:
        print("Error: Unsupported file format.")
        print("Supported formats are: PDF (.pdf) and CSV (.csv).")
        report_text = None # Set report_text to None to prevent further processing

    if report_text: # Proceed only if report_text is not None (i.e., file was processed successfully)
        if report_text.startswith("Error:"): # Check if the extraction function returned an error message
            print(report_text) # Print the error message
        else:
            recommendations = get_gpt4_recommendations(report_text)

            print("\n**Carbon Emission Reduction Recommendations:**\n")
            print(recommendations)
```