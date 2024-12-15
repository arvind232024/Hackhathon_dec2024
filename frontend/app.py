import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_file):
    # Extract text from the uploaded PDF
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def generate_excel(brd_document_text, text, website_link):
    # Create a DataFrame with the inputs
    data = {
        'BRD Document Text': [brd_document_text],
        'Text': [text],
        'Website Link': [website_link],
    }
    df = pd.DataFrame(data)

    # Save DataFrame to Excel
    excel_file = io.BytesIO()
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

        # Create a chart using XlsxWriter
        worksheet = writer.sheets['Sheet1']
        chart = writer.book.add_chart({'type': 'column'})

        # Add series to the chart (using the lengths of the text and website link)
        chart.add_series({
            'name': 'Text Length',
            'categories': '=Sheet1!$B$2:$B$2',
            'values': '=Sheet1!$D$2:$D$2',
        })
        chart.add_series({
            'name': 'Website Link Length',
            'categories': '=Sheet1!$C$2:$C$2',
            'values': '=Sheet1!$E$2:$E$2',
        })

        # Insert the chart into the worksheet
        worksheet.insert_chart('G2', chart)

    excel_file.seek(0)
    return excel_file, df

def plot_sample_chart():
    # Sample chart using Matplotlib
    data = {'Category A': 30, 'Category B': 45, 'Category C': 60}
    categories = list(data.keys())
    values = list(data.values())

    fig, ax = plt.subplots()
    ax.bar(categories, values, color='skyblue')
    ax.set_title('Sample Chart')
    ax.set_xlabel('Categories')
    ax.set_ylabel('Values')

    # Display the chart in Streamlit
    st.pyplot(fig)

def main():
    st.title("QA Hackathon")

    # File uploader for PDF
    brd_document_file = st.file_uploader("Upload BRD Document (PDF)", type="pdf")
    text = st.text_area("Text")
    website_link = st.text_input("Website Link")

    # Process the PDF if uploaded
    if brd_document_file:
        brd_document_text = extract_text_from_pdf(brd_document_file)
    else:
        brd_document_text = ""

    # Submit button
    if st.button("Submit"):
        if brd_document_text and text and website_link:
            # Generate Excel file and chart
            excel_file, df = generate_excel(brd_document_text, text, website_link)

            # Display the Excel file and chart
            st.write("Generated Excel Data:")
            st.write(df)

            # Provide download link for the Excel file
            st.download_button(
                label="Download Excel File",
                data=excel_file,
                file_name="generated_file.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

                    # Add a sample chart
            st.subheader("Sample Chart")
            plot_sample_chart()
        else:
            st.error("Please fill in all fields and upload a BRD document.")

    

    # Add a "Coming Soon Connectors" section
    st.markdown("### Connectors")
    st.write("Stay tuned for upcoming connectors to integrate with different services.")

if __name__ == "__main__":
    main()