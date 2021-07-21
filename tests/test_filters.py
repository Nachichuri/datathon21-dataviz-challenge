import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from filters import get_movie_views, get_series_views, get_shows_watch, get_mostwatched_episodes

####################
# Mocks
####################

mock_df = pd.DataFrame([
    {'asset_id': 'A', 'show_type': 'Película', 'title': 'ABC', 'content_id': '1'},
    {'asset_id': 'B', 'show_type': 'Serie', 'title': 'DEF', 'content_id': '2'},
    {'asset_id': 'C', 'show_type': 'Web', 'title': 'GHI', 'content_id': '3'},
    {'asset_id': 'D', 'show_type': 'Rolling', 'title': 'JKL', 'content_id': '4'},
    {'asset_id': 'E', 'show_type': 'TV', 'title': 'MNO', 'content_id': '5'}
    ])

mock_amount = 5


####################
# Tests
####################

def test_get_movie_views():
    
    output = get_movie_views(mock_df, mock_amount)

    assert type(output) == list
    assert type(output[0]) == dict
    assert len(output) <= mock_amount


def test_get_series_views():
    
    output = get_series_views(mock_df, mock_df, mock_amount)

    assert type(output) == type(mock_df)
    assert output.shape[0] <= mock_amount


def test_get_shows_views():
    
    output = get_shows_watch(mock_df, mock_df, mock_amount)

    assert type(output) == type(mock_df)
    assert output.shape[0] <= mock_amount


def test_get_mostwatched_episodes():
    
    output = get_mostwatched_episodes(mock_df, mock_df, mock_amount)

    assert type(output) == type(mock_df)
    assert output.shape[0] <= mock_amount

