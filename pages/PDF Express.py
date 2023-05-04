#-------importing required libraries------------
import streamlit as st
import requests
import PIL
import openai
import pypdf
import io
import re
import os
from dotenv import load_dotenv

st.set_page_config(
    page_title="Sn❆wstream",
    page_icon=PIL.Image.open("./favicon.png"),
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_dotenv()

#---------------sidebar----------------------
animation="""
<iframe src="https://embed.lottiefiles.com/animation/77218"></iframe>
"""
st.sidebar.markdown("<br><br><br><br>",unsafe_allow_html=True)
st.sidebar.markdown(animation,unsafe_allow_html=True)

#------------initializing variables---------
url=0
pdf=0

# __________________________________________
# ------------------------------------------
# CUSTOMIZING HOMEPAGE
# ------------------------------------------
# __________________________________________


custom_css="""
<style>
[data-testid="stAppViewContainer"] {
    background:#ABBBD6;
}
[data-testid="stHeader"] {
    background:transparent;
}
[data-testid="column"] {
    justify-content:center;
    align-items:center;
}
img {
    transform:scale(1.2);
    margin-right:2rem;
}
.css-1b67tfe{
    z-index:1000000;
}
.css-ml2xh6{
     margin-top:-3rem;
} 
.block-container {
    padding:0rem;
    box-sizing:border-box;
    padding-left:3rem;
}
.stTextInput,[data-testid="stFileUploadDropzone"]{
    margin-left:4rem;
    width:70%;
}
</style>
"""
st.markdown(custom_css,unsafe_allow_html=True)


col1, col2= st.columns(2)

with col1:
      title = """
       <div class="left">
            <h2 class="custom"><b>PDF</b> <br>express </h2>
        </div>

        <style>
        .left{
            margin:0;
            margin-top:3rem;
            padding:0;
            display:flex;
            flex-direction:column;
            align-items: center;
            justify-content:center;
            z-index:100;
            }
        .button{
            display:flex;
            align-items:center;
            justify-content:center;  
            z-index:10000;
            margin-bottom:-1.5rem;
            }
        .button{
            margin-left:27%;
            width:12rem;
            padding: 0.5rem;
            background:rgba(255, 255, 255, 0.3);
            border-radius: 100rem;
            color:white;
            display:flex;
            align-items:center;
            justify-content:center;
            font-family: Arial, Helvetica, sans-serif;
            text-align: center;
            font-size:1.2rem;
            font-weight:500;
            z-index:100;
            border:none;
        }
        .button:hover{
            background:#54648B;
            color:#00FCFE;
            transition: 0.5s linear;
            cursor:pointer;
            border:none;
        }
        .custom,b{
            color:#54648B;
            font-size:2.5rem;
            font-weight:700;
            text-align: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
            z-index:100;
            line-height:80%;
        }
        b{
            font-size:4.7rem;
        }
        @media screen and (orientation: portrait) {
        }
        </style>
      """
      st.markdown(title, unsafe_allow_html=True)
      st.markdown('<h2 class="button">Enter URL</h2>', unsafe_allow_html=True)
      
      #-----text input are for entering url---------------------------
      url=st.text_input("",key="url_key",value="http://amsacta.unibo.it/4469/1/WP1051.pdf")

      st.markdown('<h2 class="button">Upload PDF</h2>', unsafe_allow_html=True)

      #----------document uploader to upload pdf file---------------------
      pdf=uploaded_file = st.file_uploader("",type="pdf")

#-----------------adding gif image for imporving ui------------
with col2:
      st.image("https://i.pinimg.com/originals/58/c0/f3/58c0f33b40e1eb3d1d199f9128b9e750.gif",use_column_width=1)


st.divider()    


# assert "openai" in get_services()
# secrets = openai_secret_manager.get_secret("openai")
openai.api_key = os.environ["api_key"]

#splitting the entire text from pdf into blocks of 2048 characters each
def split_text(text):
    max_chunk_size = 2048
    chunks = []
    current_chunk = ""
    for sentence in text.split("."):
        if len(current_chunk) + len(sentence) < max_chunk_size:
            current_chunk += sentence + "."
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + "."
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

#summarizing text using opeanai api
def summarize(text):
    # Clean the text by removing newlines and excess whitespace
    text = re.sub('\n', ' ', text)
    text = re.sub(' +', ' ', text)

    # Set up the OpenAI GPT-3 API request
    prompt = f"Please summarize the following text:\n{text}\nSummary:"
    model = "text-davinci-002"
    max_tokens = 500

    # Send the API request and get the response
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Extract the summary from the API response and return it
    summary = response.choices[0].text.strip()
    return summary

#summarizing each 2048 character long block of text and concatenating the responses together
def generate_summary(text):
    response=" "
    input_chunks = split_text(text)
    output_chunks = []
    for chunk in input_chunks:
        response = summarize(chunk)
    return response

#function to render the summary of pdf file text on the page
def render(pdf_file):
    number_of_pages = len(pdf_file.pages)
    extractedText=""
    for page in range(0,number_of_pages): extractedText += pdf_file.pages[page].extract_text()
    st.write(generate_summary(extractedText))
cola,colb=st.columns(2)

with cola:
    if url:
        st.subheader("From URL PDF")
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Windows; Windows x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'}
        response = requests.get(url=url)
        on_fly_mem_obj = io.BytesIO(response.content)
        pdf_file = pypdf.PdfReader(on_fly_mem_obj)
        render(pdf_file)
with colb:
    st.subheader("From uploaded PDF")        
    if pdf!=0:render(pdf)  
