#!/usr/bin/env python
# coding: utf-8

# In[355]:


import time
import pandas as pd
import numpy as np
import itertools

start = time.time()

full_tutors = pd.read_csv("tutors.csv")
full_classes = pd.read_csv("classes.csv")
full_students = pd.read_csv("students.csv")


# In[356]:


# minor preprocessing of original dataframes for better organization later
full_tutors = full_tutors.rename(columns={'Name' : 'Tutor', 'Are you interested in Private Tutoring? How many students are you interested in tutoring?' : 'Private Tutoring', 'Which instrument(s) would you like to teach?': 'Instrument', 'Grade levels you prefer to work with:': 'Grade', 'Are you interested in In-Class Tutoring? How many classes would you like to help out with?' : 'Class Tutoring'})
full_classes = full_classes.rename(columns={'Class #1 Name (ex. 5th Grade Strings, 7th Grade Concert Band, etc)': 'Class #1 Name', 'Class #1 Classroom Number (If you do not have a specific room number, please provide a description of where the class is held)': 'Classroom Number #1'})
full_classes = full_classes.rename(columns={'Class #2 Name (ex. 5th Grade Strings, 7th Grade Concert Band, etc)': 'Class #2 Name', 'Class #2 Classroom Number (If you do not have a specific room number, please provide a description of where the class is held)': 'Classroom Number #2'})
full_classes = full_classes.rename(columns={'Class #3 Name (ex. 5th Grade Strings, 7th Grade Concert Band, etc)': 'Class #3 Name', 'Class #3 Classroom Number (If you do not have a specific room number, please provide a description of where the class is held)': 'Classroom Number #3'})
full_students = full_students.rename(columns={'Student Name - Last, First': 'Student'})


# In[357]:


# edit values in Private/Class Tutoring columns to be just number of students (0 - 4)
full_tutors = full_tutors.replace({'Private Tutoring' : {'1 student' : 1, '2 students' : 2, '3 students' : 3, '4 students' : 4, 'No, I am not interested' : 0},
                                  'Class Tutoring' : {'1 class' : 1, '2 classes' : 2, '3 classes' : 3, '4 classes' : 4, 'No, I am not interested' : 0}})
# full_tutors and full_students dataframes will not be mutated after this


# In[358]:


# split students into the 4 priorities 
application = 'Previous application with TMC'
freeLunch = 'Does the student qualify for the free or reduced lunch program?'
prevTutored = 'Yes, my student has previously applied and received lessons with TMC'
prevApplied = 'Yes, my student has applied for lessons with TMC before but was not placed for lessons'
newStudent = 'No, this is my student\'s first time applying for lessons with TMC'

students1 = full_students.loc[(full_students[application] == prevTutored)]
students2 = full_students.loc[(full_students[application] == prevApplied) & (full_students[freeLunch] == 'Yes')]
students3 = full_students.loc[(full_students[application] == newStudent) & (full_students[freeLunch] == 'Yes')]
students4 = full_students.loc[(full_students[application] == prevApplied) & (full_students[freeLunch] == 'No')]
students5 = full_students.loc[(full_students[application] == newStudent) & (full_students[freeLunch] == 'No')]


# In[359]:


#split classes into separate rows
classes1 = full_classes[['Email address','Name', 'School', 'Class #1 Name', 'Class #1 Grade Level', 'Class #1 Instruments (check all that apply)','Class #1 Timings [Monday]', 'Class #1 Timings [Tuesday]', 'Class #1 Timings [Wednesday]', 'Class #1 Timings [Thursday]', 'Class #1 Timings [Friday]', 'Classroom Number #1', 'How specifically would you like the tutors to help you? (ex. one-on-one, sectionals, etc.)', 'Any other requests or concerns that you would like TMC to know?']]
classes2 = full_classes[['Email address','Name', 'School', 'Class #2 Name', 'Class #2 Grade Level', 'Class #2 Instruments (check all that apply)','Class #2 Timings [Monday]', 'Class #2 Timings [Tuesday]', 'Class #2 Timings [Wednesday]', 'Class #2 Timings [Thursday]', 'Class #2 Timings [Friday]', 'Classroom Number #2', 'How specifically would you like the tutors to help you? (ex. one-on-one, sectionals, etc.)', 'Any other requests or concerns that you would like TMC to know?']]
classes3 = full_classes[['Email address','Name', 'School', 'Class #3 Name', 'Class #3 Grade Level', 'Class #3 Instruments (check all that apply)','Class #3 Timings [Monday]', 'Class #3 Timings [Tuesday]', 'Class #3 Timings [Wednesday]', 'Class #3 Timings [Thursday]', 'Class #3 Timings [Friday]', 'Classroom Number #3', 'How specifically would you like the tutors to help you? (ex. one-on-one, sectionals, etc.)', 'Any other requests or concerns that you would like TMC to know?']]
new_cols = {x: y for x, y in zip(classes2.columns, classes1.columns)}
classes1 = classes1.append(classes2.rename(columns=new_cols), ignore_index = True)
new_cols = {x: y for x, y in zip(classes3.columns, classes1.columns)}
classes1 = classes1.append(classes3.rename(columns=new_cols), ignore_index = True)
classes1 = classes1[classes1['Class #1 Name'].isna() == False].reset_index(drop=True)
full_classes = classes1.rename({'Class #1 Name': 'Class Name', 'Class #1 Grade Level': 'Grade Level','Class #1 Instruments (check all that apply)': 'Instruments', 'Class #1 Timings [Monday]': 'Monday', 'Class #1 Timings [Tuesday]': 'Tuesday', 'Class #1 Timings [Wednesday]': 'Wednesday', 'Class #1 Timings [Thursday]': 'Thursday', 'Class #1 Timings [Friday]':'Friday', 'Classroom Number #1': 'Classroom Number'},axis=1)
full_classes['id'] = full_classes.index
full_classes


# In[360]:


# more useful arrays
student = ['Student']
choices = ['Instrument (First Choice)', 'Instrument (Second Choice)', 'Instrument (Third Choice)']
grade = ['Grade Level']

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
times = ['Before 11am', '11am-1pm', '1pm-3pm', '3pm-5pm', "After 5pm"]
daystimes = [day + ' ' + time for day in days for time in times]

class_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
class_times = ['8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', 'After 4PM']
class_daystimes = [day + ' ' + time for day in class_days for time in class_times]

rangeToList = {'Before 11am': '8AM, 9AM, 10AM', '11am-1pm':'11AM, 12PM', '1pm-3pm':'1PM, 2PM', '3pm-5pm':'3PM, After 4PM', "After 5pm":'After 4PM'}


# In[361]:


"""
Function to preprocess the given dataframe.
Arguments: data - raw dataframe (read from tutors.csv or students.csv)
           status - 'students' or 'tutors'
Returns: new dataframe with only the necessary columns for matching
"""
def preprocess(data, status):
    # filter out irrelevant columns, remove/replace invalid data entries
    data = data.replace(np.nan, '')
    if status == 'students':
        data = data[student + choices + days + grade]
        # consolidate all instruments into one column, in the order of preference
        data['Instrument'] = data[choices].agg(', '.join, axis=1)
        data = data.drop(choices, 1)
        data = data.rename(columns={'Grade Level': 'Grade'})
        
    elif status == 'tutors':
        data = data[['Tutor', 'Instrument'] + days + ['Grade', 'Private Tutoring']]
        
    # standardize instrument name to be lowercase
    data['Instrument'] = data['Instrument'].str.lower()
    
    # extract day/time availabilities into separate columns
    index = 0
    for i in range(len(days)):
        for j in range(len(times)):
            d = days[i]
            t = times[j]
            data[daystimes[index]] = data[d].str.contains(t)
            index += 1
    
    # keep only day, time combination columns in dataframe
    data = data.drop(days, 1)
    
    # add column for number of availabilities
    temp = data[daystimes]
    temp['Count'] = temp.sum(1)
    data['Count'] = temp['Count']
    data = data.sort_values(by='Count')
    
    return data


# In[362]:


"""
Function to preprocess the given dataframe.
Arguments: data - raw dataframe (read from tutors.csv or students.csv)
Returns: new dataframe with only the necessary columns for matching
"""
def preprocess_for_classes(data):
    # filter out irrelevant columns, remove/replace invalid data entries
    data = data.replace(np.nan, '')

    data = data[['Tutor', 'Instrument'] + days + ['Grade', 'Class Tutoring']]
    
    data['Monday'] = data['Monday'].str.replace('Before 11am', '8AM, 9AM, 10AM')
    
    # standardize instrument name to be lowercase
    data['Instrument'] = data['Instrument'].str.lower()
    
    index = 0
    for i in range(len(days)):
        for j in range(len(times)):
            d = days[i]
            t = times[j]
            data[d] = data[d].str.replace(t, rangeToList[t])
            index += 1
    data = data.drop(['Saturday', 'Sunday'],1)
    data = extract_times(data)

    return data[data['Class Tutoring'] > 0]

def extract_times(data):
    # extract day/time availabilities into separate columns
    data = data.replace(np.nan, '')
    
    index = 0
    for i in range(len(class_days)):
        for j in range(len(class_times)):
            d = class_days[i]
            t = class_times[j]
            data[class_daystimes[index]] = data[d].str.contains(t)
            index += 1
    
    # keep only day, time combination columns in dataframe
    data = data.drop(class_days, 1)
    
    # add column for number of availabilities
    temp = data[class_daystimes]
    temp['Count'] = temp.sum(1)
    data['Count'] = temp['Count']
    data = data.sort_values(by='Count')
    data = data.drop('Count', axis=1)
    return data


# In[363]:


# create dataframes to use for matching
pd.set_option('mode.chained_assignment', None)
tutors = preprocess(full_tutors, 'tutors')
# students = preprocess(full_students, 'students')

students1 = preprocess(students1, 'students')
students2 = preprocess(students2, 'students')
students3 = preprocess(students3, 'students')
students4 = preprocess(students4, 'students')
students5 = preprocess(students5, 'students')

# all students, in order of priority level and least to most available
students = pd.concat([students1, students2, students3, students4, students5])

#class matching
tutors_for_classes = preprocess_for_classes(full_tutors)
full_classes['Instruments'] = full_classes['Instruments'].str.lower()
classes = extract_times(full_classes)


# In[364]:


# copies to mutate in function; tutors will be removed once they are fully matched
tutors2 = tutors[tutors['Private Tutoring'] > 0]


# In[365]:


"""
Takes in a student in the form of a tuple with (length, Series) -- values from a df.iterrows() iterable.
Returns a list of matched tutor, instrument, and time slots, or a list of Nones if no match can be created.
Matches are considered valid if there is an instrument overlap between student and tutor, and at least one time availability overlap.
"""
def match(student):
    student_info = student[1]
    # remove empty strings from student's instruments choice (i.e. if student has less than 3 preferences)
    student_instruments = list(filter(None, student_info['Instrument'].split(', ')))
    student_grade = student_info['Grade']
    
    t_without_count = tutors2.drop(columns='Count')
        
    # iterate through student's instruments, beginning with first choice
    for instrument in student_instruments:
        # iterate through all remaining tutors, searching for a match with specific instrument choice
        for tutor in t_without_count.iterrows():
            tutor_info = tutor[1]
            tutor_instruments = tutor_info['Instrument']
            tutor_grade = list(filter(None, tutor_info['Grade'].split(', ')))
            # merge into one Series with values as lists of [tutor value, student value]
            combined_info = tutor_info.combine(student_info, lambda x, y: [x, y])
            # times where both tutor and student are available
            times = [t for t in combined_info.index if combined_info[t] == [True, True]]
            
            #brute force grade preference
            if instrument in tutor_instruments and len(times) > 0 and student_grade in tutor_grade:
                return [tutor_info[0], instrument, times]
        
        for tutor in t_without_count.iterrows():
            tutor_info = tutor[1]
            tutor_instruments = tutor_info['Instrument']
            tutor_grade = list(filter(None, tutor_info['Grade'].split(', ')))
            # merge into one Series with values as lists of [tutor value, student value]
            combined_info = tutor_info.combine(student_info, lambda x, y: [x, y])
            # times where both tutor and student are available
            times = [t for t in combined_info.index if combined_info[t] == [True, True]]
            
            # if instrument matches and there is at least one shared time availability
            if instrument in tutor_instruments and len(times) > 0:
                return [tutor_info[0], instrument, times]
    
    # no match found for any of the three instrument choices
    return [None, None, None]


# In[366]:


"""
Takes in a class in the form of a tuple with (length, Series) -- values from a df.iterrows() iterable.
Returns a list of matched tutor, instrument, and time slots, or a list of Nones if no match can be created.
Matches are considered valid if there is an instrument overlap between student and tutor, and at least one time availability overlap.
"""
def match_classes(classes):
    class_info = classes[1]
    class_id = class_info['id']
    # remove empty strings from student's instruments choice (i.e. if student has less than 3 preferences)
    class_instruments = list(filter(None, class_info['Instruments'].split(', ')))
    class_grade = class_info['Grade Level']
        
    # iterate through classes instruments, beginning with first choice
    for instrument in class_instruments:
        # iterate through all remaining tutors, searching for a match with specific instrument choice
        for tutor in tutors_for_classes.iterrows():
            tutor_info = tutor[1]
            tutor_instruments = tutor_info['Instrument']
            tutor_grade = list(filter(None, tutor_info['Grade'].split(', ')))
            # merge into one Series with values as lists of [tutor value, student value]
            combined_info = tutor_info.combine(class_info, lambda x, y: [x, y])
            # times where both tutor and student are available
            times = [t for t in combined_info.index if combined_info[t] == [True, True]]
            
            #brute force grade preference
            if instrument in tutor_instruments and len(times) > 0 and class_grade == tutor_grade:
                return [tutor_info[0], instrument, times, class_id]
        
        for tutor in tutors_for_classes.iterrows():
            tutor_info = tutor[1]
            tutor_instruments = tutor_info['Instrument']
            tutor_grade = list(filter(None, tutor_info['Grade'].split(', ')))
            # merge into one Series with values as lists of [tutor value, student value]
            combined_info = tutor_info.combine(class_info, lambda x, y: [x, y])
            # times where both tutor and student are available
            times = [t for t in combined_info.index if combined_info[t] == [True, True]]
            
            # if instrument matches and there is at least one shared time availability
            if instrument in tutor_instruments and len(times) > 0:
                return [tutor_info[0], instrument, times, class_id]
    
    # no match found for any of the three instrument choices
    return [None, None, None, None]


# In[367]:


# create the iterator from rows of students
s_without_count = students.drop(columns='Count')
students_iter = s_without_count.iterrows()


# In[368]:


# create the dataframe to store matches once made
matches = pd.DataFrame(columns=['Student', 'Tutor', 'Instrument', 'Time(s)'])
class_matches = pd.DataFrame(columns=['Class', 'Tutor', 'Instrument', 'Time(s)', 'id'])


# In[369]:


# iterate through students; use function defined above to get a match
for c in classes.iterrows():
    m = match_classes(c)
    # add to matches dataframe
    class_matches.loc[len(class_matches)] = [c[1][0]] + m
    # remove tutor if successfully matched
    if m[0] is not None:
        tutor_idx = tutors_for_classes[tutors_for_classes['Tutor'] == m[0]].index[0]
        tutors_for_classes.at[tutor_idx, 'Class Tutoring'] -= 1
        if tutors_for_classes.at[tutor_idx, 'Class Tutoring'] == 0:
            tutors_for_classes = tutors_for_classes.drop(tutors_for_classes[tutors_for_classes['Tutor'] == m[0]].index)
        else:
            # move tutor row to end of tutors_for_classes dataframe
            idx = tutors_for_classes.index.tolist()
            idx.remove(tutor_idx)
            tutors_for_classes = tutors_for_classes.reindex(idx + [tutor_idx])
            tutors_for_classes.at[tutor_idx,m[2][0]] = False
class_matches


# In[370]:


timesToTutors = {' 8AM': ' Before 11am', ' 9AM': ' Before 11am', '10AM':'Before 11am', '11AM':'11am-1pm', '12PM':'11am-1pm', ' 1PM':' 1pm-3pm', ' 2PM':' 1pm-3pm', ' 3PM':' 3pm-5pm', ' 4PM':' 5pm'}
class_match_2 = class_matches.copy()
tutorNames = tutors2['Tutor'].values

for r in class_match_2.iterrows():
    if r[1][3] is None:
        continue
    for i in range(len(r[1][3])):
        t = r[1][3][i]
        key = t[-4:]
        if key in timesToTutors:
            r[1][3][i] = t[:-4]
            r[1][3][i] += timesToTutors[key]
        
    if r[1][1] in tutorNames:
        for t in r[1][3]:
            tutors2.at[r[1][1]==tutors2['Tutor'],t] = False
            
        
class_match_2


# In[371]:


# iterate through students; use function defined above to get a match
for s in students_iter:
    m = match(s)
    # add to matches dataframe
    matches.loc[len(matches)] = [s[1][0]] + m
    # remove tutor if fully matched
    if m[0] is not None:
        tutor_idx = tutors2[tutors2['Tutor'] == m[0]].index[0]
        tutors2.at[tutor_idx, 'Private Tutoring'] -= 1
        if tutors2.at[tutor_idx, 'Private Tutoring'] == 0:
            tutors2 = tutors2.drop(tutors2[tutors2['Tutor'] == m[0]].index)
        else:
            # move tutor row to end of tutors2 dataframe
            idx = tutors2.index.tolist()
            idx.remove(tutor_idx)
            tutors2 = tutors2.reindex(idx + [tutor_idx])
            tutors2.at[tutor_idx,m[2][0]] = False


# In[372]:


# matched students
matched = matches[matches['Tutor'].notna()]
matched


# In[373]:


# unmatched students
no_match = matches[matches['Tutor'].isna()]
no_match


# In[374]:


# unmatched tutors
tutors2[['Tutor', 'Instrument', 'Count', 'Private Tutoring']]


# In[297]:


# matches with relevant information (add any columns needed)
matched = matched.merge(full_students[['Student', 'Email Address', 'Grade Level', 'Parent / Guardian Name(s) - Last, First', 'Phone Number - (111) 111 - 1111']], on='Student', how='left')
matched = matched.merge(full_tutors[['Tutor', 'Email', 'Phone Number']], on='Tutor', how='left')
matched = matched.rename(columns={'Email Address' : 'Student Email', 'Email' : 'Tutor Email', 'Phone Number - (111) 111 - 1111': 'Student Phone Number', 'Phone Number':'Tutor Phone Number'})
student_matched = matched.to_csv()


# In[382]:


class_matched = class_matches[class_matches['Tutor'].notna()]
class_matched = class_matched.merge(full_classes[['Name', 'School', 'Grade Level', 'Class Name', 'Classroom Number', 'How specifically would you like the tutors to help you? (ex. one-on-one, sectionals, etc.)', 'Any other requests or concerns that you would like TMC to know?','id']], on='id', how='left')
class_matched = class_matched.merge(full_tutors[['Tutor', 'Email', 'Phone Number']], on='Tutor', how='left')
class_matched = class_matched.rename(columns={'Email Address' : 'Student Email', 'Email' : 'Tutor Email', 'Name': 'Teacher Name', 'Phone Number':'Tutor Phone Number'})
class_matched = class_matched.drop('id', axis=1)
class_match = class_matched.to_csv()
class_matched


# In[375]:


full_classes


# In[180]:


# students with no matches with relevant information (add any columns needed)
no_match = no_match.merge(full_students[['Student', 'Email Address']], on='Student', how='left')
no_match = no_match.rename(columns={'Email Address' : 'Student Email'}).drop(['Tutor', 'Instrument', 'Time(s)'], 1)
no_match


# In[181]:


# time for computation (in seconds):

# In[ ]:





# In[ ]:




