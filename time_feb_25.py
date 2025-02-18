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

# Define a discrete color sequence
# color_sequence = px.colors.qualitative.Plotly

# Convert 'Date of Activity' to datetime format
df_nav['Date of Activity'] = pd.to_datetime(df_nav['Date of Activity'], errors='coerce')
df_eng['Date of Activity'] = pd.to_datetime(df_eng['Date of Activity'], errors='coerce')
df_mc['Date of Activity'] = pd.to_datetime(df_mc['Date of Activity'], errors='coerce')
df_it['Date of Activity'] = pd.to_datetime(df_it['Date of Activity'], errors='coerce')

# Navigation
df_nav = df_nav[(df_nav['Date of Activity'] >= "2025-02-01") & (df_nav['Date of Activity'] <= "2025-02-14")]

# Engagement
df_eng = df_eng[(df_eng['Date of Activity'] >= "2025-02-01") & (df_eng['Date of Activity'] <= "2025-02-14")]

# MarCom
df_mc = df_mc[(df_mc['Date of Activity'] >= "2025-02-01") & (df_mc['Date of Activity'] <= "2025-02-14")]

# IT
df_it = df_it[(df_it['Date of Activity'] >= "2025-02-01") & (df_it['Date of Activity'] <= "2025-02-14")]
 

# print(df.head(10))
# print('Total Marketing Events: ', len(df))
# print('Column Names: \n', df.columns)
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
nav_hours = df_nav.groupby('Person filling out this form:')['Activity duration (minutes):'].sum().reset_index()

nav_hours['Activity duration (hours):'] = nav_hours['Activity duration (minutes):'] / 60

# Optional: Sort the results by total activity duration, descending
nav_hours = nav_hours.sort_values(by='Activity duration (minutes):', ascending=False)

# Display the grouped DataFrame
# print(activity_duration_grouped)

# Bar Chart for Activity Duration by Person
nav_hours_bar = px.bar(
    nav_hours,
    x="Person filling out this form:",
    y='Activity duration (hours):',  # Now using hours
    color="Person filling out this form:",
    text='Activity duration (hours):',  # Display the activity duration in hours
).update_layout(
    height=450, 
    width=900,
    title=dict(
        text='Total Navigation Hours by Person',
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
            text='Activity Duration (hours)',
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
nav_hours_pie = px.pie(
    nav_hours,  # Use the grouped data for the pie chart
    names="Person filling out this form:",
    values='Activity duration (hours):'  # Show activity duration in hours
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
df_mc['Activity duration (hours):'] = pd.to_numeric(df_mc['Activity duration (hours):'], errors='coerce')

# Group by 'Person completing this form:' and sum the 'Activity duration (hours):'
mc_hours = df_mc.groupby('Person completing this form:')['Activity duration (hours):'].sum().reset_index()

# Optional: Sort the results by total activity duration (in hours), descending
mc_hours = mc_hours.sort_values(by='Activity duration (hours):', ascending=False)

# Display the grouped DataFrame
# print(mc_hours)

# Bar Chart for Activity Duration by Person
mc_hours_bar = px.bar(
    mc_hours,  # Use the grouped data for the bar chart
    x="Person completing this form:",  # X-axis as the person completing the form
    y='Activity duration (hours):',  # Now using hours
    color="Person completing this form:",  # Color by the person completing the form
    text='Activity duration (hours):',  # Display the activity duration in hours
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
            text='Activity Duration (hours)',
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
mc_hours_pie = px.pie(
    mc_hours,  # Use the grouped data for the pie chart
    names="Person completing this form:",  # Names as the person completing the form
    values='Activity duration (hours):'  # Show activity duration in hours
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

# -------------------------- Engagement Hours ------------------------------ #

# print(df_eng.columns)

# Index(['Timestamp', 'Date of Activity', 'Person submitting this form:',
#        'Activity Duration (minutes):', 'Care Network Activity:',
#        'Entity name:', 'Brief Description:', 'Activity Status:',
#        'BMHC Administrative Activity:', 'Total travel time (minutes):',
#        'Community Outreach Activity:',
#        'Number engaged at Community Outreach Activity:'],

# Convert 'Activity Duration (minutes):' to numeric, forcing errors to NaN (in case of non-numeric data)
df_eng['Activity Duration (minutes):'] = pd.to_numeric(df_eng['Activity Duration (minutes):'], errors='coerce')

# Group by 'Person submitting this form:' and sum the 'Activity Duration (minutes):'
eng_hours = df_eng.groupby('Person submitting this form:')['Activity Duration (minutes):'].sum().reset_index()

# Convert minutes to hours by dividing by 60
eng_hours['Activity Duration (hours):'] = eng_hours['Activity Duration (minutes):'] / 60

# Optional: Sort the results by total activity duration (in hours), descending
eng_hours = eng_hours.sort_values(by='Activity Duration (hours):', ascending=False)

# Display the grouped DataFrame
# print(eng_hours)

# Bar Chart for Activity Duration by Person
eng_hours_bar = px.bar(
    eng_hours,
    x="Person submitting this form:",  # X-axis: Person
    y='Activity Duration (hours):',  # Y-axis: Activity Duration in hours
    color="Person submitting this form:",  # Color by Person
    text='Activity Duration (hours):',  # Display activity duration in hours as text
).update_layout(
    height=450, 
    width=900,
    title=dict(
        text='Total Engagement Hours by Person',
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
            text='Activity Duration (hours)',
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

# Pie Chart for Activity Duration Ratio by Person
eng_hours_pie = px.pie(
    eng_hours,  # Use the grouped data for the pie chart
    names="Person submitting this form:",  # Person names as the slice labels
    values='Activity Duration (hours):'  # Use activity duration in hours as values
).update_layout(
    title='Ratio of Engagement Hours by Person',
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
df_it['How much time did you spend on these tasks? (minutes)'] = pd.to_numeric(df_it['How much time did you spend on these tasks? (minutes)'], errors='coerce')

# Group by 'Person completing this form:' and sum the 'How much time did you spend on these tasks? (minutes)' column
it_hours = df_it.groupby('Person completing this form:')['How much time did you spend on these tasks? (minutes)'].sum().reset_index()

# Convert minutes to hours by dividing by 60
it_hours['Activity Duration (hours):'] = it_hours['How much time did you spend on these tasks? (minutes)'] / 60

# Optional: Sort the results by total activity duration (in hours), descending
it_hours = it_hours.sort_values(by='Activity Duration (hours):', ascending=False)


# Display the grouped DataFrame
# print(activity_duration_grouped_it)

# Bar Chart for IT Activity Duration by Person
it_hours_bar = px.bar(
    it_hours,  # Use the 'it_hours' DataFrame
    x="Person completing this form:",  # X-axis: Person
    y='Activity Duration (hours):',  # Y-axis: Activity Duration in hours
    color="Person completing this form:",  # Color by Person
    text='Activity Duration (hours):',  # Display activity duration in hours as text
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
            text='Activity Duration (hours)',
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
it_hours_pie = px.pie(
    it_hours,  # Use the 'it_hours' DataFrame
    names="Person completing this form:",  # Person names as the slice labels
    values='Activity Duration (hours):'  # Use activity duration in hours as values
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
                    figure=nav_hours_bar
                )
            ]
        ),
        html.Div(
            className='graph4',
            children=[
                dcc.Graph(
                    figure=nav_hours_pie
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
                    figure=mc_hours_bar
                )
            ]
        ),
        html.Div(
            className='graph4',
            children=[
                dcc.Graph(
                    figure=mc_hours_pie
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
                    figure=eng_hours_bar
                )
            ]
        ),
        html.Div(
            className='graph4',
            children=[
                dcc.Graph(
                    figure=eng_hours_pie
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
                    figure=it_hours_bar
                )
            ]
        ),
        html.Div(
            className='graph4',
            children=[
                dcc.Graph(
                    figure=it_hours_pie
                )
            ]
        )
    ]
),
        
        html.Div(
            className='row3',
            children=[
                html.Div(
                    className='graph33',
                    children=[
                        dcc.Graph(
                            # figure=mc_bar
                        )
                    ]
                ),
            ]
        ),   

        html.Div(
            className='row3',
            children=[
                html.Div(
                    className='graph33',
                    children=[
                        dcc.Graph(
                            # figure=it_hours_bar
                        )
                    ]
                ),
            ]
        ),   

        html.Div(
            className='row3',
            children=[
                html.Div(
                    className='graph33',
                    children=[
                        dcc.Graph(
                            # figure=it_hours_pie
                        )
                    ]
                ),
            ]
        ),   
        
                # html.Div(
        #     className='row3',
        #     children=[
        #         html.Div(
        #             className='graph33',
        #             children=[
        #                 dcc.Graph(
        #                     figure=nav_hours_bar
        #                 )
        #             ]
        #         ),
        #     ]
        # ),   
])

print(f"Serving Flask app '{current_file}'! 🚀")

if __name__ == '__main__':
    app.run_server(debug=True)
                #    False)
# =================================== Updated Database ================================= #

# updated_path = 'data/bmhc_q4_2024_cleaned.xlsx'
# data_path = os.path.join(script_dir, updated_path)
# df.to_excel(data_path, index=False)
# print(f"DataFrame saved to {data_path}")

# updated_path1 = 'data/service_tracker_q4_2024_cleaned.csv'
# data_path1 = os.path.join(script_dir, updated_path1)
# df.to_csv(data_path1, index=False)
# print(f"DataFrame saved to {data_path1}")

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