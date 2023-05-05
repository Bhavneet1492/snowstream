# import the required libraries 

#-----------------snowpark-------------------
from snowflake.snowpark.session import Session
from snowflake.snowpark.types import IntegerType

#-----------------pandas---------------------
import pandas as pd

#----------------streamlit-------------------
import streamlit as st
from streamlit_folium import st_folium

#----------------folium----------------------
import folium

#----------------pillow---------------------
import PIL

#-----------------api-----------------------
import requests
import json

#-----------------time----------------------
import time

from dotenv import load_dotenv
import os

#--------setting thepage configurations-----
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

#-----------------functions-------------------
def loader():
        progress_text = ["Loading databases","Filtering data","Setting the tables","Formatting data","Serving results"]
        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.1)
            my_bar.progress(percent_complete+1, text=progress_text[percent_complete%5])
        st.divider()

def render_data(tab_name,search_choice,numberOfSamples):
    df=pd.DataFrame(session.sql(f"select * from openalex.{tab_name} limit {numberOfSamples}").collect())
    serial_number=0
    if search_choice!=0:
        tab_df = df[df["DISPLAY_NAME"].str.contains(search_choice.replace(" ","|"),case=False,na=False)]
        if tab_df.empty:
            st.error(f"⚠️{tab_name[:-1]} not found")
            st.warning(f"This {tab_name[:-1]} does not exist in the selected samples. Please check if you have entered the correct spelling or try entering a more name")
            st.info("OR search for more samples")
        else:
            for tab in range(len(tab_df)):
                response_API = requests.get(tab_df["WORKS_API_URL"].iloc[tab])
                data = response_API.text
                parse_json = json.loads(data)
                results=parse_json["results"]
                l=len(results)
                for result in range(l):
                    serial_number+=1
                    st.subheader('{}. [{}]({})'.format(serial_number,results[result]["title"],results[result]["doi"]))
                    author_name=", ".join([results[result]["authorships"][index]["author"]["display_name"] for index in range(len(results[result]["authorships"]))])
                    published=results[result]["publication_year"]
                    type_=results[result]["type"]
                    #publisher=results[result]["primary_location"]["source"]["host_organization_name"]
                    try:
                        publisher=results[result]["primary_location"]["source"]["host_organization_name"]
                    except:
                        publisher="unknown"
                    st.markdown('**Author(s)** `{}` **Published:** {} **Type:** {} **Publisher:** _{}_'.format(author_name,published,type_,publisher))
                    tags=""
                    for i in range(len(results[result]["concepts"])):tags+=results[result]["concepts"][i]["display_name"]+" | "
                    institutes=""
                    for i in range(len(results[result]["authorships"])):
                        institutes_len=len(results[result]["authorships"][i]["institutions"])
                        if institutes_len!=0:
                            for j in range(institutes_len):
                                institute_name=results[result]["authorships"][i]["institutions"][j]["display_name"]
                                if institute_name not in institutes:institutes+=results[result]["authorships"][i]["institutions"][j]["display_name"]+" | "
                    if institutes_len!=0:st.markdown("**Associated Institutes:** {}".format(institutes[:-3]))
                    st.markdown("**Tags:** {}".format(tags[:-3]))
                    st.divider()
            
#--------------------------body------------------------
session=create_session_object()

st.title("Stream Research Works")

tab1, tab2, tab3, tab4  = st.tabs(["Author","Topic","Institution","Location"])

def render_ui(tab_name,cols,default):

    with cols[0]:
        st.subheader(f"{tab_name}'s name")
        search_choice=st.text_input(f"Enter any keyword based on the {tab_name}'s name",value=default,key=f"{tab_name}Key")
            
    with cols[2]:
        st.subheader("Samples")
        numberOfSamples=st.number_input("Enter the number of samples to search from",min_value=0,value=100,key=f"{tab_name}KeySample")

    loader()
    render_data(f"{tab_name}s",search_choice,numberOfSamples)

#-------------------tabs------------------------------------
with tab1:
    render_ui("Author",st.columns(3),"har")

with tab2:
     render_ui("Concept",st.columns(3),"art")

with tab3:
     render_ui("Institution",st.columns(3),"tech")

with tab4:
    #creating map for locations of various institutions
    st.code("This map shows the location of various institutions across the globe")
    st.markdown("`Samples`")
    numberOfSamples=st.number_input("Enter the number of samples to search from",min_value=0,value=100,key="GeoKeySample")
    loader()
    df=pd.DataFrame(session.sql(f"select display_name, TO_JSON(geo) from openalex.institutions limit {numberOfSamples}").collect())
    df_new=pd.json_normalize(df["TO_JSON(GEO)"].apply(json.loads))
    # st.dataframe(df_new)
    if st.checkbox("Apply Filter"):
        with st.columns(2)[0]:
            filter_choice=st.radio('**Filter** based on:',("city", "country", "country_code"),horizontal=True)
        with st.columns(2)[1]:
            option = st.selectbox(f'Select a {filter_choice}',df_new[filter_choice].unique())
        df_new=df_new[df_new[filter_choice] == option]
    df_new=df_new[['latitude','longitude']]
    df_new['name']=df["DISPLAY_NAME"]
    df_new.dropna(inplace=True)
    map = folium.Map(location=[50, 50], zoom_start=2)
    for i, row in df_new.iterrows():folium.Marker(location=[row['latitude'], row['longitude']], popup=row["name"]).add_to(map)
    st_folium(map,width=2000, height=500)
