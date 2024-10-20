from flask import Flask, render_template, request, send_file
from flask import redirect, url_for
from fpdf import FPDF
import google.generativeai as genai
from fpdf import FPDF


# Configure the API key for the Generative AI service
genai.configure(api_key="AIzaSyAZFVJ1WLT1AAwSvkTc40jxAALiqxymqXg")

app = Flask(__name__)

# Function to summarize text using the generative AI model
def summarize_text(text):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([f"Summarize the following text:\n\n{text}"])
        
        return response.text
    except Exception as e:
        return f"Error: {e}"
    


class StyledPDF(FPDF):
    def __init__(self, title):
        super().__init__()
        self.title = title  # Store the dynamic title

    def header(self):
        # Add a dynamic header with the provided title
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 51, 102)  # Dark blue color
        self.cell(0, 10, self.title, ln=True, align="C")
        self.ln(10)  # Add spacing after the header

    def footer(self):
        # Add a footer with page numbers
        self.set_y(-15)  # Position at 1.5 cm from the bottom
        self.set_font("Arial", "I", 10)
        self.set_text_color(128)  # Gray color
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

  



def create_pdf(summary, title="Summary Report", output_filename="summary.pdf"):
    pdf = FPDF()
    pdf.add_page()

    # Add title with proper alignment and styling
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.ln(10)  # Add space below the title

    # Set font for the content
    pdf.set_font("Arial", "", 12)

    # Define a list of bullet-like symbols to remove
    bullet_chars = ['*', '-', '•', '●', '‣', '▪']

    # Cleanly add the summary without bullet points
    lines = summary.strip().split('\n')  # Split by newlines
    for line in lines:
        # Remove leading bullet points and whitespace
        cleaned_line = line.lstrip(''.join(bullet_chars)).strip()
        if cleaned_line:  # Add only non-empty lines
            pdf.multi_cell(0, 10, cleaned_line, align="J")
            pdf.ln(2)  # Small space between paragraphs

    # Output the PDF
    pdf.output(output_filename)





# Example usage:
summary_text = """This is a test summary. The content should fit well within the page and align properly."""
dynamic_title = "Custom Header for the Summary Report"
create_pdf(summary_text, title=dynamic_title, output_filename="custom_summary.pdf")

    








# Function to generate a PDF from the summary


@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    if request.method == "POST":
        user_text = request.form["user_text"]
        if user_text:
            summary = summarize_text(user_text)
            create_pdf(summary,title="Summary Report", output_filename="summary.pdf")
            return redirect(url_for("index", summary=summary))

    # On GET request (or page refresh), show an empty form
    
    return render_template("home.html", summary=request.args.get("summary", ""))


@app.route("/download")
def download_pdf():
    return send_file("summary.pdf", as_attachment=True)           
if __name__ == "__main__":
    app.run(debug=True)
