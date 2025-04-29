import pandas as pd
import pdfplumber

def extract_matrix_from_pdf(pdf_path):
    cost_matrix = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                cost_matrix.extend(table)  # Append all rows

    # Convert to DataFrame
    df = pd.DataFrame(cost_matrix)
    
    return df

pdf_path = "fare_chart.pdf"
df = extract_matrix_from_pdf(pdf_path)
df.to_csv("cost_matrix.csv", index=False)  # Save for verification
print(df.head())  # Display a preview
