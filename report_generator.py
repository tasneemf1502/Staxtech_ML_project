from fpdf import FPDF

def generate_pdf(name, score, prediction, feedback):

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=16)
    pdf.cell(200,10,"InternML Evaluation Report", ln=True, align="C")

    pdf.set_font("Arial", size=12)
    pdf.cell(200,10,f"Student Name: {name}", ln=True)
    pdf.cell(200,10,f"Performance Score: {score}%", ln=True)
    pdf.cell(200,10,f"Prediction: {prediction}", ln=True)

    pdf.multi_cell(0,10,f"Feedback: {feedback}")

    filename = f"{name}_evaluation_report.pdf"
    pdf.output(filename)

    return filename