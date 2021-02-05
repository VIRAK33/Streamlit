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
from datetime import timedelta
from io import StringIO, BytesIO

module_config.style()



def download_csv(md):
    csv = md.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a style="float:left" href="data:file/csv;base64,{b64}">Download csv file</a>' 

    st.markdown(href, unsafe_allow_html=True)


def get_image_download_link(img):
	"""Generates a link allowing the PIL image to be downloaded
	in:  PIL image
	out: href string
	"""
	buffered = BytesIO()
	plt.savefig(buffered, format="jpg", bbox_inches='tight')
	img_str = base64.b64encode(buffered.getvalue()).decode()
	href = f'<a style="float:left" href="data:file/jpg;base64,{img_str}">Download Image</a>'
	return href

# st.title('Data Visualization')
data_file = st.file_uploader("Upload a file", type=("csv", "csv"))

if data_file is not None:
    st.sidebar.title('Data Visualization')
    file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}
    # st.write(file_details)
    df = pd.read_csv(data_file)
    df = df.rename(columns={'userid':'userid', 'username': 'ID', 'firstname':'Student Name', 'phone1':'Sex', 'department':'Department', 'lastname':'Group', 'courseName':'Course Name', 'moduleName':'Module Name', 'completionstate': 'State', 'CompletionDate':'Completion Date'})
    md = df
    radio_select = st.sidebar.radio('Feature', ['Course', 'Student', 'Completion'])

    # Course = side.select_course(md)
    if radio_select == 'Course':
        option_course = ['All courses and students', 'Course Summary', 'Student Learning Progress',
                        'Active Students', 'All course in Department', 'Department Summary'
                        ]
        question = side.features(option_course)

        all_courses = md['Course Name'].unique()
        all_courses = np.insert(all_courses, 0, 'All', axis=0)

        # Select question 0 "All courses and students"
        if question == option_course[0]:
            # sns.set_theme(style="darkgrid")
            course = st.selectbox(
                'Select course:',
                (all_courses)
            )
            col1,col2 = st.beta_columns(2)
            # with col1:
            md = md[['ID', 'Student Name', 'Sex', 'Group', 'Department', 'Course Name', 'State', 'Completion Date']]

            if course != 'All':
                md = md[md['Course Name'] == course ]
                # st.write(md)
                st.dataframe(data=md, height=600)

            else:
                # md.set_index('ID', inplace=True)
                # st.dataframe(md.assign(hack='').set_index('No'))
                st.dataframe(data=md, height=600)
            
            download_csv(md)


            #Plot Graph_______
            # if course == 'All':
            

            #_______

        # Select question 1 "Course summary"
        if question == option_course[1]:
            course = st.selectbox('Select course:',all_courses)
            col1,col2 = st.beta_columns(2)
            md = qr.course_summary(md)
            with col1:
                st.dataframe(data=md, height=400)
                # st.write(md)
                download_csv(md)

            with col2:
                    
                if course == 'All':
                    md =df
                    md = md.rename(columns={'userid':'ID', 'username': 'Username', 'firstname':'Student Name', 'phone1':'Sex', 'department':'Department', 'lastname':'Group', 'courseName':'Course Name', 'moduleName':'Module Name', 'completionstate': 'State', 'CompletionDate':'Completion Date'})
                    
                    progress = md[(md['State'] == 1)]
                    # pg = progress.groupby(['Student Name','Course Name']).count()
                    # print(pg[['ID']])
                    arr = []
                    for i in range(0, len(progress)):
                        name = progress.iloc[i][2]
                        sex =  progress.iloc[i][3]
                        course = progress.iloc[i][6]

                        completed = progress[progress['Student Name'] == name].count()


                        if [name, sex,course, completed[0]] not in arr:
                            arr.insert(i, [name, sex, course, completed[0]])


                    pro = pd.DataFrame(arr, columns = ['Student Name', 'Sex', 'Course', 'Completed'])
                    pro.sort_values(by=['Student Name'], inplace=True)


                    # plt.figure(figsize=(10,10), dpi=250)
                    s = plt.figure(figsize=(10,8))

                    g2 = sns.countplot(hue= "Sex",y="Course",  data=pro)

                    for p in g2.patches:
                            percentage = '{:.0f}'.format(p.get_width())
                            x = p.get_x() + p.get_width() + 0.02
                            y = (p.get_y() + p.get_height()/2) + 0.15
                            g2.annotate(percentage, (x, y))
                    
                    plt.yticks(rotation = 45)
                    plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.15), ncol=2)
                    plt.title("Number of students in each courses")
                    plt.xlabel('Number of students')
                    plt.ylabel('Courses')
                    st.write(s) 
                    plt.savefig('images/Number of students in each courses.png')
                    st.markdown(get_image_download_link(s), unsafe_allow_html=True)

                else:
                    md = qr.courseStudent(df,course)
                    totalRecord = md['Sex'].count()
                    if totalRecord > 0:
                        s = plt.figure()
                        # fig, axes = plt.subplots(1, 3)
                        s = plt.figure(figsize=(10,5))
                        g2 = sns.countplot(x="Sex", data=md)

                        for p in g2.patches:
                                percentage = '{:.0f}'.format(p.get_height())
                                x = p.get_x() + p.get_width()/2
                                y = p.get_y() + p.get_height() + 0.4
                                g2.annotate(percentage, (x, y))
                                
                        plt.title("Number of students in each course")
                        plt.xlabel('Gender')
                        plt.ylabel('Number of Students')
                        st.write(s) 
                        st.markdown(get_image_download_link(s), unsafe_allow_html=True)

                

        if question == option_course[2]:
            course = st.selectbox('Select course:',(md['Course Name'].unique()))
            col1,col2 = st.beta_columns(2)

            today = datetime.date.today()
            last14Day = today - timedelta(14)

            with col1:
                startDate = st.date_input("Start date", datetime.date(2020,9,1))
                # startDate = st.date_input("Start date",last14Day)

            with col2:
                endDate = st.date_input("End date", today)
            md = df

            progress = md[(md['State'] == 1) & (md['Completion Date'] >= str(startDate)) & (md['Completion Date'] <= str(endDate)) & (md['Course Name'] == course)]
            # pg = progress.groupby(['Firstname','Course Name']).count()
            # pg[['ID']]
            arr = []
            for i in range(0, len(progress)):
                id = progress.iloc[i][1]
                name = progress.iloc[i][2]
                sex =  progress.iloc[i][3]
                course = progress.iloc[i][6]
                
                completed = progress[progress['Student Name'] == name].count()


                if [id, name, sex,course, completed[0]] not in arr:
                    arr.insert(i, [id, name, sex, course, completed[0]])
                    

            pro = pd.DataFrame(arr, columns = ['ID', 'Student Name', 'Sex', 'Course', 'Completed'])
            pro.sort_values(by=['Student Name'], inplace=True)
            c1, c2 = st.beta_columns(2)
            with c1:
                st.dataframe(data=pro, height=600)
                download_csv(pro)
            with c2:
                import math
                maxLesson = pro['Completed'].max()
                totalRecord = pro['Completed'].count()
                if totalRecord > 0:
                    s = plt.figure(figsize=(10,totalRecord/3)) # 1 inch has 3 record
                    g2 = sns.barplot(y=pro['Student Name'], x= pro['Completed'])

                    for p in g2.patches:
                        percentage = '{:.0f}'.format(p.get_width())

                        x = p.get_x() + p.get_width() + 0.02
                        y = (p.get_y() + p.get_height()/2) + 0.15
                        g2.annotate(percentage, (x, y))

                    x_ticks = np.arange(0, maxLesson + 1, 1)
                    plt.xticks(x_ticks)
                    plt.title("Student Learing Progress")
                    plt.xlabel('Completed Courses')
                    plt.ylabel('Student Name')
                    plt.savefig('images/Student Learning Proress/'+ str(i) +'.png', bbox_inches='tight')
                    s
                    st.markdown(get_image_download_link(s), unsafe_allow_html=True)


        if question == option_course[3]:
            # st.write(df)
            course = st.selectbox('Select course:',(md['Course Name'].unique()))
            col1,col2 = st.beta_columns(2)

            today = datetime.date.today()
            last14Day = today - timedelta(14)

            with col1:
                # startDate = st.date_input('Start date', last14Day)
                startDate = st.date_input("Start date", datetime.date(2020,9,1))
            with col2:
                endDate = st.date_input('End date', today)

            md = df

            progress = md[(md['State'] == 1) & (md['Completion Date'] >= str(startDate)) & (md['Completion Date'] <= str(endDate)) & (md['Course Name'] == course)]

            arr = []
            for i in range(0, len(progress)):
                id = progress.iloc[i][1]
                name = progress.iloc[i][2]
                sex =  progress.iloc[i][3]
                course = progress.iloc[i][6]
                
                completed = progress[progress['Student Name'] == name].count()


                if [id, name, sex,course, completed[0]] not in arr:
                    arr.insert(i, [id, name, sex, course, completed[0]])
                    

            pro = pd.DataFrame(arr, columns = ['ID', 'Student Name', 'Sex', 'Course', 'Completed'])
            c1, c2 = st.beta_columns(2)
            with c1:
                st.dataframe(data=pro, height=600)
            with c2:
                totalRecord = pro['Completed'].count()
                if totalRecord > 0:
                    if totalRecord > 25:
                        s = plt.figure()
                        g2 = sns.barplot(y=pro['Student Name'], x= pro['Completed'])
                                
                        plt.title("Student Learing Progress")
                        plt.xlabel('Completed Courses')
                        plt.ylabel('Student Name')
                        plt.ylim(0, 25)
                        # plt.show()
                        plt.savefig('images/Student Learning Proress/'+ str(i) +'.png', bbox_inches='tight')
                        s
                    else:
                        s = plt.figure()
                        g2 = sns.barplot(y=pro['Student Name'], x= pro['Completed'])
                                
                        plt.title("Student Learing Progress")
                        plt.xlabel('Completed Courses')
                        plt.ylabel('Student Name')
                        # plt.ylim(0, 25)
                        # plt.show()
                        plt.savefig('images/Student Learning Proress/'+ str(i) +'.png', bbox_inches='tight')
                        s 


    if radio_select == 'Student':
        
        st.write('Hi Student')

    if radio_select == 'Completion':
        option_completion = ['Student and Finished Course', 'Completion Summary']
        question = side.features(option_completion)

