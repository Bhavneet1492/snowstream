#---------import required libraries----------
import streamlit as st
import PIL

#-------------Set page context---------------
st.set_page_config(
    page_title="Sn❆wstream",
    page_icon="chart_with_upwards_trend",
    layout="wide",
    initial_sidebar_state="collapsed",
)

#------------------custom css styling-------------
custom_css="""
<style>
img {
    margin-right:2rem;
    margin-top:-3rem;
    margin-bottom:-5rem;
}
.custom1{
    font-weight:50;
    opacity:0.5;
    font-size:1.6rem;
    margin-top:-2.2rem;
}
.custom5{
    font-weight:1;
    width:80%;
}
.custom3{
    font-weight:1;
    font-size:0.95rem;
    opacity:0.6;
}
[data-testid="metric-container"]{
    /* border:1px solid white; */
    border-radius:0.7rem;
    padding:1rem;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    margin-top:1rem;
    background:rgb(255,255,255,0.1);
    color:#29B5E8;
    overflow:hidden;
}
.css-1wivap2{
}
[data-testid="metric-container"]:hover{
    cursor:crosshair;
    transition:0.3s linear;
    background:none;
}
@media screen and (orientation: portrait){
  img {
   padding-right:2rem;
}  
[data-testid="metric-container"]{
    width:90vw;
}
.custom5{
    width:100%;
}
@media screen and (max-width:300px){
  img {
   padding-right:7rem;
}  
}
</style>

"""
# ------------------homepage text and styling--------------------------
st.image(PIL.Image.open("./logo_ss.png"),width=300)
st.markdown(custom_css,unsafe_allow_html=True)
st.header("re: Search//")
st.markdown('<h1 class="custom1">search redefined</h1><h5 class="custom5" style="font-weight:200;">Search from among millions of research papers and articles with easy filtering options. The works of the author you’re looking for, your preferred institution or publisher, country of origin and more, everything is just a click away :) How cool is that really?</h5>',unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Data source:", "OpenAlex", "by Util")
col2.metric("Inspired by the", "ancient", "-Library of Alexandria")
col3.metric("Updated on", "monthly", "basis")
col4.metric("Olivie Blake's", "related", "-The Atlas Six")
st.markdown('<h3 class="custom3"><i>You can see how popular a topic is <a  target="_blank" href="https://bhavneet1492-snowstream-home-eizpch.streamlit.app/Popularity">[Popularity]</a> and locate institutions on a world map too! <a  target="_blank" href="https://bhavneet1492-snowstream-home-eizpch.streamlit.app/Stream">[Stream->Location]</a></i></h3>',unsafe_allow_html=True)

#---------------sidebar----------------------
animation="""
<iframe src="https://embed.lottiefiles.com/animation/77218"></iframe>
"""
st.sidebar.markdown("<br><br>",unsafe_allow_html=True)
st.sidebar.markdown(animation,unsafe_allow_html=True)
