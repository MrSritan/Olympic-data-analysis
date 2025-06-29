import plotly.figure_factory as ff

def medal_tally(df ):
    medaltally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medaltally = medaltally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False)
    medaltally.loc[:, 'Total'] = medaltally['Gold'] + medaltally['Silver'] + medaltally['Bronze']
    medaltally = medaltally.reset_index()
    medaltally_regionwise = medaltally[['region', 'Gold', 'Silver', 'Bronze', 'Total']]
    return medaltally_regionwise

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Over all')
    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'Over all')

    return years, country


def fetch_medal_tally(df,year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    flag = 0
    if year == 'Over all' and country == 'Over all':
        tempdf = medal_df

    if year == 'Over all' and country != 'Over all':
        flag = 1
        tempdf = medal_df[medal_df['region'] == country]

    if year != 'Over all' and country == 'Over all':
        tempdf = medal_df[medal_df['Year'] == int(year)]

    if year != 'Over all' and country != 'Over all':
        tempdf = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = tempdf.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year')
        x.loc[:, 'Total'] = x['Gold'] + x['Silver'] + x['Bronze']
        x.reset_index(inplace=True)
    else:
        x = tempdf.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False)
        x.loc[:, 'Total'] = x['Gold'] + x['Silver'] + x['Bronze']
        x.reset_index(inplace=True)

    return(x)



def data_over_time(df,col):
    data_overtime = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    data_overtime.rename(columns={'count': 'No of '+col}, inplace=True)
    return data_overtime


def most_succ(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Over all':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'count', 'Sport', 'region', ]].drop_duplicates(['Name'])
    x.rename(columns={'count': 'No of Medals'}, inplace=True)
    return x

def yearwise_me_tal_con(df,country):
    tempdf = df.dropna(subset=['Medal']).drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    newtempdf = tempdf
    if country != 'Over all':
        newtempdf = tempdf[tempdf['region']==country]

    finaldf = newtempdf.groupby('Year').count()['Medal'].reset_index('Year').sort_values('Year')

    return finaldf


def country_sport_year_ana(df,country):
    tempdf = df.dropna(subset=['Medal']).drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    newtempdf = tempdf[tempdf['region'] == country].sort_values('Year')

    return newtempdf


def most_succ_conwise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'count', 'Sport']].drop_duplicates(['Name'])
    x.rename(columns={'count': 'No of Medals'}, inplace=True)
    return x


def sport_wise_age(df, sport):
    athletedf = df.drop_duplicates(subset=['Name', 'region'])
    tempdf = athletedf[(athletedf['Sport'] == sport)]['Age'].dropna()
    tempdf1 = athletedf[(athletedf['Sport'] == sport) & (athletedf['Medal'] == 'Gold')]['Age'].dropna()
    tempdf2 = athletedf[(athletedf['Sport'] == sport) & (athletedf['Medal'] == 'Silver')]['Age'].dropna()
    tempdf3 = athletedf[(athletedf['Sport'] == sport) & (athletedf['Medal'] == 'Bronze')]['Age'].dropna()

    fig = ff.create_distplot([tempdf, tempdf1, tempdf2, tempdf3],
                             ['Age Distribution', 'Gold medalist', 'Silver medalist', 'Bronze medalist'],
                             show_hist=False, show_rug=False)
    return fig


def athlete_size_sex (df,sport):
    athletedf = df.drop_duplicates(subset=['Name','region'])
    athletedf['Medal'] = athletedf['Medal'].fillna('No Medal')
    tempdf = athletedf[athletedf['Sport']==sport]
    return tempdf

def male_female(df):
    athletedf = df.drop_duplicates(subset=['Name', 'region'])
    men = athletedf[athletedf['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index('Year').rename(
        columns={'Name': 'Athletes'})
    women = athletedf[athletedf['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index('Year').rename(
        columns={'Name': 'Athletes'})
    final = men.merge(women, on='Year')
    final.rename(columns={'Athletes_x': 'Men', 'Athletes_y': 'Women'}, inplace=True)
    return final
