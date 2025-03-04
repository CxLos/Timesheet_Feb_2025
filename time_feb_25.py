# =================================== IMPORTS ================================= #
import numpy as np 
import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px
import os
import sys
import dash
from dash import dcc, html
# 'data/~$bmhc_data_2024_cleaned.xlsx'
# print('System Version:', sys.version)
# -------------------------------------- DATA ------------------------------------------- #

current_dir = os.getcwd()
current_file = os.path.basename(__file__)
script_dir = os.path.dirname(os.path.abspath(__file__))

data_nav = 'data/Navigation_Responses.xlsx'
data_eng = 'data/Engagement_Responses.xlsx'
data_mc = 'data/MarCom_Responses.xlsx'
data_it = 'data/IT_Responses.xlsx'

file_path_nav = os.path.join(script_dir, data_nav)
file_path_eng = os.path.join(script_dir, data_eng)
file_path_mc = os.path.join(script_dir, data_mc)
file_path_it = os.path.join(script_dir, data_it)

data_nav = pd.read_excel(file_path_nav)
data_eng = pd.read_excel(file_path_eng)
data_mc = pd.read_excel(file_path_mc)
data_it = pd.read_excel(file_path_it)

df_nav = data_nav.copy()
df_eng = data_eng.copy()
df_mc = data_mc.copy()
df_it = data_it.copy()

# Trim leading and trailing whitespaces from column names for all dataframes
df_nav.columns = df_nav.columns.str.strip()
df_eng.columns = df_eng.columns.str.strip()
df_mc.columns = df_mc.columns.str.strip()
df_it.columns = df_it.columns.str.strip()

# Trim whitespace from values in all columns in all dataframes
df_nav = df_nav.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df_eng = df_eng.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df_mc = df_mc.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df_it = df_it.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Convert 'Date of Activity' to datetime format
df_nav['Date of Activity'] = pd.to_datetime(df_nav['Date of Activity'], errors='coerce')
df_eng['Date of Activity'] = pd.to_datetime(df_eng['Date of Activity'], errors='coerce')
df_mc['Date of Activity'] = pd.to_datetime(df_mc['Date of Activity'], errors='coerce')
df_it['Date of Activity'] = pd.to_datetime(df_it['Date of Activity'], errors='coerce')

# FIRST HALF
df_nav1 = df_nav[(df_nav['Date of Activity'] >= "2025-02-01") & (df_nav['Date of Activity'] <= "2025-02-14")]
df_eng1 = df_eng[(df_eng['Date of Activity'] >= "2025-02-01") & (df_eng['Date of Activity'] <= "2025-02-14")]
df_mc1 = df_mc[(df_mc['Date of Activity'] >= "2025-02-01") & (df_mc['Date of Activity'] <= "2025-02-14")]
df_it1 = df_it[(df_it['Date of Activity'] >= "2025-02-01") & (df_it['Date of Activity'] <= "2025-02-14")]

# SECOND HALF
df_nav2 = df_nav[(df_nav['Date of Activity'] >= "2025-02-15") & (df_nav['Date of Activity'] <= "2025-02-28")]
df_eng2 = df_eng[(df_eng['Date of Activity'] >= "2025-02-15") & (df_eng['Date of Activity'] <= "2025-02-28")]
df_mc2 = df_mc[(df_mc['Date of Activity'] >= "2025-02-15") & (df_mc['Date of Activity'] <= "2025-02-28")]
df_it2 = df_it[(df_it['Date of Activity'] >= "2025-02-15") & (df_it['Date of Activity'] <= "2025-02-28")]

# Rename "Activity Duration (hours):" to "Hours"
# df_it1['Hours'] = pd.to_numeric(df_it1['Activity Duration (hours):'], errors='coerce')

# Rename "Activity Duration (hours):" to "Hours" for all dataframes
for df in [df_mc1, df_mc2, df_it1, df_it2]:
    df['Hours'] = pd.to_numeric(df['Activity Duration (hours):'], errors='coerce')
    
# for df in [df_nav1, df_nav2]:
#     df['Hours'] = pd.to_numeric(df['Activity Duration (hours)'], errors='coerce')
    
for df in [df_eng1, df_eng2, df_nav1, df_nav2]:
    if 'Activity Duration (minutes):' in df.columns:
        df['Hours'] = pd.to_numeric(df['Activity Duration (minutes):'], errors='coerce') / 60
    # else:
    #     print(f"Column 'Activity Duration (minutes):' not found in dataframe. Available columns: {df.columns}")

 

# print(df.head(10))
# print('Total Marketing Events: ', len(df))
# print('Column Names: \n', df_nav1.columns)
# print('DF Shape:', df.shape)
# print('Dtypes: \n', df.dtypes)
# print('Info:', df.info())
# print("Amount of duplicate rows:", df.duplicated().sum())

# print('Current Directory:', current_dir)
# print('Script Directory:', script_dir)
# print('Path to data:',file_path)

# ================================= Columns ================================= #



# =============================== Missing Values ============================ #

# missing = df.isnull().sum()
# print('Columns with missing values before fillna: \n', missing[missing > 0])

# ============================== Data Preprocessing ========================== #

# Check for duplicate columns
# duplicate_columns = df.columns[df.columns.duplicated()].tolist()
# print(f"Duplicate columns found: {duplicate_columns}")
# if duplicate_columns:
#     print(f"Duplicate columns found: {duplicate_columns}")

# --------------------------- Navigation Hours --------------------------- #

# print(df_nav.columns)

# Index(['Timestamp', 'Date of Activity', 'Person filling out this form:',
#        'Activity duration (minutes):', 'Location Encountered:',
#        'Individual's First Name:', 'Individual's Date of Birth:',
#        'Individual's Insurance Status:', 'Individual's street address:',
#        'City:', 'ZIP Code:', 'County:', 'Type of support given:',
#        'Provide brief support description:', 'Individual's Status:',
#        'HMIS SPID Number:', 'MAP Card Number', 'Gender:', 'Race/Ethnicity:',
#        'Total travel time (minutes):', 'Direct Client Assistance Amount:',
#        'Column 21', 'Individual's Last Name:'],

# Create a dataframe where you count the total minutes under "Activity duration (minutes): grouped by "Person filling out this form:"

# Group by 'Person filling out this form:' and sum the 'Activity duration (minutes):'
# Group by 'Person filling out this form:' and sum the 'Activity duration (minutes):'
nav_hours1 = df_nav1.groupby('Person submitting this form:')['Hours'].sum().reset_index()

# nav_hours1['Activity duration (hours):'] = nav_hours1['Activity duration (minutes):'] / 60

# Optional: Sort the results by total activity duration, descending
# nav_hours1 = nav_hours1.sort_values(by='Hours', ascending=False)

# Display the grouped DataFrame
# print(activity_duration_grouped)

# Bar Chart for Activity Duration by Person
nav_hours_bar1 = px.bar(
    nav_hours1,
    x="Person submitting this form:",
    y='Hours',  # Now using hours
    color="Person submitting this form:",
    text='Hours', 
).update_layout(
    height=450, 
    width=900,
    title=dict(
        text='Navigation Hours by Person',
        x=0.5, 
        font=dict(
            size=25,
            family='Calibri',
            color='black',
        )
    ),
    font=dict(
        family='Calibri',
        size=18,
        color='black'
    ),
    xaxis=dict(
        tickangle=-20,  # Rotate x-axis labels for better readability
        tickfont=dict(size=18),  # Adjust font size for the tick labels
        title=dict(
            text="Person",
            font=dict(size=20),  # Font size for the title
        ),
        showticklabels=True  # Show x-tick labels
    ),
    yaxis=dict(
        title=dict(
            text='Hours',
            font=dict(size=20),  # Font size for the title
        ),
    ),
    legend=dict(
        title='Person',
        orientation="v",  # Vertical legend
        x=1.05,  # Position legend to the right
        y=1,  # Position legend at the top
        xanchor="left",  # Anchor legend to the left
        yanchor="top",  # Anchor legend to the top
        # visible=False  # Ensure the legend is visible
        visible=True  # Ensure the legend is visible
    ),
    hovermode='closest',  # Display only one hover label per trace
    bargap=0.08,  # Reduce the space between bars
    bargroupgap=0,  # Reduce space between individual bars in groups
).update_traces(
    textposition='auto',  # Show text labels inside bars
    hovertemplate='<b>Person:</b> %{x}<br><b>Activity Duration:</b> %{y} hours<extra></extra>'  # Fixed hovertemplate
)

# Location Pie Chart
nav_hours_pie1 = px.pie(
    nav_hours1,  # Use the grouped data for the pie chart
    names="Person submitting this form:",
    values='Hours'  # Show activity duration in hours
).update_layout(
    title='Ratio of Hours by Person',
    title_x=0.5,
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    )
).update_traces(
    rotation=90,
    textinfo='value+percent',
    hovertemplate='<b>%{label}</b>: %{value} hours<extra></extra>'  # Updated hovertemplate to show hours
)

# Table
nav_table1 = go.Figure(data=[go.Table(
    # columnwidth=[50, 50, 50],  # Adjust the width of the columns
    header=dict(
        values=list(nav_hours1.columns),
        fill_color='paleturquoise',
        align='center',
        height=30,  # Adjust the height of the header cells
        # line=dict(color='black', width=1),  # Add border to header cells
        font=dict(size=12)  # Adjust font size
    ),
    cells=dict(
        values=[nav_hours1[col] for col in nav_hours1.columns],
        fill_color='lavender',
        align='left',
        height=25,  # Adjust the height of the cells
        # line=dict(color='black', width=1),  # Add border to cells
        font=dict(size=12)  # Adjust font size
    )
)])

nav_table1.update_layout(
    margin=dict(l=50, r=50, t=30, b=40),  # Remove margins
    height=400,
    width=500,  # Set a smaller width to make columns thinner
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
    plot_bgcolor='rgba(0,0,0,0)'  # Transparent plot area
)

# --------------------- Navigation Hours 2 --------------------- #

# Group by 'Person filling out this form:' and sum the 'Activity duration (minutes):'
nav_hours2 = df_nav2.groupby('Person submitting this form:')['Hours'].sum().reset_index()

# nav_hours2['Activity duration (hours):'] = nav_hours2['Activity duration (minutes):'] / 60

# Optional: Sort the results by total activity duration, descending
# nav_hours2 = nav_hours2.sort_values(by='Hours', ascending=False)

# Display the grouped DataFrame
# print(activity_duration_grouped)

# Bar Chart for Activity Duration by Person
nav_hours_bar2 = px.bar(
    nav_hours2,
    x="Person submitting this form:",
    y='Hours',  # Now using hours
    color="Person submitting this form:",
    text='Hours',  # Display the activity duration in hours
).update_layout(
    height=450, 
    width=900,
    title=dict(
        text='Navigation Hours by Person',
        x=0.5, 
        font=dict(
            size=25,
            family='Calibri',
            color='black',
        )
    ),
    font=dict(
        family='Calibri',
        size=18,
        color='black'
    ),
    xaxis=dict(
        tickangle=-20,  # Rotate x-axis labels for better readability
        tickfont=dict(size=18),  # Adjust font size for the tick labels
        title=dict(
            text="Person",
            font=dict(size=20),  # Font size for the title
        ),
        showticklabels=True  # Show x-tick labels
    ),
    yaxis=dict(
        title=dict(
            text='Hours',
            font=dict(size=20),  # Font size for the title
        ),
    ),
    legend=dict(
        title='Person',
        orientation="v",  # Vertical legend
        x=1.05,  # Position legend to the right
        y=1,  # Position legend at the top
        xanchor="left",  # Anchor legend to the left
        yanchor="top",  # Anchor legend to the top
        # visible=False  # Ensure the legend is visible
        visible=True  # Ensure the legend is visible
    ),
    hovermode='closest',  # Display only one hover label per trace
    bargap=0.08,  # Reduce the space between bars
    bargroupgap=0,  # Reduce space between individual bars in groups
).update_traces(
    textposition='auto',  # Show text labels inside bars
    hovertemplate='<b>Person:</b> %{x}<br><b>Activity Duration:</b> %{y} hours<extra></extra>'  # Fixed hovertemplate
)

# Location Pie Chart
nav_hours_pie2 = px.pie(
    nav_hours2,  # Use the grouped data for the pie chart
    names="Person submitting this form:",
    values='Hours'  # Show activity duration in hours
).update_layout(
    title='Ratio of Hours by Person',
    title_x=0.5,
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    )
).update_traces(
    rotation=20,
    textinfo='value+percent',
    hovertemplate='<b>%{label}</b>: %{value} hours<extra></extra>'  # Updated hovertemplate to show hours
)

# Table
nav_table2 = go.Figure(data=[go.Table(
    # columnwidth=[50, 50, 50],  # Adjust the width of the columns
    header=dict(
        values=list(nav_hours2.columns),
        fill_color='paleturquoise',
        align='center',
        height=30,  # Adjust the height of the header cells
        # line=dict(color='black', width=1),  # Add border to header cells
        font=dict(size=12)  # Adjust font size
    ),
    cells=dict(
        values=[nav_hours2[col] for col in nav_hours2.columns],
        fill_color='lavender',
        align='left',
        height=25,  # Adjust the height of the cells
        # line=dict(color='black', width=1),  # Add border to cells
        font=dict(size=12)  # Adjust font size
    )
)])

nav_table2.update_layout(
    margin=dict(l=50, r=50, t=30, b=40),  # Remove margins
    height=400,
    width=500,  # Set a smaller width to make columns thinner
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
    plot_bgcolor='rgba(0,0,0,0)'  # Transparent plot area
)

# ---------------------------- MarCom Hours ------------------------------ #

# print(df_mc.columns)

# Index(['Timestamp',
#        'Which MarCom activity category are you submitting an entry for?',
#        'Person completing this form:', 'Activity duration (hours):',
#        'Purpose of the activity (please only list one):',
#        'Please select the type of product(s):',
#        'Please provide public information:', 'Please explain event-oriented:',
#        'Date of Activity', 'Brief activity description:', 'Activity Status',
#        'Total travel time (minutes):', 'Please provide public information:.1',
#        'Please explain event-oriented:.1'],
#       dtype='object')

# Convert 'Activity duration (hours):' to numeric, coercing errors to NaN
# df_mc1['Activity duration (hours):'] = pd.to_numeric(df_mc1['Activity duration (hours):'], errors='coerce')

# Group by 'Person completing this form:' and sum the 'Activity duration (hours):'
mc_hours1 = df_mc1.groupby('Person submitting this form:')['Hours'].sum().reset_index()

# Optional: Sort the results by total activity duration (in hours), descending
mc_hours1 = mc_hours1.sort_values(by='Hours', ascending=False)

# Bar Chart for Activity Duration by Person
mc_hours_bar1 = px.bar(
    mc_hours1,
    x="Person submitting this form:",
    y='Hours',
    color="Person submitting this form:",
    text='Hours',
).update_layout(
    height=450, 
    width=900,
    title=dict(
        text='Total MarCom Hours by Person (First Half)',
        x=0.5, 
        font=dict(size=25, family='Calibri', color='black'),
    ),
    font=dict(family='Calibri', size=18, color='black'),
    xaxis=dict(
        tickangle=-20,
        tickfont=dict(size=18),
        title=dict(text="Person", font=dict(size=20)),
        showticklabels=True
    ),
    yaxis=dict(
        title=dict(text='Hours', font=dict(size=20)),
    ),
    legend=dict(
        title='Person',
        orientation="v",
        x=1.05,
        y=1,
        xanchor="left",
        yanchor="top",
        visible=True
    ),
    hovermode='closest',
    bargap=0.08,
    bargroupgap=0,
).update_traces(
    textposition='auto',
    hovertemplate='<b>Person:</b> %{x}<br><b>Activity Duration:</b> %{y} hours<extra></extra>'
)

# Pie Chart for Activity Duration by Person
mc_hours_pie1 = px.pie(
    mc_hours1,
    names="Person submitting this form:",
    values='Hours'
).update_layout(
    title='Ratio of MarCom Hours by Person (First Half)',
    title_x=0.5,
    font=dict(family='Calibri', size=17, color='black')
).update_traces(
    rotation=90,
    textinfo='value+percent',
    hovertemplate='<b>%{label}</b>: %{value} hours<extra></extra>'
)

# Table
mc_table1 = go.Figure(data=[go.Table(
    header=dict(
        values=list(mc_hours1.columns),
        fill_color='paleturquoise',
        align='center',
        height=30,
        font=dict(size=12)
    ),
    cells=dict(
        values=[mc_hours1[col] for col in mc_hours1.columns],
        fill_color='lavender',
        align='left',
        height=25,
        font=dict(size=12)
    )
)])

mc_table1.update_layout(
    margin=dict(l=50, r=50, t=30, b=40),
    height=400,
    width=500,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)


# ---------------------------- MarCom Hours ------------------------------ #

# Convert 'Activity duration (hours):' to numeric, coercing errors to NaN
# df_mc2['Activity duration (hours):'] = pd.to_numeric(df_mc2['Activity duration (hours):'], errors='coerce')

# Group by 'Person completing this form:' and sum the 'Activity duration (hours):'
mc_hours2 = df_mc2.groupby('Person submitting this form:')['Hours'].sum().reset_index()

# Optional: Sort the results by total activity duration (in hours), descending
mc_hours2 = mc_hours2.sort_values(by='Hours', ascending=False)

# Display the grouped DataFrame
# print(mc_hours)

# Bar Chart for Activity Duration by Person
mc_hours_bar2 = px.bar(
    mc_hours2,  # Use the grouped data for the bar chart
    x="Person submitting this form:",  # X-axis as the person completing the form
    y='Hours',  # Now using hours
    color="Person submitting this form:",  # Color by the person completing the form
    text='Hours',  # Display the activity duration in hours
).update_layout(
    height=450, 
    width=900,
    title=dict(
        text='Total MarCom Hours by Person',
        x=0.5, 
        font=dict(
            size=25,
            family='Calibri',
            color='black',
        )
    ),
    font=dict(
        family='Calibri',
        size=18,
        color='black'
    ),
    xaxis=dict(
        tickangle=-20,  # Rotate x-axis labels for better readability
        tickfont=dict(size=18),  # Adjust font size for the tick labels
        title=dict(
            text="Person",
            font=dict(size=20),  # Font size for the title
        ),
        showticklabels=True  # Show x-tick labels
    ),
    yaxis=dict(
        title=dict(
            text='Hours',
            font=dict(size=20),  # Font size for the title
        ),
    ),
    legend=dict(
        title='Person',
        orientation="v",  # Vertical legend
        x=1.05,  # Position legend to the right
        y=1,  # Position legend at the top
        xanchor="left",  # Anchor legend to the left
        yanchor="top",  # Anchor legend to the top
        # visible=True  # Ensure the legend is visible
        visible=True  # Ensure the legend is visible
    ),
    hovermode='closest',  # Display only one hover label per trace
    bargap=0.08,  # Reduce the space between bars
    bargroupgap=0,  # Reduce space between individual bars in groups
).update_traces(
    textposition='auto',  # Show text labels inside bars
    hovertemplate='<b>Person:</b> %{x}<br><b>Activity Duration:</b> %{y} hours<extra></extra>'  # Fixed hovertemplate
)

# Pie Chart for Activity Duration by Person
mc_hours_pie2 = px.pie(
    mc_hours2,  # Use the grouped data for the pie chart
    names="Person submitting this form:",  # Names as the person completing the form
    values='Hours'  # Show activity duration in hours
).update_layout(
    title='Ratio of MarCom Hours by Person',
    title_x=0.5,
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    )
).update_traces(
    rotation=90,
    textinfo='value+percent',
    hovertemplate='<b>%{label}</b>: %{value} hours<extra></extra>'  # Updated hovertemplate to show hours
)

# Table
mc_table2 = go.Figure(data=[go.Table(
    # columnwidth=[50, 50, 50],  # Adjust the width of the columns
    header=dict(
        values=list(mc_hours2.columns),
        fill_color='paleturquoise',
        align='center',
        height=30,  # Adjust the height of the header cells
        # line=dict(color='black', width=1),  # Add border to header cells
        font=dict(size=12)  # Adjust font size
    ),
    cells=dict(
        values=[mc_hours2[col] for col in mc_hours2.columns],
        fill_color='lavender',
        align='left',
        height=25,  # Adjust the height of the cells
        # line=dict(color='black', width=1),  # Add border to cells
        font=dict(size=12)  # Adjust font size
    )
)])

mc_table2.update_layout(
    margin=dict(l=50, r=50, t=30, b=40),  # Remove margins
    height=400,
    width=500,  # Set a smaller width to make columns thinner
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
    plot_bgcolor='rgba(0,0,0,0)'  # Transparent plot area
)

# -------------------------- Engagement Hours ------------------------------ #

# print(df_eng.columns)

# Index(['Timestamp', 'Date of Activity', 'Person submitting this form:',
#        'Activity Duration (minutes):', 'Care Network Activity:',
#        'Entity name:', 'Brief Description:', 'Activity Status:',
#        'BMHC Administrative Activity:', 'Total travel time (minutes):',
#        'Community Outreach Activity:',
#        'Number engaged at Community Outreach Activity:'],

# Convert 'Activity Duration (minutes):' to numeric, forcing errors to NaN (in case of non-numeric data)
# Convert 'Activity Duration (minutes):' to numeric, coercing errors to NaN
# df_eng1['Activity Duration (minutes):'] = pd.to_numeric(df_eng1['Activity Duration (minutes):'], errors='coerce')

# Group by 'Person submitting this form:' and sum the 'Activity Duration (minutes):'
eng_hours1 = df_eng1.groupby('Person submitting this form:')['Hours'].sum().reset_index()

# Convert minutes to hours
# eng_hours1['Activity Duration (hours):'] = eng_hours1['Activity Duration (minutes):'] / 60

# Sort the results by total activity duration (in hours), descending
# eng_hours1 = eng_hours1.sort_values(by='Hours', ascending=False)

# Bar Chart for Activity Duration by Person
eng_hours_bar1 = px.bar(
    eng_hours1,
    x="Person submitting this form:",
    y='Hours',
    color="Person submitting this form:",
    text='Hours',
).update_layout(
    height=450, 
    width=900,
    title=dict(
        text='Engagement Hours by Person',
        x=0.5, 
        font=dict(size=25, family='Calibri', color='black'),
    ),
    font=dict(family='Calibri', size=18, color='black'),
    xaxis=dict(
        tickangle=-20,
        tickfont=dict(size=18),
        title=dict(text="Person", font=dict(size=20)),
        showticklabels=True
    ),
    yaxis=dict(
        title=dict(text='Hours', font=dict(size=20)),
    ),
    legend=dict(
        title='Person',
        orientation="v",
        x=1.05,
        y=1,
        xanchor="left",
        yanchor="top",
        visible=True
    ),
    hovermode='closest',
    bargap=0.08,
    bargroupgap=0,
).update_traces(
    textposition='auto',
    hovertemplate='<b>Person:</b> %{x}<br><b>Activity Duration:</b> %{y} hours<extra></extra>'
)

# Pie Chart for Activity Duration Ratio by Person
eng_hours_pie1 = px.pie(
    eng_hours1,
    names="Person submitting this form:",
    values='Hours'
).update_layout(
    title='Ratio of Engagement Hours by Person',
    title_x=0.5,
    font=dict(family='Calibri', size=17, color='black')
).update_traces(
    rotation=90,
    textinfo='value+percent',
    hovertemplate='<b>%{label}</b>: %{value} hours<extra></extra>'
)

# Table
eng_table1 = go.Figure(data=[go.Table(
    header=dict(
        values=list(eng_hours1.columns),
        fill_color='paleturquoise',
        align='center',
        height=30,
        font=dict(size=12)
    ),
    cells=dict(
        values=[eng_hours1[col] for col in eng_hours1.columns],
        fill_color='lavender',
        align='left',
        height=25,
        font=dict(size=12)
    )
)])

eng_table1.update_layout(
    margin=dict(l=50, r=50, t=30, b=40),
    height=400,
    width=500,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)


# ----------------- Engagement Part 2 --------------------- #

# df_eng2['Hours'] = pd.to_numeric(df_eng2['Hours'], errors='coerce')

# Group by 'Person submitting this form:' and sum the 'Activity Duration (minutes):'
eng_hours2 = df_eng2.groupby('Person submitting this form:')['Hours'].sum().reset_index()

# Convert minutes to hours by dividing by 60
# eng_hours2['Hours'] = eng_hours2['Hours'] / 60

# Optional: Sort the results by total activity duration (in hours), descending
eng_hours2 = eng_hours2.sort_values(by='Hours', ascending=False)

# Bar Chart for Activity Duration by Person
eng_hours_bar2 = px.bar(
    eng_hours2,
    x="Person submitting this form:",  # X-axis: Person
    y='Hours',  # Y-axis: Activity Duration in hours
    color="Person submitting this form:",  # Color by Person
    text='Hours',  # Display activity duration in hours as text
).update_layout(
    height=450, 
    width=900,
    title=dict(
        text='Engagement Hours by Person',
        x=0.5, 
        font=dict(
            size=25,
            family='Calibri',
            color='black',
        )
    ),
    font=dict(
        family='Calibri',
        size=18,
        color='black'
    ),
    xaxis=dict(
        tickangle=-20,  # Rotate x-axis labels for better readability
        tickfont=dict(size=18),  # Adjust font size for the tick labels
        title=dict(
            text="Person",
            font=dict(size=20),  # Font size for the title
        ),
        showticklabels=True  # Show x-tick labels
    ),
    yaxis=dict(
        title=dict(
            text='Hours',
            font=dict(size=20),  # Font size for the title
        ),
    ),
    legend=dict(
        title='Person',
        orientation="v",  # Vertical legend
        x=1.05,  # Position legend to the right
        y=1,  # Position legend at the top
        xanchor="left",  # Anchor legend to the left
        yanchor="top",  # Anchor legend to the top
        visible=True  # Ensure the legend is visible
    ),
    hovermode='closest',  # Display only one hover label per trace
    bargap=0.08,  # Reduce the space between bars
    bargroupgap=0,  # Reduce space between individual bars in groups
).update_traces(
    textposition='auto',  # Show text labels inside bars
    hovertemplate='<b>Person:</b> %{x}<br><b>Activity Duration:</b> %{y} hours<extra></extra>'  # Fixed hovertemplate
)

# Pie Chart for Activity Duration Ratio by Person
eng_hours_pie2 = px.pie(
    eng_hours2,  # Use the grouped data for the pie chart
    names="Person submitting this form:",  # Person names as the slice labels
    values='Hours'  # Use activity duration in hours as values
).update_layout(
    title='Ratio of Engagement Hours by Person',
    title_x=0.5,
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    )
).update_traces(
    rotation=0,
    textinfo='value+percent',  # Show value and percentage on the pie slices
    hovertemplate='<b>%{label}</b>: %{value} hours<extra></extra>'  # Updated hovertemplate to show hours
)

# Table
eng_table2 = go.Figure(data=[go.Table(
    header=dict(
        values=list(eng_hours2.columns),
        fill_color='paleturquoise',
        align='center',
        height=30,  # Adjust the height of the header cells
        font=dict(size=12)  # Adjust font size
    ),
    cells=dict(
        values=[eng_hours2[col] for col in eng_hours2.columns],
        fill_color='lavender',
        align='left',
        height=25,  # Adjust the height of the cells
        font=dict(size=12)  # Adjust font size
    )
)])

eng_table2.update_layout(
    margin=dict(l=50, r=50, t=30, b=40),  # Remove margins
    height=400,
    width=500,
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
    plot_bgcolor='rgba(0,0,0,0)'  # Transparent plot area
)

# ---------------------------- IT Hours ------------------------------ #

# print(df_it.columns)

# Index(['Timestamp', 'Which form are you filling out?',
#        'Person completing this form:',
#        'Was all required IT equipment purchased/ serviced this month?',
#        'If answered "No" to above question, please specify why:',
#        'Were all IT equipment support request addressed?',
#        'Was phone system maintained and any support issues resolved within 48 hours?',
#        'Was page speed optimization completed this month?',
#        'Were any 404 errors identified and fixed?',
#        'Were Updates made to the sitemap, internal linking, or robot.txt as needed?',
#        'Was a Database / cloud backup completed?',
#        'Did you complete any content or layout updates on the website?',
#        'Please note any challenges, reasons for delays, or noteworthy outcomes from completed tasks:',
#        'Person completing this form:.1', 'Was a Security Audit Conducted?',
#        'If yes, were all issues addressed?',
#        'Were any new Cybersecurity vulnerabilities identified?',
#        'Did all Scheduled Cybersecurity training sessions occur this month?',
#        'Please note any challenges, reasons for delays, or noteworthy outcomes from completed tasks:.1',
#        'Person completing this form',
#        'Were automated Workflows reviewed and adjusted as necessary?',
#        'Were all planned email campaigns executed?',
#        'Were A/B tests conducted on landing pages or customer journeys?',
#        'Were any necessary SEO updates made this month?',
#        'Were all monthly analytics reports generated and reviewed?',
#        'Please note any challenges, reasons for delays, or noteworthy outcomes from completed tasks:.2',
#        'Person completing this form:.2',
#        'Did you attend or host all scheduled events this month?',
#        'Were all new or potential community partnerships engaged as planned?',
#        'Did you follow up with all attendees or participants from recent events?',
#        'Were all planned outreach campaigns completed?',
#        'Did you track social media engagement metrics?',
#        'Was feedback from the community collected and reviewed?',
#        'Please note any challenges, reasons for delays, or noteworthy outcomes from completed tasks:.3',
#        'Person completing this form:.3',
#        'Did all planned technical training sessions for staff occur?',
#        'Did all scheduled employees complete the training?',
#        'Please note any challenges, reasons for delays, or noteworthy outcomes from completed tasks:.4',
#        'Person completing this form:.4',
#        'Were all Weekly and Monthly reports completed and submitted on time?',
#        'Was data collected accurately and reviewed for quality?',
#        'Did you identify any actionable insights from this month's data?',
#        'Please note any challenges, reasons for delays, or noteworthy outcomes from completed tasks:.5',
#        'Date of Activity', 'Briefly describe what tasks you worked on:',
#        'How much time did you spend on these tasks? (minutes)',
#        'Date of Activity.1', 'Date', 'Date.1', 'Date.2', 'Date.3',
#        'Email Address', 'Date:'],
       
# Convert 'How much time did you spend on these tasks? (minutes)' to numeric, forcing errors to NaN (in case of non-numeric data)
# Convert 'How much time did you spend on these tasks? (minutes)' to numeric, forcing errors to NaN (in case of non-numeric data)
# Convert 'Activity Duration (hours):' to numeric, coercing errors to NaN
# df_it1['Activity Duration (hours):'] = pd.to_numeric(df_it1['Activity Duration (hours):'], errors='coerce')

# Group by 'Person completing this form:' and sum the 'Activity Duration (hours):'
it_hours1 = df_it1.groupby('Person submitting this form:')['Hours'].sum().reset_index()

# Sort the results by total activity duration (in hours), descending
# it_hours1 = it_hours1.sort_values(by='Hours', ascending=False)

# Bar Chart for IT Activity Duration by Person
it_hours_bar1 = px.bar(
    it_hours1,
    x="Person submitting this form:",
    y='Hours',
    color="Person submitting this form:",
    text='Hours',
).update_layout(
    height=450, 
    width=900,
    title=dict(
        text='IT Hours by Person',
        x=0.5, 
        font=dict(size=25, family='Calibri', color='black'),
    ),
    font=dict(family='Calibri', size=18, color='black'),
    xaxis=dict(
        tickangle=-20,
        tickfont=dict(size=18),
        title=dict(text="Person", font=dict(size=20)),
        showticklabels=True
    ),
    yaxis=dict(
        title=dict(text='Hours', font=dict(size=20)),
    ),
    legend=dict(
        title='Person',
        orientation="v",
        x=1.05,
        y=1,
        xanchor="left",
        yanchor="top",
        visible=True
    ),
    hovermode='closest',
    bargap=0.08,
    bargroupgap=0,
).update_traces(
    textposition='auto',
    hovertemplate='<b>Person:</b> %{x}<br><b>Activity Duration:</b> %{y} hours<extra></extra>'
)

# Pie Chart for IT Activity Duration Ratio by Person
it_hours_pie1 = px.pie(
    it_hours1,
    names="Person submitting this form:",
    values='Hours'
).update_layout(
    title='Ratio of IT Hours by Person',
    title_x=0.5,
    font=dict(family='Calibri', size=17, color='black')
).update_traces(
    rotation=90,
    textinfo='value+percent',
    hovertemplate='<b>%{label}</b>: %{value} hours<extra></extra>'
)

# Table
it_table1 = go.Figure(data=[go.Table(
    header=dict(
        values=list(it_hours1.columns),
        fill_color='paleturquoise',
        align='center',
        height=30,
        font=dict(size=12)
    ),
    cells=dict(
        values=[it_hours1[col] for col in it_hours1.columns],
        fill_color='lavender',
        align='left',
        height=25,
        font=dict(size=12)
    )
)])

it_table1.update_layout(
    margin=dict(l=50, r=50, t=30, b=40),
    height=400,
    width=500,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

# ---------------- IT Part 2 ------------ #

# Convert 'Activity Duration (hours):' to numeric, coercing errors to NaN
# df_it1['Hours'] = pd.to_numeric(df_it1['Activity Duration (hours):'], errors='coerce')

# Group by 'Person completing this form:' and sum the 'How much time did you spend on these tasks? (minutes)' column
it_hours2 = df_it2.groupby('Person submitting this form:')['Hours'].sum().reset_index()

# Convert minutes to hours by dividing by 60
# it_hours2['Activity Duration (hours):'] = it_hours2['How much time did you spend on these tasks? (minutes)'] / 60

# Optional: Sort the results by total activity duration (in hours), descending
# it_hours2 = it_hours2.sort_values(by='Activity Duration (hours):', ascending=False)

# print(df_it2)

# Display the grouped DataFrame
# print(activity_duration_grouped_it)

# Bar Chart for IT Activity Duration by Person
it_hours_bar2 = px.bar(
    it_hours2,  # Use the 'it_hours2' DataFrame
    x="Person submitting this form:",  # X-axis: Person
    y='Hours',  # Y-axis: Activity Duration in hours
    color="Person submitting this form:",  # Color by Person
    text='Hours',  # Display activity duration in hours as text
).update_layout(
    height=450, 
    width=900,
    title=dict(
        text='Total IT Hours by Person',
        x=0.5, 
        font=dict(
            size=25,
            family='Calibri',
            color='black',
        )
    ),
    font=dict(
        family='Calibri',
        size=18,
        color='black'
    ),
    xaxis=dict(
        tickangle=-20,  # Rotate x-axis labels for better readability
        tickfont=dict(size=18),  # Adjust font size for the tick labels
        title=dict(
            text="Person",
            font=dict(size=20),  # Font size for the title
        ),
        showticklabels=True  # Show x-tick labels
    ),
    yaxis=dict(
        title=dict(
            text='Hours',
            font=dict(size=20),  # Font size for the title
        ),
    ),
    legend=dict(
        title='Person',
        orientation="v",  # Vertical legend
        x=1.05,  # Position legend to the right
        y=1,  # Position legend at the top
        xanchor="left",  # Anchor legend to the left
        yanchor="top",  # Anchor legend to the top
        visible=True  # Ensure the legend is visible
        # visible=False  # Ensure the legend is visible
    ),
    hovermode='closest',  # Display only one hover label per trace
    bargap=0.08,  # Reduce the space between bars
    bargroupgap=0,  # Reduce space between individual bars in groups
).update_traces(
    textposition='auto',  # Show text labels inside bars
    hovertemplate='<b>Person:</b> %{x}<br><b>Activity Duration:</b> %{y} hours<extra></extra>'  # Fixed hovertemplate
)

# Pie Chart for IT Activity Duration Ratio by Person
it_hours_pie2 = px.pie(
    it_hours2,  # Use the 'it_hours2' DataFrame
    names="Person submitting this form:",  # Person names as the slice labels
    values='Hours'  # Use activity duration in hours as values
).update_layout(
    title='Ratio of IT Hours by Person',
    title_x=0.5,
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    )
).update_traces(
    rotation=90,
    textinfo='value+percent',  # Show value and percentage on the pie slices
    hovertemplate='<b>%{label}</b>: %{value} hours<extra></extra>'  # Updated hovertemplate to show hours
)

# Table
it_table2 = go.Figure(data=[go.Table(
    # columnwidth=[50, 50, 50],  # Adjust the width of the columns
    header=dict(
        values=list(it_hours2.columns),
        fill_color='paleturquoise',
        align='center',
        height=30,  # Adjust the height of the header cells
        # line=dict(color='black', width=1),  # Add border to header cells
        font=dict(size=12)  # Adjust font size
    ),
    cells=dict(
        values=[it_hours2[col] for col in it_hours2.columns],
        fill_color='lavender',
        align='left',
        height=25,  # Adjust the height of the cells
        # line=dict(color='black', width=1),  # Add border to cells
        font=dict(size=12)  # Adjust font size
    )
)])

it_table2.update_layout(
    margin=dict(l=50, r=50, t=30, b=40),  # Remove margins
    height=400,
    width=500,  # Set a smaller width to make columns thinner
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
    plot_bgcolor='rgba(0,0,0,0)'  # Transparent plot area
)

# ============================== Total Hours ========================== #

# Select only the required columns from each dataframe
columns_to_keep = ['Person submitting this form:', 'Hours']

# The code is concatenating the specified columns from four different DataFrames (`eng_hours1`,
# `nav_hours1`, `it_hours1`, `mc_hours1`) along the rows axis (axis 0) using the `pd.concat` function
# from the pandas library. The `columns_to_keep` variable contains the columns that are being selected
# from each DataFrame. The `ignore_index=True` parameter is used to reset the index of the resulting
# DataFrame to have a continuous range of integers.

total_hours1 = pd.concat(
    [eng_hours1[columns_to_keep], nav_hours1[columns_to_keep], it_hours1[columns_to_keep], mc_hours1[columns_to_keep]],
    ignore_index=True
)
total_hours1 = total_hours1.sort_values(by='Person submitting this form:', ascending=True)
# print(total_hours1)

total_hours2 = pd.concat(
    [eng_hours2[columns_to_keep], nav_hours2[columns_to_keep], it_hours2[columns_to_keep], mc_hours2[columns_to_keep]],
    ignore_index=True
)
total_hours2 = total_hours2.sort_values(by='Person submitting this form:', ascending=True)
# print(total_hours2)

total_hours = pd.concat([total_hours1, total_hours2], ignore_index=True)
total_hours_grouped = total_hours.groupby('Person submitting this form:', as_index=False).sum()
total_hours_grouped = total_hours_grouped.sort_values(by='Person submitting this form:', ascending=True)
print(total_hours_grouped)

# Total Hours 1 Table
total_hours_table1 = go.Figure(data=[go.Table(
    header=dict(
        values=list(total_hours1.columns),
        fill_color='paleturquoise',
        align='center',
        height=30,
        font=dict(size=12)
    ),
    cells=dict(
        values=[total_hours1[col] for col in total_hours1.columns],
        fill_color='lavender',
        align='left',
        height=25,
        font=dict(size=12)
    )
)])

total_hours_table1.update_layout(
    margin=dict(l=50, r=50, t=30, b=40),
    height=600,
    width=500,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

# Total Hours 2 Table
total_hours_table2 = go.Figure(data=[go.Table(
    header=dict(
        values=list(total_hours2.columns),
        fill_color='paleturquoise',
        align='center',
        height=30,
        font=dict(size=12)
    ),
    cells=dict(
        values=[total_hours2[col] for col in total_hours2.columns],
        fill_color='lavender',
        align='left',
        height=25,
        font=dict(size=12)
    )
)])

total_hours_table2.update_layout(
    margin=dict(l=50, r=50, t=30, b=40),
    height=600,
    width=500,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

# Total Hours Grouped Table
total_hours_grouped_table = go.Figure(data=[go.Table(
    header=dict(
        values=list(total_hours_grouped.columns),
        fill_color='paleturquoise',
        align='center',
        height=30,
        font=dict(size=12)
    ),
    cells=dict(
        values=[total_hours_grouped[col] for col in total_hours_grouped.columns],
        fill_color='lavender',
        align='left',
        height=25,
        font=dict(size=12)
    )
)])

total_hours_grouped_table.update_layout(
    margin=dict(l=50, r=50, t=30, b=40),
    height=600,
    width=500,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

# ============================== Dash Application ========================== #

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    children=[ 
        html.Div(
            className='divv', 
            children=[ 
                html.H1('BMHC Employee Hours', className='title'),
                html.H1('02/01/2025 - 02/14/2025', className='title2'),
                html.Div(
                    className='btn-box', 
                    children=[
                        html.A(
                            'Repo',
                            href='https://github.com/CxLos/Eng_Jan_2025',
                            className='btn'
                        )
                    ]
                )
            ]
        ),
        
html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph3',
            children=[
                dcc.Graph(
                    figure=nav_hours_bar1
                )
            ]
        ),
        html.Div(
            className='graph4',
            children=[
                dcc.Graph(
                    figure=nav_hours_pie1
                )
            ]
        )
    ]
),
        
html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph3',
            children=[
                dcc.Graph(
                    figure=mc_hours_bar1
                )
            ]
        ),
        html.Div(
            className='graph4',
            children=[
                dcc.Graph(
                    figure=mc_hours_pie1
                )
            ]
        )
    ]
),
        
html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph3',
            children=[
                dcc.Graph(
                    figure=eng_hours_bar1
                )
            ]
        ),
        html.Div(
            className='graph4',
            children=[
                dcc.Graph(
                    figure=eng_hours_pie1
                )
            ]
        )
    ]
),

html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph3',
            children=[
                dcc.Graph(
                    figure=it_hours_bar1
                )
            ]
        ),
        html.Div(
            className='graph4',
            children=[
                dcc.Graph(
                    figure=it_hours_pie1
                )
            ]
        )
    ]
),
        
# ROW 2
html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph3',
            children=[
                html.Div(
                    className='table',
                    children=[
                        html.H1(
                            className='table-title',
                            children='Navigation Hours Table'
                        )
                    ]
                ),
                html.Div(
                    className='table2', 
                    children=[
                        dcc.Graph(
                            className='data',
                            figure=nav_table1
                        )
                    ]
                )
            ]
        ),
        html.Div(
            className='graph4',
            children=[                
              html.Div(
                    className='table',
                    children=[
                        html.H1(
                            className='table-title',
                            children='MarCom Hours Table'
                        )
                    ]
                ),
                html.Div(
                    className='table2', 
                    children=[
                        dcc.Graph(
                            figure=mc_table1
                        )
                    ]
                )
   
            ]
        )
    ]
),
        
# ROW 2
html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph3',
            children=[
                html.Div(
                    className='table',
                    children=[
                        html.H1(
                            className='table-title',
                            children='Engagement Hours Table'
                        )
                    ]
                ),
                html.Div(
                    className='table2', 
                    children=[
                        dcc.Graph(
                            className='data',
                            figure=eng_table1
                        )
                    ]
                )
            ]
        ),
        html.Div(
            className='graph4',
            children=[                
              html.Div(
                    className='table',
                    children=[
                        html.H1(
                            className='table-title',
                            children='IT Hours Table'
                        )
                    ]
                ),
                html.Div(
                    className='table2', 
                    children=[
                        dcc.Graph(
                            figure=it_table1
                        )
                    ]
                )
   
            ]
        )
    ]
),
        
# ROW 2
html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph3',
            children=[
                html.Div(
                    className='table',
                    children=[
                        html.H1(
                            className='table-title',
                            children='2/1/2025 - 2/14/2025'
                        )
                    ]
                ),
                html.Div(
                    className='table2', 
                    children=[
                        dcc.Graph(
                            className='data',
                            figure=total_hours_table1
                        )
                    ]
                )
            ]
        ),
        html.Div(
            className='graph4',
            children=[                
                html.Div(
                    className='table2', 
                    children=[
                        dcc.Graph(
                            # figure=
                        )
                    ]
                )
   
            ]
        )
    ]
),
    
# ====================================================================================== # 

        html.Div(
            className='divv', 
            children=[ 
                html.H1('BMHC Employee Hours', className='title'),
                html.H1('02/15/2025 - 02/28/2025', className='title2'),
                html.Div(
                    className='btn-box', 
                    children=[
                    ]
                )
            ]
        ),
        
html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph3',
            children=[
                dcc.Graph(
                    figure=nav_hours_bar2
                )
            ]
        ),
        html.Div(
            className='graph4',
            children=[
                dcc.Graph(
                    figure=nav_hours_pie2
                )
            ]
        )
    ]
),
        
html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph3',
            children=[
                dcc.Graph(
                    figure=mc_hours_bar2
                )
            ]
        ),
        html.Div(
            className='graph4',
            children=[
                dcc.Graph(
                    figure=mc_hours_pie2
                )
            ]
        )
    ]
),
        
html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph3',
            children=[
                dcc.Graph(
                    figure=eng_hours_bar2
                )
            ]
        ),
        html.Div(
            className='graph4',
            children=[
                dcc.Graph(
                    figure=eng_hours_pie2
                )
            ]
        )
    ]
),

html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph3',
            children=[
                dcc.Graph(
                    figure=it_hours_bar2
                )
            ]
        ),
        html.Div(
            className='graph4',
            children=[
                dcc.Graph(
                    figure=it_hours_pie2
                )
            ]
        )
    ]
),
        
# ROW 2
html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph3',
            children=[
                html.Div(
                    className='table',
                    children=[
                        html.H1(
                            className='table-title',
                            children='Navigation Hours Table'
                        )
                    ]
                ),
                html.Div(
                    className='table2', 
                    children=[
                        dcc.Graph(
                            className='data',
                            figure=nav_table2
                        )
                    ]
                )
            ]
        ),
        html.Div(
            className='graph4',
            children=[                
              html.Div(
                    className='table',
                    children=[
                        html.H1(
                            className='table-title',
                            children='MarCom Hours Table'
                        )
                    ]
                ),
                html.Div(
                    className='table2', 
                    children=[
                        dcc.Graph(
                            figure=mc_table2
                        )
                    ]
                )
   
            ]
        )
    ]
),
        
# ROW 2
html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph3',
            children=[
                html.Div(
                    className='table',
                    children=[
                        html.H1(
                            className='table-title',
                            children='Engagement Hours Table'
                        )
                    ]
                ),
                html.Div(
                    className='table2', 
                    children=[
                        dcc.Graph(
                            className='data',
                            figure=eng_table2
                        )
                    ]
                )
            ]
        ),
        html.Div(
            className='graph4',
            children=[                
              html.Div(
                    className='table',
                    children=[
                        html.H1(
                            className='table-title',
                            children='IT Hours Table'
                        )
                    ]
                ),
                html.Div(
                    className='table2', 
                    children=[
                        dcc.Graph(
                            figure=it_table2
                        )
                    ]
                )
   
            ]
        )
    ]
),
# ROW 2
html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph3',
            children=[
                html.Div(
                    className='table',
                    children=[
                        html.H1(
                            className='table-title',
                            children='Hours 2/15/2025 - 2/28/2025'
                        )
                    ]
                ),
                html.Div(
                    className='table2', 
                    children=[
                        dcc.Graph(
                            className='data',
                            figure=total_hours_table2
                        )
                    ]
                )
            ]
        ),
        html.Div(
            className='graph4',
            children=[                
              html.Div(
                    className='table',
                    children=[
                        html.H1(
                            className='table-title',
                            children='Total Hours 2/1-2025 - 2/28/2025'
                        )
                    ]
                ),
                html.Div(
                    className='table2', 
                    children=[
                        dcc.Graph(
                            figure=total_hours_table1
                        )
                    ]
                )
   
            ]
        )
    ]
),
        
        
# ROW 2
# html.Div(
#     className='row2',
#     children=[
#         html.Div(
#             className='graph4',
#             children=[                
#               html.Div(
#                     className='table',
#                     children=[
#                         html.H1(
#                             className='table-title',
#                             children='Total Hours February 2025'
#                         )
#                     ]
#                 ),
#                 html.Div(
#                     className='table2', 
#                     children=[
#                         dcc.Graph(
#                             figure=total_hours_grouped_table
#                         )
#                     ]
#                 )
   
#             ]
#         )
#     ]
# ),
])

print(f"Serving Flask app '{current_file}'! 🚀")

if __name__ == '__main__':
    app.run_server(debug=True)
                #    False)
# =================================== Updated Database ================================= #

# updated_path = 'data/nav_hours_cleaned.xlsx'
# data_path = os.path.join(script_dir, updated_path)
# nav_hours1.to_excel(data_path, index=False)
# print(f"DataFrame saved to {data_path}")

# updated_path = 'data/mc_hours_cleaned.xlsx'
# data_path = os.path.join(script_dir, updated_path)
# mc_hours1.to_excel(data_path, index=False)
# print(f"DataFrame saved to {data_path}")

# updated_path = 'data/eng_hours_cleaned.xlsx'
# data_path = os.path.join(script_dir, updated_path)
# eng_hours1.to_excel(data_path, index=False)
# print(f"DataFrame saved to {data_path}")

# updated_path = 'data/it_hours_cleaned.xlsx'
# data_path = os.path.join(script_dir, updated_path)
# it_hours1.to_excel(data_path, index=False)
# print(f"DataFrame saved to {data_path}")

# updated_path = 'data/hours_2_1_to_2_14.xlsx'
# data_path = os.path.join(script_dir, updated_path)
# total_hours1.to_excel(data_path, index=False)
# print(f"DataFrame saved to {data_path}")

# updated_path = 'data/hours_2_15_to_2_28.xlsx'
# data_path = os.path.join(script_dir, updated_path)
# total_hours2.to_excel(data_path, index=False)
# print(f"DataFrame saved to {data_path}")

# updated_path = 'data/hours_2_1_to_2_28.xlsx'
# data_path = os.path.join(script_dir, updated_path)
# total_hours_grouped.to_excel(data_path, index=False)
# print(f"DataFrame saved to {data_path}")

# -------------------------------------------- KILL PORT ---------------------------------------------------

# netstat -ano | findstr :8050
# taskkill /PID 24772 /F
# npx kill-port 8050

# ---------------------------------------------- Host Application -------------------------------------------

# 1. pip freeze > requirements.txt
# 2. add this to procfile: 'web: gunicorn impact_11_2024:server'
# 3. heroku login
# 4. heroku create
# 5. git push heroku main

# Create venv 
# virtualenv venv 
# source venv/bin/activate # uses the virtualenv

# Update PIP Setup Tools:
# pip install --upgrade pip setuptools

# Install all dependencies in the requirements file:
# pip install -r requirements.txt

# Check dependency tree:
# pipdeptree
# pip show package-name

# Remove
# pypiwin32
# pywin32
# jupytercore

# ----------------------------------------------------

# Name must start with a letter, end with a letter or digit and can only contain lowercase letters, digits, and dashes.

# Heroku Setup:
# heroku login
# heroku create mc-impact-11-2024
# heroku git:remote -a mc-impact-11-2024
# git push heroku main

# Clear Heroku Cache:
# heroku plugins:install heroku-repo
# heroku repo:purge_cache -a mc-impact-11-2024

# Set buildpack for heroku
# heroku buildpacks:set heroku/python

# Heatmap Colorscale colors -----------------------------------------------------------------------------

#   ['aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
            #  'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
            #  'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
            #  'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
            #  'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
            #  'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
            #  'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
            #  'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl',
            #  'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn',
            #  'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu',
            #  'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar',
            #  'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn',
            #  'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid',
            #  'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr',
            #  'ylorrd'].

# rm -rf ~$bmhc_data_2024_cleaned.xlsx
# rm -rf ~$bmhc_data_2024.xlsx
# rm -rf ~$bmhc_q4_2024_cleaned2.xlsx