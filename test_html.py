import streamlit as st
from components.model_details import render_model_details
from utils.style_loader import load_css

st.set_page_config(layout="wide")

load_css("styles/style.css")

render_model_details()