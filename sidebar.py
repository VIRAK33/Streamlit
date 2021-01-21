
import streamlit as st





def select_course(md):
    course = st.sidebar.selectbox(
        'Select course:',
        (md['Course Name'].unique())
    )
    return course

def features(arr):
    question = st.sidebar.selectbox(
    'Select option',arr
    )
    return question
    