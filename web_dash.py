import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


import preppro ,helper

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preppro.preprocess(df, region_df)
st.sidebar.title('Olympics Analysis')
user_menu = st.sidebar.radio(
    'Select an Option',('Medal Tally','Overall Analysis','Country wise Analysis','Athlete wise Analysis')
)





if user_menu == 'Medal Tally':

    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year =  st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country",country)

    if selected_country == 'Over all' and selected_year == 'Over all':
        st.title("Overall Medal Tally")

    elif selected_country == 'Over all' and selected_year != 'Over all':
        st.title("Medal Tally in "+ str(selected_year))

    elif selected_country != 'Over all' and selected_year == 'Over all':
        st.title("Over all Medal Tally of "+ str(selected_country))

    elif selected_country != 'Over all' and selected_year != 'Over all':
        st.title("Medal Tally of " + str(selected_country)  +" in " + str(selected_year))

    st.table(helper.fetch_medal_tally(df,selected_year,selected_country))

if user_menu == 'Overall Analysis':
    Editions = df['Year'].nunique() - 1
    Cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = format(df['Name'].nunique(), ",")
    countries = df['region'].nunique()

    st.title("Top Stats")

    # Styling function
    def stat_card(title, value, color="cyan"):
        return f"""
           <div style='text-align: center;'>
               <h4 style='color: deepskyblue;'>{title}</h4>
               <h2 style='color: {color};'>{value}</h2>
           </div>
           """


    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(stat_card("Editions", Editions, "White"), unsafe_allow_html=True)
    with col2:
        st.markdown(stat_card("Cities", Cities, "White"), unsafe_allow_html=True)
    with col3:
        st.markdown(stat_card("Countries", countries, "White"), unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(stat_card("Sports", sports, "White"), unsafe_allow_html=True)
    with col2:
        st.markdown(stat_card("Events", events, "White"), unsafe_allow_html=True)
    with col3:
        st.markdown(stat_card("Athletes", athletes, "White"), unsafe_allow_html=True)


    nations_overtime = helper.data_over_time(df,'region')
    fig = px.line(nations_overtime, x="Year", y='No of region')
    st.title("Participating Countries over the Year")
    st.plotly_chart(fig)

    events_overtime = helper.data_over_time(df, 'Event')
    fig = px.line(events_overtime, x="Year", y='No of Event')
    st.title("Events over the Years")
    st.plotly_chart(fig)

    events_overtime = helper.data_over_time(df, 'Name')
    fig = px.line(events_overtime, x="Year", y='No of Name')
    st.title("Athletes over the Years")
    st.plotly_chart(fig)

    st.title("Events distribution in Sports over the Years")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Over all')

    selected_sport = st.selectbox('Select a Sport',sport_list)


    y = helper.most_succ(df,selected_sport)
    st.table(y)



if user_menu == 'Country wise Analysis':
    st.title("Country wise Analysis")

    country = df['region'].dropna().unique().tolist()
    country.sort()
    selected_country = st.selectbox("Select Country", country)

    st.title(selected_country +" Medal Tally over the Years")

    finaldf = helper.yearwise_me_tal_con(df,selected_country)
    fig = px.bar(finaldf, x='Year', y='Medal')
    st.plotly_chart(fig)

    st.title(selected_country + " Sport wise analysis over the Years")
    finaldf = helper.country_sport_year_ana(df,selected_country)

    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(finaldf.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype(int),annot=True)
    st.pyplot(fig)

    st.title(selected_country + " Most Succesful Athletes")
    x = helper.most_succ_conwise(df,selected_country)
    st.table(x)


if user_menu == 'Athlete wise Analysis':
    st.title("Athlete Age wise Analysis")



    athletedf = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athletedf['Age'].dropna()
    x2 = athletedf[athletedf['Medal'] == 'Gold']['Age'].dropna()
    x3 = athletedf[athletedf['Medal'] == 'Silver']['Age'].dropna()
    x4 = athletedf[athletedf['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4],
                             ['Age Distribution', 'Gold medalist', 'Silver medalist', 'Bronze medalist'],
                             show_hist=False, show_rug=False)
    st.plotly_chart(fig)

    st.title("Athlete Sport wise Age Analysis")

    sports_list = df['Sport'].unique().tolist()
    selected_sport = st.selectbox('Select a Sport',sports_list, key='age_analysis_sport')

    st.header(str(selected_sport)+" Age wise Analysis")

    fig = helper.sport_wise_age(df, selected_sport)
    st.plotly_chart(fig)

    st.title("Athlete Sport wise Anthropometry Analysis")

    sports_list2 = df['Sport'].unique().tolist()
    selected_sport2 = st.selectbox('Select a Sport', sports_list2, key='anthropometry_sport')

    tempdf = helper.athlete_size_sex(df,selected_sport2)

    st.header(str(selected_sport2) + " Anthropometry Analysis")

    fig, ax = plt.subplots(figsize=(20,20))
    sns.scatterplot(data=tempdf, x='Weight', y='Height', hue='Medal', style='Sex', s=200, ax=ax)
    st.pyplot(fig)

    st.title("Male v/s Female Athlete Partisipation")
    final = helper.male_female(df)
    final_melted = final.melt(id_vars='Year', value_vars=['Men', 'Women'],
                              var_name='Gender', value_name='Athletes')

    fig = px.bar(final_melted, x='Year', y= 'Athletes', color='Gender',
                 barmode='group', title='Number of Male and Female Athletes Over the Years',color_discrete_map={'Men': 'deepskyblue', 'Women': 'red'})

    fig.update_layout(template='plotly_dark', xaxis_title='Year', yaxis_title='Number of Athletes')
    st.plotly_chart(fig)
