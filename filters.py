import pandas as pd

def get_daily_movie_views(dataframe, df_metadata, date, amount):
    # Filter by day
    df_day_views = dataframe[dataframe['tunein'].str.startswith(str(date))]
    # Merge with metadata
    df_day_views_with_meta = df_day_views.merge(df_metadata, on='asset_id')
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

def get_daily_series_views(dataframe, df_metadata, date, amount):
  
  df_day_views = dataframe[dataframe['tunein'].str.startswith(str(date))]

  df_day_views_with_meta = pd.merge(df_day_views, df_metadata, on='asset_id')

  df_f_is_serie = df_day_views_with_meta['show_type'].isin(['Serie', 'Web', 'Rolling'])

  # Las series pueden tener varios caps
  unique_series = df_day_views_with_meta[df_f_is_serie]['content_id'].value_counts()

  pd_series_unicas = pd.DataFrame(unique_series).reset_index().rename(columns={'index': 'serie_id', 'content_id': 'views'})

  return pd.merge(pd_series_unicas, df_metadata.drop_duplicates('content_id'), left_on='serie_id', right_on='content_id', how='left').head(amount)

