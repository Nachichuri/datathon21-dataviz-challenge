import pandas as pd
import plotly.express as px
import pycountry
from datetime import datetime


# 1. Most watched movies
def get_movie_views(dataframe, amount):
  '''
  Returns a dictionary with asset id, number of views and movie title for the selected
  amount of most watched movies in the entered DF.

  Arguments:
  dataframe(Pandas DataFrame): Flow DF with all visualizatons.
  amount(str): Integer showing the amount of movies to return.
  '''
  # Filter by type
  f_is_movie = dataframe['show_type'] == 'Película'
  # Get total views per movie
  df_f_movies = dataframe[f_is_movie][['content_id', 'title']].value_counts()
  # It's a multi-column value_counts so we get the keys and values and use it to return dictionary for new DF
  top_movies = [item for item in zip(df_f_movies.keys().tolist()[:amount], df_f_movies.tolist()[:amount])]

  return [{'asset_id': movie[0][0], 'title': movie[0][1], 'views': movie[1]} for movie in top_movies]


# 2. Most watched series
# In the documentation it is specified that all series fall in three categories
# of 'show_type': <serie>, <web> and <rolling>.
def get_series_views(dataframe, df_metadata, amount):
  '''
  Returns a Pandas DataFrame with asset id, number of views and series title for the selected
  amount of most watched series in the entered DF.
  
  Arguments:
  dataframe(Pandas DataFrame): Flow DF with all visualizatons.
  df_metadata(Pandas DataFrame): Flow DF with all content metadata.
  amount(str): Integer showing the amount of series to return.
  '''
  # Filter by type
  df_f_is_serie = dataframe['show_type'].isin(['Serie', 'Web', 'Rolling'])

  # Series can have multiple chapters, so we keep only the series by its content id
  unique_series = dataframe[df_f_is_serie]['content_id'].value_counts()

  df_unique_series = pd.DataFrame(unique_series).reset_index().rename(columns={'index': 'serie_id', 'content_id': 'views'})

  return pd.merge(df_unique_series, df_metadata.drop_duplicates('content_id'), left_on='serie_id', right_on='content_id', how='left').head(amount)


# 3. Most watched TV shows
def get_shows_watch(dataframe, df_metadata, amount):
  '''
  Returns a Pandas DataFrame with asset id, number of views and show title for the selected
  amount of most watched shows in the entered DF.
  
  Arguments:
  dataframe(Pandas DataFrame): Flow DF with all visualizatons.
  df_metadata(Pandas DataFrame): Flow DF with all content metadata.
  amount(str): Integer showing the amount of shows to return.
  '''
  # Filter by type
  df_f_is_show = dataframe['show_type'].isin(['TV'])

  unique_shows = dataframe[df_f_is_show]['content_id'].value_counts()

  pd_shows_unicos = pd.DataFrame(unique_shows).reset_index().rename(columns={'index': 'show_id', 'content_id': 'views'})

  return pd.merge(pd_shows_unicos, df_metadata.drop_duplicates('content_id'), left_on='show_id', right_on='content_id', how='left').head(amount)


# 4. Most watched episodes
# On top of general information about show type, since series are the most watched content, let's also
# get information about the most watched episodes
def get_mostwatched_episodes(dataframe, df_metadata, amount):
  '''
  Returns a Pandas DataFrame with asset id, number of views and episode title for the selected
  amount of most watched serie episode in the entered DF.
  
  Arguments:
  dataframe(Pandas DataFrame): Flow DF with all visualizatons.
  df_metadata(Pandas DataFrame): Flow DF with all content metadata.
  amount(str): Integer showing the amount of episodes to return.
  '''
  # Filter by type
  df_f_is_serie = dataframe['show_type'].isin(['Serie', 'Web', 'Rolling'])

  mostwatched_episodes = dataframe[df_f_is_serie]['asset_id'].value_counts()

  pd_mostwatched_episodes = pd.DataFrame(mostwatched_episodes).reset_index().rename(columns={'index': 'serie_id', 'asset_id': 'views'})

  return pd.merge(pd_mostwatched_episodes, df_metadata.drop_duplicates('asset_id'), left_on='serie_id', right_on='asset_id', how='left').head(amount)


# 5 - Connections per device per hour
# The idea is to see what devices the client use to consume content, and to see
# how media consumption devices vary through the day
def get_device_used(dataframe, complete_dataframe):
  '''
  Returns a list of dictionaries with device type, hour of day and amount of views for all the
  content watched in the first DF.
  
  Arguments:
  dataframe(Pandas DataFrame): Flow DF with all visualizatons.
  complete_dataframe(Pandas DataFrame): Unfiltered train dataframe to get all available categories.
  '''
  # We get all the available devices from the unfiltered DataFrame
  base_views = {device: {n: 0 for n in range(24)} for device in complete_dataframe['device_type'].value_counts().keys().to_list()}

  df_device_per_hour = dataframe.copy()

  df_device_per_hour['watch_hour'] = df_device_per_hour.apply(
      lambda row: int(row['tunein'][11:13]),
      axis=1)
  
  info_dict = df_device_per_hour[['device_type', 'watch_hour']].value_counts()

  views_per_hour_per_device = [item for item in zip(info_dict.keys().tolist(), info_dict.tolist())]

  for item in views_per_hour_per_device:
    base_views[item[0][0]][item[0][1]] = item[1]

  return [{'device': key, 'hour': n, 'views': base_views[key][n]} for n in range(24) for key in base_views]


# 6 - Categories per show type
# Now we want to get information regardin the most watched categories, and what
# show types compose those categories
def get_category_per_showtype(dataframe, amount):
  '''
  Returns a list of dictionaries with device category, show type and amount of views for all the
  content watched in the entered DF.
  
  Arguments:
  dataframe(Pandas DataFrame): Flow DF with all visualizatons.
  amount(str): Integer showing the amount of episodes to return.
  '''
  # We only keep the main show types
  filtered_showtypes = dataframe[dataframe['show_type'].isin(['Serie', 'TV', 'Película'])].copy()
  # We keep only the first (supposedly main) category listed if there are more than none
  filtered_showtypes['main_category'] = filtered_showtypes.apply(lambda row: row['category'].split('/')[0], axis=1)
  # We keep all the ones that are in the top n selected categories
  top_categories = filtered_showtypes[filtered_showtypes['main_category'].isin(filtered_showtypes['main_category'].value_counts().keys().to_list()[:amount])]

  # We get the amount of views per device in every category
  final_list = [combination for combination in zip(top_categories[['main_category', 'show_type']].value_counts().keys().to_list(), top_categories[['main_category', 'show_type']].value_counts().to_list())]

  return [{'category': entry[0][0], 'show_type': entry[0][1], 'views': entry[1]} for entry in final_list]


# 7 - Country of origin of all views
# Now the idea is to see which country the most watched content comes from
def get_country_from_watched_content(dataset):
  '''
  Returns a list of dictionaries with country name and amount of individually watched 
  content for that country, for all the content watched in the entered DF.
  
  Arguments:
  dataframe(Pandas DataFrame): Flow DF with all visualizatons.
  '''
  # We use the pycountry library to get all alpha_2 (2 digit) country names
  country_list = {country.alpha_2: country.name for country in pycountry.countries}

  df_country_from_watched_content = dataset['country_of_origin'].value_counts()

  df_countries_with_total = zip(df_country_from_watched_content.keys().to_list(), df_country_from_watched_content.to_list())

  return [{'country': country_list.get(entry[0]), 'views': entry[1]} for entry in df_countries_with_total]


# 8 - Potentially dropped content
# Now we're assuming that if a user starts watching content for more than a minute, and then
# stops watching it before 5 minutes have elapsed, the user didn't like the content and thus
# dropped it from his watch list. The idea is to detect content that might not be a good asset.
def get_potential_most_dropped_content(dataframe, df_metadata, amount):
  '''
  Returns a Pandas DataFrame with the top selected amount of content that the user decided to
  stop watching it before 5 min had elapsed since tune in.
  
  Arguments:
  dataframe(Pandas DataFrame): Flow DF with all visualizatons.
  df_metadata(Pandas DataFrame): Flow DF with all content metadata.
  amount(str): Integer showing the amount of top dropped content to return.
  '''
  df_content = dataframe.copy()
  
  df_content['seconds_watched'] = df_content.apply(lambda row: (datetime.strptime(row['tuneout'][:16], '%Y-%m-%d %H:%M') - datetime.strptime(row['tunein'][:16], '%Y-%m-%d %H:%M')).seconds, axis=1)

  # If the user was 1 minute into watching the content but decided to stop before 5 mins, we consider it a drop:
  df_content_with_sec = df_content[(df_content['seconds_watched'] > 60) & (df_content['seconds_watched'] < 300)]
  
  drop_per_entry = [{'content_id': entry[0], 'drops': entry[1]} for entry in zip(df_content_with_sec['content_id'].value_counts().keys().to_list(), df_content_with_sec['content_id'].value_counts().to_list())]

  return pd.DataFrame(drop_per_entry).merge(df_metadata.drop_duplicates(subset=['content_id']), on='content_id', how='left').head(amount)
