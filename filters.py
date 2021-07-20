import pandas as pd

# 1.1. Daily - Most watched movies
def get_daily_movie_views(dataframe, df_metadata, amount):
  '''
  Returns a dictionary with asset id, number of views and movie title for the selected
  amount of most watched movies in the entered DF.
  
  Arguments:
  dataframe(Pandas DataFrame): Flow DF with all daily visualizatons.
  df_metadata(Pandas DataFrame): Flow DF with all content metadata.
  amount(str): Integer showing the amount of movies to return.
  '''
  # Merge with metadata
  df_day_views_with_meta = dataframe.merge(df_metadata, on='asset_id')
  # Filter by type
  f_is_movie = df_day_views_with_meta['show_type'] == 'Película'
  # Get total views per movie
  df_f_movies = df_day_views_with_meta[f_is_movie][['content_id', 'title']].value_counts()
  # It's a multi-column value_counts so we get the keys and values and use it to return dictionary for new DF
  top_movies = [item for item in zip(df_f_movies.keys().tolist()[:amount], df_f_movies.tolist()[:amount])]

  return [{'asset_id': movie[0][0], 'title': movie[0][1], 'views': movie[1]} for movie in top_movies]


# 1.2. Daily - Most watched series
# In the documentation it is specified that all series fall in three categories
# of 'show_type': <serie>, <web> and <rolling>.
def get_daily_series_views(dataframe, df_metadata, amount):
  '''
  Returns a Pandas DataFrame with asset id, number of views and series title for the selected
  amount of most watched series in the entered DF.
  
  Arguments:
  dataframe(Pandas DataFrame): Flow DF with all daily visualizatons.
  df_metadata(Pandas DataFrame): Flow DF with all content metadata.
  amount(str): Integer showing the amount of series to return.
  '''
  df_day_views_with_meta = pd.merge(dataframe, df_metadata, on='asset_id')

  df_f_is_serie = df_day_views_with_meta['show_type'].isin(['Serie', 'Web', 'Rolling'])

  # Las series pueden tener varios caps
  unique_series = df_day_views_with_meta[df_f_is_serie]['content_id'].value_counts()

  pd_series_unicas = pd.DataFrame(unique_series).reset_index().rename(columns={'index': 'serie_id', 'content_id': 'views'})

  return pd.merge(pd_series_unicas, df_metadata.drop_duplicates('content_id'), left_on='serie_id', right_on='content_id', how='left').head(amount)


# 1.3. Daily - Most watched TV shows
def get_daily_shows_watch(dataframe, df_metadata, amount):
  '''
  Returns a dictionary with asset id, number of views and TV show title for the selected
  amount of most watched movies in the entered DF.
  
  Arguments:
  dataframe(Pandas DataFrame): Flow DF with all daily visualizatons.
  df_metadata(Pandas DataFrame): Flow DF with all content metadata.
  amount(str): Integer showing the amount of movies to return.
  '''
  df_day_views_with_meta = pd.merge(dataframe, df_metadata, on='asset_id')

  df_f_is_show = df_day_views_with_meta['show_type'].isin(['TV'])

  unique_shows = df_day_views_with_meta[df_f_is_show]['content_id'].value_counts()

  pd_shows_unicos = pd.DataFrame(unique_shows).reset_index().rename(columns={'index': 'show_id', 'content_id': 'views'})

  return pd.merge(pd_shows_unicos, df_metadata.drop_duplicates('content_id'), left_on='show_id', right_on='content_id', how='left').head(amount)

# 1.4. Daily - Most watched episodes
# In the documentation it is specified that all series fall in three categories
# of 'show_type': <serie>, <web> and <rolling>.

def get_daily_mostwatched_episodes(dataframe, df_metadata, amount):

  df_day_views_with_meta = pd.merge(dataframe, df_metadata, on='asset_id')

  df_f_is_serie = df_day_views_with_meta['show_type'].isin(['Serie', 'Web', 'Rolling'])

  mostwatched_episodes = df_day_views_with_meta[df_f_is_serie]['asset_id'].value_counts()

  pd_mostwatched_episodes = pd.DataFrame(mostwatched_episodes).reset_index().rename(columns={'index': 'serie_id', 'asset_id': 'views'})

  return pd.merge(pd_mostwatched_episodes, df_metadata.drop_duplicates('asset_id'), left_on='serie_id', right_on='asset_id', how='left').head(amount)

# 1.5 - Daily - Connections per device per hour

def get_daily_device_used(dataframe, complete_dataframe):
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