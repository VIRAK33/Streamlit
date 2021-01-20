import  streamlit as st
def style():
    st.set_page_config(layout="wide")

    st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
    }
    </style>
    """, unsafe_allow_html=True)