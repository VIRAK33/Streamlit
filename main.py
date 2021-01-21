import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import datetime
import module_config
import sidebar as side
import query as qr
import base64

module_config.style()
st.title('Data Visualization')

def download_csv(md):
    csv = md.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a style="float:right" href="data:file/csv;base64,{b64}">Download csv file</a>' 

    st.markdown(href, unsafe_allow_html=True)


data_file = st.file_uploader("Upload a file", type=("csv", "csv"))

if data_file is not None:
    
    file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}
    # st.write(file_details)
    df = pd.read_csv(data_file)
    md = df.rename(columns={'userid':'userid', 'username': 'ID', 'firstname':'Student Name', 'phone1':'Sex', 'department':'Department', 'lastname':'Group', 'courseName':'Course Name', 'moduleName':'Module Name', 'completionstate': 'Completion State', 'CompletionDate':'Completion Date'})
   
    radio_select = st.sidebar.radio('Feature', ['Course', 'Student', 'Completion'])

    # Course = side.select_course(md)
    if radio_select == 'Course':
        option_course = ['All courses and students', 'Course Summary', 'Student Learning Progress',
                        'Active Students', 'All course in Department', 'Department Summary'
                        ]
        question = side.features(option_course)
        
        all_courses = md['Course Name'].unique()

        # Select question 0 "All courses and students"
        if question == option_course[0]:
            course = st.selectbox(
                'Select course:',
                (all_courses)
            )
            md = md[['ID', 'Student Name', 'Sex', 'Group', 'Department', 'Course Name', 'Completion State', 'Completion Date']]
            md = md[md['Course Name'] == course ]
            st.write(md)
            download_csv(md)

            

        if question ==  option_course[1]:
            md = qr.course_summary(md)
            st.write(md)
            download_csv(md)



    if radio_select == 'Student':
        option_student = ['List Student in Department', 'Student Details', 'Learning Progress all student in Department']
        question = side.features(option_student)


        md['cn'] = md['Course Name'].map({'Climate Change and Adaptation':'Climate Change and Adaptation', 'Cover Crop':'Cover Crop',\
        'Database Analysis and Design':'Database Analysis and Design', 'Environmental Geology':'Environmental Geology',\
        'Food Microbiology': 'Food Microbiology', 'Geodesy and Topography':'Geodesy and Topography',\
        'Geographic Information System and Remote Sensing':'GIS',\
        'Image Processing':'Image Processing', 'Introduction to Computer Science': 'CS',\
        'Natural Language Processing':'NLP', 'Software Engineering':'Software Engineering',\
        'Strength of Material':'Strength of Material', 'Topographic Surveying':'Topographic Surveying'})
            
        s = plt.figure(figsize=(4,6), dpi=250)
        g2 = sns.countplot(y="cn", hue = 'Sex', data=md)
        for p in g2.patches:
                percentage = '{:.0f}'.format(p.get_width())
                x = p.get_x() + p.get_width() + 0.02
                y = (p.get_y() + p.get_height()/2) + 0.15
                g2.annotate(percentage, (x, y))
                
        plt.title("Number of students in each courses")
        plt.xlabel('Number of students')
        plt.ylabel('Courses')
        # plt.show()
        # plt.savefig('Number of students in each courses.png')

        col1,col2 = st.beta_columns(2)
        with col1:
            st.write(s)

    if radio_select == 'Completion':
        option_completion = ['Student and Finished Course', 'Completion Summary']
        question = side.features(option_completion)

