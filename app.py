import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_title='NYC Airbnb', page_icon=':wave:')

def plot_scatter(x,y,hue:None):
    plt.figure(figsize=(10,6))
    sns.scatterplot(x=x,y=y,hue=hue)
    plt.ioff()
    st.pyplot()

def plot_pie(group,y,title):
    df.groupby(group).sum().plot.pie(y=y,
                                    autopct='%.1f', 
                                    ylabel='',
                                    legend=False,
                                    figsize=(8,8))
    plt.title(title)
    st.pyplot()

st.title('NYC Airbnb')
st.markdown("""
<p><b>About Dataset</b></p>
<p><b>Context</b></p>
Since 2008, guests and hosts have used Airbnb to expand on traveling possibilities and present more unique, personalized way of experiencing the world. This dataset describes the listing activity and metrics in NYC, NY for 2019.
<p></p>
<p><b>Content</b></p>
This data file includes all needed information to find out more about hosts, geographical availability, necessary metrics to make predictions and draw conclusions.
<p></p>
<p><b>Acknowledgements</b></p>
This public dataset is part of Airbnb, and the original source can be found on this website.
<p></p>
<p><b>Inspiration</b></p>
What can we learn about different hosts and areas?
What can we learn from predictions? (ex: locations, prices, reviews, etc)
Which hosts are the busiest and why?
Is there any noticeable difference of traffic among different areas and what could be the reason for it?
<p></p>
<p></p>
            """,unsafe_allow_html=True)

df = pd.read_csv('AB_NYC_2019.csv')

st.write(df.head(10))
st.markdown('-'*70)

st.success('Null values about dataset')
st.warning("Since we don't need the first 4 colums let's drop them")
col1,col2 = st.columns([4,8])
with col1:
    st.write(df.isnull().sum())
with col2:
    df.drop(['id','name','host_id','host_name'],axis=1,inplace=True)
    st.write(df.head(10))
st.markdown('-'*70)

st.subheader('Describe the dataset')
st.write(df.describe())
st.markdown('-'*70)

st.subheader('Choose data to see its graphics')
data_type = st.selectbox('',['Default','Neighbourhood Group','Room Type','Availability 365'])
if data_type == 'Neighbourhood Group':
    st.subheader('Different Neighbourhood Groups')
    st.markdown(
    '''The following plot represents the count of Airbnb's in the different 
    neighbourhood groups. From the plot, we can easily visualize that maximum 
    number of houses or apartments listed on Airbnb is in''')
    plot_type = st.selectbox('',['Choose plot type','Horizontal','Vertical','Scatter','Pie'])
    if plot_type == 'Horizontal':
        df.neighbourhood_group.value_counts().plot.barh().set_title('Neighbourhood Group Frequency')
        st.pyplot()
        st.markdown('-'*70)
    elif plot_type == 'Vertical':
        f,ax = plt.subplots(figsize=(15,6))
        ax = sns.countplot(x=df.neighbourhood_group,palette="muted")
        st.pyplot()
        st.markdown('-'*70)

        plt.figure(figsize=(12,8))
        df.groupby('neighbourhood_group').agg({'price':'mean','availability_365':'mean'}).plot.bar(alpha=.6)
        plt.title('Neighbourhood Group For Price And Availability')
        st.pyplot()

    elif plot_type == 'Scatter':
        plot_scatter(x=df.longitude,y=df.latitude,hue=df.neighbourhood_group)
        st.markdown('-'*70)
        plot_scatter(x=df.price,y=df.availability_365,hue=df.neighbourhood_group)
    elif plot_type == 'Pie':
        plot_pie(group='neighbourhood_group',y='price',title='Price for Neighbourhood Group')
        plot_pie(group='neighbourhood_group',y='availability_365',title='Availability 365 for Neighbourhood Group')
        
        st.markdown('-'*70)
elif data_type == 'Room Type':
    st.subheader('Different Room Type')
    plot_type = st.selectbox('',['Choose plot type','Horizontal','Vertical','Scatter','Pie'])
    if plot_type == 'Horizontal':
        df.room_type.value_counts().plot.barh()
        plt.title('Room Type Frequency')
        st.pyplot()
        st.markdown('-'*70)
    elif plot_type == 'Vertical':
        sns.countplot(x=df['room_type'], palette="plasma")
        fig = plt.gcf()
        fig.set_size_inches(8,5)
        plt.title('Room Type')
        st.pyplot()
        st.markdown('-'*70)
    elif plot_type == 'Scatter':
        plot_scatter(x=df.longitude,y=df.latitude,hue=df.room_type)
        st.markdown('-'*70)
    elif plot_type == 'Pie':
        plot_pie(group='room_type',y='price',title='Price for Room Type')
        plot_pie(group='room_type',y='availability_365',title='Availability 365 for Room Type')
        st.markdown('-'*70)

elif data_type == 'Availability 365':
    plot_scatter(x=df.longitude,y=df.latitude,hue=df.availability_365)
    st.markdown('-'*70)
    # st.subheader('Different Plot Type')
    # plot_type = st.selectbox('',['Choose plot type','Horizontal','Vertical','Scatter'])
    # if plot_type == 'Horizontal':
    #     df.availability_365.value_counts().plot.barh()
    #     plt.title('Room Type Frequency')
    #     st.pyplot()
    #     st.markdown('-'*70)
    # elif plot_type == 'Vertical':
    #     sns.countplot(data=df[df['availability_365']>=150],x=df['availability_365'], palette="plasma")
    #     fig = plt.gcf()
    #     fig.set_size_inches(8,5)
    #     plt.title('Room Type')
    #     st.pyplot()
    #     st.markdown('-'*70)
    # elif plot_type == 'Scatter':
    #     plot_scatter(x=df.longitude,y=df.latitude,hue=df.availability_365)
    #     st.markdown('-'*70)
    
else:
    data = st.selectbox('Choose Neigbourhood or Correlation',['Neigbourhood','Correlation'])
    if data == 'Neigbourhood':
        neighbour_type = st.selectbox('Neighbourhood Group',df.neighbourhood_group.unique().tolist())
        # st.pyplot(sns.jointplot(x='price',y='neighbourhood_group',data=df))
        st.success('Neighbourhood by price with histplot')
        col1,col2 = st.columns([4,8])
        for i in df.neighbourhood_group.unique().tolist():
            if neighbour_type == i:
                df1 = df[df.neighbourhood_group == i][["neighbourhood","price"]]
                d = df1.groupby("neighbourhood").mean()
                with col1:
                    st.write(d)
                with col2:

                    sns.histplot(d,kde=True)
                    st.pyplot()
    elif data == 'Correlation':
        df.reviews_per_month.fillna(value=0,inplace=True)
        df.drop('last_review',axis=1,inplace=True)
        df['neighbourhood_group'] = df.neighbourhood_group.astype('category').cat.codes
        df['neighbourhood'] = df.neighbourhood.astype('category').cat.codes
        df['room_type'] = df.room_type.astype('category').cat.codes
        
        corr = df.corr(method='kendall')
        plt.figure(figsize=(15,12))
        palette = sns.diverging_palette(20, 220, n=256)
        sns.heatmap(corr, annot=True, fmt=".2f", cmap=palette, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5}).set(ylim=(11, 0))
        plt.title("Correlation Matrix",size=15, weight='bold')
        st.pyplot()
        
