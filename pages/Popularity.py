# import the required libraries 

#-----------------snowpark-------------------
from snowflake.snowpark.session import Session
from snowflake.snowpark.types import IntegerType

#-----------------pandas---------------------
import pandas as pd

#-----------------PIL---------------------
from PIL import Image

#----------------streamlit-------------------
import streamlit as st
import streamlit.components.v1 as components

#----------------misc-----------------------
import re
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import json
from dotenv import load_dotenv

st.set_page_config(
    page_title="Sn❆wstream",
    page_icon=Image.open("./favicon.png"),
    layout="wide",
    initial_sidebar_state="collapsed",
)
load_dotenv()
#----------create session object--------------
def create_session_object():
   connection_parameters = {
   "account": os.environ["account"],
   "user": os.environ["user"],
   "password":os.environ["password"],
   "warehouse": "compute_wh",
   "role": "accountadmin",
   "database": "openalex"
  }
   session = Session.builder.configs(connection_parameters).create()
   print(session.sql('select current_warehouse(), current_database(), current_schema()').collect())
   return session

#---------------sidebar----------------------
animation="""
<iframe src="https://embed.lottiefiles.com/animation/77218"></iframe>
"""
st.sidebar.markdown("<br><br><br><br>",unsafe_allow_html=True)
st.sidebar.markdown(animation,unsafe_allow_html=True)

session=create_session_object()

st.markdown("<h1 style='font-size:4rem;line-height:14px;margin:0;padding:0;'>☁<br><h2>&nbsp;///</h2></h1>",unsafe_allow_html=True)
st.title("Popularity")

def render(schema):
    col1,col2=st.columns(2)

    with col1:
        search_choice=st.text_input(f"Enter any keyword contained in the {schema}'s name",value="art",key=f"{schema}Key")

    with col2:
        numberOfSamples=st.slider("Enter the number of samples to search from",min_value=0,value=5000,max_value=65000,step=1000,key=f"{schema}KeySample")

    if search_choice!=0:
        schema_df=pd.DataFrame(session.sql(f"select display_name, TO_JSON(counts_by_year) from openalex.{schema}s limit {numberOfSamples}").collect())
        df_new=pd.json_normalize(schema_df["TO_JSON(COUNTS_BY_YEAR)"].apply(json.loads))
        df_new['name']=schema_df["DISPLAY_NAME"]
        df_new = df_new[df_new["name"].str.contains(search_choice.replace(" ","|"),case=False,na=False)]
        col=st.columns(2)
        col_no=0
        for index,row in df_new.iterrows():
            row=row.tolist()
            l=len(row)
            name=row[-1]
            year=[]
            works_count=[]
            cited_by_count=[]
            for i in range(l-1):
                if row[i]:
                    if "year" in row[i]:
                        year.append(row[i]["year"]) 
                        if "works_count" in row[i]:works_count.append(row[i]["works_count"])
                        else:works_count.append(0)
                        if "cited_by_count" in row[i]:cited_by_count.append(row[i]["cited_by_count"])
                        else:cited_by_count.append(0)
            df=pd.DataFrame({"year":year,'works_count':works_count,"cited_by_count":cited_by_count},columns=["cited_by_count","works_count","year"])
            
            if df.empty==False:
                #-----------------draw plots--------------------------------------
                with col[col_no%2]:
                    pattern = re.compile(re.escape(search_choice), re.IGNORECASE)
                    st.header(pattern.sub(f":blue[{search_choice}]", name))
                    col_no+=1
                    fig = make_subplots(specs=[[{"secondary_y": True}]])
                    fig.add_trace(
                        go.Bar(x=df['year'], y=df['cited_by_count'], name="Cited By count"),
                        secondary_y=False,
                    )

                    fig.add_trace(
                        go.Scatter(x=df['year'], y=df['works_count'], name="Works count"),
                        secondary_y=True,
                    )
                    fig.update_layout(xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=False)
                    )           
                    st.plotly_chart(fig, use_container_width=True)       

                    st.divider()

               
def ui(schema):
    st.subheader(f"{schema}'s name")
    render(f"{schema}")

tab1, tab2, tab3, tab4  = st.tabs(["Concepts","Author","Institutions","Works"])
with tab1:ui("concept")
with tab2:st.header('`Coming Soon`')
with tab3:st.header('`Coming Soon`')
with tab4:st.header('`Coming Soon`')
