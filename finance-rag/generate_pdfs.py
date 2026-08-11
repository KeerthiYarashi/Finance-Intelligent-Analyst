import os
from fpdf import FPDF

def create_pdf(filename, title, quarter, revenue, profit, margin, management_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    # Title
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.ln(10)
    
    # Financial Highlights
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"Financial Highlights - {quarter}", ln=True)
    
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, txt=f"Total Revenue: ${revenue} Billion", ln=True)
    pdf.cell(200, 10, txt=f"Net Profit: ${profit} Billion", ln=True)
    pdf.cell(200, 10, txt=f"Operating Margin: {margin}%", ln=True)
    pdf.ln(10)
    
    # Management Commentary
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Management Commentary", ln=True)
    
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, txt=management_text)
    
    # CEO info trap
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, txt="Note: This document contains forward-looking statements.", ln=True)
    
    pdf.output(filename)

def main():
    os.makedirs("data", exist_ok=True)
    
    # Q1
    q1_text = "Demand outlook remains strong across all geographies, particularly in the cloud computing segment which grew by 24%. Headwinds include supply chain constraints in Asia."
    create_pdf("data/TechCorp_Q1_2023.pdf", "TechCorp Q1 2023 Earnings Release", "Q1 2023", 52.4, 12.1, 23.1, q1_text)
    
    # Q2
    q2_text = "Revenue grew significantly compared to the same quarter of the previous year. We declared a dividend of $0.55 per share with a record date of August 15. The enterprise software segment grew fastest, up 31%."
    create_pdf("data/TechCorp_Q2_2023.pdf", "TechCorp Q2 2023 Earnings Release", "Q2 2023", 56.8, 14.2, 25.0, q2_text)
    
    # Q3
    q3_text = "Operating margin continues a rising trend this year. However, we see risks related to currency fluctuations and inflation challenges in the European market. A three-line summary: Record revenue driven by cloud adoption. Margins expanded despite macro risks. Strong pipeline for Q4."
    create_pdf("data/TechCorp_Q3_2023.pdf", "TechCorp Q3 2023 Earnings Release", "Q3 2023", 61.2, 16.5, 27.0, q3_text)

if __name__ == "__main__":
    main()
