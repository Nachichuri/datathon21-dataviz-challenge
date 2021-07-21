import pandas as pd
import plotly.express as px
import pycountry
from datetime import datetime

# 1.1. Daily - Most watched movies
def get_movie_views(dataframe, amount):
  '''
  Returns a dictionary with asset id, number of views and movie title for the selected
  amount of most watched movies in the entered DF.
  
  Arguments:
  dataframe(Pandas DataFrame): Flow DF with all daily visualizatons.
  df_metadata(Pandas DataFrame): Flow DF with all content metadata.
  amount(str): Integer showing the amount of movies to return.
  '''
  # Filter by type
  f_is_movie = dataframe['show_type'] == 'Película'
  # Get total views per movie
  df_f_movies = dataframe[f_is_movie][['content_id', 'title']].value_counts()
  # It's a multi-column value_counts so we get the keys and values and use it to return dictionary for new DF
  top_movies = [item for item in zip(df_f_movies.keys().tolist()[:amount], df_f_movies.tolist()[:amount])]

  return [{'asset_id': movie[0][0], 'title': movie[0][1], 'views': movie[1]} for movie in top_movies]


# 1.2. Daily - Most watched series
# In the documentation it is specified that all series fall in three categories
# of 'show_type': <serie>, <web> and <rolling>.
def get_series_views(dataframe, df_metadata, amount):
  '''
  Returns a Pandas DataFrame with asset id, number of views and series title for the selected
  amount of most watched series in the entered DF.
  
  Arguments:
  dataframe(Pandas DataFrame): Flow DF with all daily visualizatons.
  df_metadata(Pandas DataFrame): Flow DF with all content metadata.
  amount(str): Integer showing the amount of series to return.
  '''
  df_f_is_serie = dataframe['show_type'].isin(['Serie', 'Web', 'Rolling'])

  # Las series pueden tener varios caps
  unique_series = dataframe[df_f_is_serie]['content_id'].value_counts()

  pd_series_unicas = pd.DataFrame(unique_series).reset_index().rename(columns={'index': 'serie_id', 'content_id': 'views'})

  return pd.merge(pd_series_unicas, df_metadata.drop_duplicates('content_id'), left_on='serie_id', right_on='content_id', how='left').head(amount)


# 1.3. Daily - Most watched TV shows
def get_shows_watch(dataframe, df_metadata, amount):
  '''
  Returns a dictionary with asset id, number of views and TV show title for the selected
  amount of most watched movies in the entered DF.
  
  Arguments:
  dataframe(Pandas DataFrame): Flow DF with all daily visualizatons.
  df_metadata(Pandas DataFrame): Flow DF with all content metadata.
  amount(str): Integer showing the amount of movies to return.
  '''
  df_f_is_show = dataframe['show_type'].isin(['TV'])

  unique_shows = dataframe[df_f_is_show]['content_id'].value_counts()

  pd_shows_unicos = pd.DataFrame(unique_shows).reset_index().rename(columns={'index': 'show_id', 'content_id': 'views'})

  return pd.merge(pd_shows_unicos, df_metadata.drop_duplicates('content_id'), left_on='show_id', right_on='content_id', how='left').head(amount)

# 1.4. Daily - Most watched episodes
# In the documentation it is specified that all series fall in three categories
# of 'show_type': <serie>, <web> and <rolling>.

def get_mostwatched_episodes(dataframe, df_metadata, amount):
  df_f_is_serie = dataframe['show_type'].isin(['Serie', 'Web', 'Rolling'])

  mostwatched_episodes = dataframe[df_f_is_serie]['asset_id'].value_counts()

  pd_mostwatched_episodes = pd.DataFrame(mostwatched_episodes).reset_index().rename(columns={'index': 'serie_id', 'asset_id': 'views'})

  return pd.merge(pd_mostwatched_episodes, df_metadata.drop_duplicates('asset_id'), left_on='serie_id', right_on='asset_id', how='left').head(amount)

# 1.5 - Daily - Connections per device per hour

def get_device_used(dataframe, complete_dataframe):
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

# 1.6 - Categories per show type
def get_category_per_showtype(dataframe, amount):
  # We only keep the main show types
  filtered_showtypes = dataframe[dataframe['show_type'].isin(['Serie', 'TV', 'Película'])].copy()
  # We keep only the first (supposedly main) category listed if there are more than none
  filtered_showtypes['main_category'] = filtered_showtypes.apply(lambda row: row['category'].split('/')[0], axis=1)
  # We keep all the ones that are in the top n selected categories
  top_categories = filtered_showtypes[filtered_showtypes['main_category'].isin(filtered_showtypes['main_category'].value_counts().keys().to_list()[:amount])]

  # We get the amount of views per device in every category
  final_list = [combination for combination in zip(top_categories[['main_category', 'show_type']].value_counts().keys().to_list(), top_categories[['main_category', 'show_type']].value_counts().to_list())]

  return [{'category': entry[0][0], 'show_type': entry[0][1], 'views': entry[1]} for entry in final_list]


# 1.7 - Country of origin of all views

def get_country_from_watched_content(dataset):

  country_list = {country.alpha_2: country.name for country in pycountry.countries}

  df_country_from_watched_content = dataset['country_of_origin'].value_counts()

  df_countries_with_total = zip(df_country_from_watched_content.keys().to_list(), df_country_from_watched_content.to_list())

  return [{'country': country_list.get(entry[0]), 'views': entry[1]} for entry in df_countries_with_total]


# 8 - Potentially dropped content
def get_potential_most_dropped_content(dataframe, df_metadata, amount):
  df_content = dataframe.copy()

  df_content['seconds_watched'] = df_content.apply(lambda row: (datetime.strptime(row['tuneout'][:16], '%Y-%m-%d %H:%M') - datetime.strptime(row['tunein'][:16], '%Y-%m-%d %H:%M')).seconds, axis=1)

  df_content_with_sec = df_content[(df_content['seconds_watched'] > 60) & (df_content['seconds_watched'] < 300)]
  
  drop_per_entry = [{'content_id': entry[0], 'drops': entry[1]} for entry in zip(df_content_with_sec['content_id'].value_counts().keys().to_list(), df_content_with_sec['content_id'].value_counts().to_list())]

  return pd.DataFrame(drop_per_entry).merge(df_metadata.drop_duplicates(subset=['content_id']), on='content_id', how='left').head(amount)