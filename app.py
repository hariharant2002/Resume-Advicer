import streamlit as st
import json
import re
import ast
import google.generativeai as palm
import fitz  # PyMuPDF library
palm.configure(api_key=st.secrets["api_key"])



def qgen(text):

    defaults = {
    'model': 'models/text-bison-001',
    'temperature': 0.6,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
    'max_output_tokens': 1024,
    'stop_sequences': [],
    'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":1},{"category":"HARM_CATEGORY_TOXICITY","threshold":1},{"category":"HARM_CATEGORY_VIOLENCE","threshold":2},{"category":"HARM_CATEGORY_SEXUAL","threshold":2},{"category":"HARM_CATEGORY_MEDICAL","threshold":2},{"category":"HARM_CATEGORY_DANGEROUS","threshold":2}],
    }

    
    prompt = f"""Extract the work experience section from the given resume, and rewrite i, along with the accompanying description. Do not change
      the wording of the text.
      If there is no work experience/internship, return NIL
      Do not insert other information like projects, skills, etc.
      Do not make assumptions
    input: {text}
    output:"""

    response = palm.generate_text(
    **defaults,
    prompt=prompt
    )
    question_list=response.result
    # #sentences_list = re.split(r'\. (?=[A-Z])',question_list)
    # actual_list = ast.literal_eval(question_list)
    #return response.result
    return fix(response.result)

def fix(text):

    defaults = {
    'model': 'models/text-bison-001',
    'temperature': 0.6,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
    'max_output_tokens': 1024,
    'stop_sequences': [],
    'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":1},{"category":"HARM_CATEGORY_TOXICITY","threshold":1},{"category":"HARM_CATEGORY_VIOLENCE","threshold":2},{"category":"HARM_CATEGORY_SEXUAL","threshold":2},{"category":"HARM_CATEGORY_MEDICAL","threshold":2},{"category":"HARM_CATEGORY_DANGEROUS","threshold":2}],
    }

    
    prompt = f"""
    "Could you please analyze the Work Experience given? Suggest any necessary changes and improvements.
    rewrite the sentences using action verbs where appropriate. Rewrite the sentences under the heading rewrite .Remember,your response should be informative, logical, and based
    solely on the information provided. Please do not make assumptions or guesses.


    input: {text}
    output:"""

    response = palm.generate_text(
    **defaults,
    prompt=prompt
    )
    question_list=response.result
    # #sentences_list = re.split(r'\. (?=[A-Z])',question_list)
    # actual_list = ast.literal_eval(question_list)
    return response.result


def read_pdf(file):
    text = ""
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text += page.get_text()
    pdf_document.close()
    return qgen(text)
    #return qgen(text)




def main():#1
    st.title("resume fixer \U0001F528")
    uploaded_file = st.file_uploader("Upload your resume", type=["pdf"])

    if uploaded_file is not None:
        st.subheader("Uploaded PDF Content:")
        try:
            pdf_text = read_pdf(uploaded_file)

            st.write(pdf_text)
        except:
            st.error("Error reading the PDF. Please make sure it's a valid PDF document.")

if __name__ == "__main__":
    main()
