""" Name: Ramon Urena
CS230: Section SN2F
Data: Skyscrapers around the World
URL:

Description: This program allows users to locate the tallest 100 skyscrapers in a map and filter by year completed. (a few sentences about your program and the queries and charts)"""

python -m pip install -U matplotlib
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pydeck as pdk
import pandas as pd


# extract all data from file
def read_data(fileName):
    df = pd.read_csv(fileName)
    lst = []

    columns = ['RANK', 'NAME', 'CITY', 'Full Address', 'Latitude', 'Longitude', 'COMPLETION', 'Height', 'Meters', 'Feet', 'FLOORS', 'MATERIAL', 'FUNCTION', 'Link']

    for index, row in df.iterrows():
        sub = []
        for col in columns:
            index_no = df.columns.get_loc(col)
            sub.append(row[index_no])
        lst.append(sub)

    return lst


# list created to collect all the different cities
def city_list(data):
    cities = []

    for i in range(len(data)):
        if data[i][2] not in cities:
            cities.append(data[i][2])

    return cities


# list created to collect all the different materials
def material_list(data):
    materials = []

    for i in range(len(data)):
        if data[i][11] not in materials:
            materials.append(data[i][11])

    return materials


# list created to collect all the different functions
def function_list(data):
    functions = []

    for i in range(len(data)):
        if data[i][12] not in functions:
            functions.append(data[i][12])

    return functions


# function to count the amount of the frequency of skyscrapers' functions in our data
def functions_freq(data, functions):
    functions_dict = {}

    for function in functions:
        freq = 0
        for i in range(len(data)):
            if data[i][12] == function:
                freq += 1
        functions_dict[function] = freq

    return functions_dict


# counts how many skyscrapers comply with the specifications set by the user
def freq_data(data, cities, COMPLETION):
    freq_dict = {}

    for city in cities:
        freq = 0
        for i in range(len(data)):
            if data[i][2] == city and COMPLETION >= data[i][6]:
                freq += 1
        freq_dict[city] = freq

    return freq_dict


# create a bar to represent the skyscrapers that fit the criteria given by the user
def bar_chart(freq_dict):
    x = freq_dict.keys()
    y = freq_dict.values()

    plt.bar(x, y, color="skyblue")
    plt.xticks(rotation=45)
    plt.xlabel('Cities')
    plt.ylabel('Amount of buildings in each city')
    title = 'Amount of Skyscrapers in top 100 in'
    for key in freq_dict.keys():
        title += ' ' + key + ","
    plt.title(title)

    return plt


# function to create pie chart to represent skyscrapers functions
def functions_bar_chart(functions_dict):
    x = functions_dict.keys()
    y = functions_dict.values()

    plt.bar(x, y, color="red")
    plt.xticks(rotation=45)
    plt.xlabel('Functions')
    plt.ylabel('Amount of Skyscrapers in top 100')
    title = 'Functions of Skyscrapers in top 100 in'
    for key in functions_dict.keys():
        title += ' ' + key + ","
    plt.title(title)

    return plt


# display map using the filters given by user
def display_map(data, cities, COMPLETION):
    loc = []
    for i in range(len(data)):
        if data[i][2] in cities and COMPLETION >= data[i][6]:
            loc.append([data[i][1], data[i][4], data[i][5]])

    map_df = pd.DataFrame(loc, columns=['NAME', 'Latitude', 'Longitude'])

    view_state = pdk.ViewState(latitude=map_df['Latitude'].mean(), longitude=map_df['Longitude'].mean(), zoom=10, pitch=8)
    layer = pdk.Layer('ScatterplotLayer', data=map_df, get_position='[Longitude, Latitude]', get_radius=400, get_color=[0, 255, 255], picktable=True)
    tool_tip = {'html': 'Name:<br/>{NAME}', 'style': {'backgroundColor': 'navy', 'color': 'White'}}

    map_a = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9', initial_view_state=view_state, layers=[layer], tooltip=tool_tip)

    st.pydeck_chart(map_a)


def main():
    data = read_data('Skyscrapers2021.csv')

    st.title('Tallest 100 Skyscrapers in the world')
    st.write("I hope you are not afraid of heights!")

    cities = st.sidebar.multiselect('Select the cities that you want to explore', city_list(data))
    completionYear = st.sidebar.slider('Select completion year', 1920, 2020, 1930)

    functions = st.sidebar.multiselect('Select what functionality the skyscrapers should perform to compare it to a city', function_list(data))

    if len(cities) > 0:
        st.write('Map of 100 Tallest Skyscrapers')
        display_map(data, cities, completionYear)
        st.write('\nCount of Skyscrapers')
        st.pyplot(bar_chart(freq_data(data, cities, completionYear)))
        st.write('\nFunctions of Skyscrapers')
        st.pyplot(functions_bar_chart(functions_freq(data, functions)))


main()
