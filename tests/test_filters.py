import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from filters import get_movie_views, get_series_views, get_shows_watch, get_mostwatched_episodes, get_device_used, get_category_per_showtype, get_potential_most_dropped_content, get_country_from_watched_content

####################
# Mocks
####################

mock_df = pd.DataFrame([
    {'asset_id': 'A', 'show_type': 'Película', 'title': 'ABC', 'content_id': '1', 'device_type': 'STATIONARY', 'tunein': '2021-02-18 23:52:00.0', 'tuneout': '2021-02-19 00:52:00.0', 'category': 'Drama/Romance', 'country_of_origin': 'AR'},
    {'asset_id': 'B', 'show_type': 'Serie', 'title': 'DEF', 'content_id': '2', 'device_type': 'STATIONARY', 'tunein': '2021-03-18 22:52:00.0', 'tuneout': '2021-03-18 22:59:00.0', 'category': 'Drama/Crimen', 'country_of_origin': 'AR'},
    {'asset_id': 'C', 'show_type': 'Web', 'title': 'GHI', 'content_id': '3', 'device_type': 'STB', 'tunein': '2021-01-18 22:52:00.0', 'tuneout': '2021-01-18 22:56:00.0', 'category': 'Infantil', 'country_of_origin': 'US'},
    {'asset_id': 'D', 'show_type': 'Rolling', 'title': 'JKL', 'content_id': '4', 'device_type': 'STB', 'tunein': '2021-02-12 22:52:00.0', 'tuneout': '2021-02-12 23:52:00.0', 'category': 'Acción', 'country_of_origin': 'US'},
    {'asset_id': 'E', 'show_type': 'TV', 'title': 'MNO', 'content_id': '5', 'device_type': 'STB', 'tunein': '2021-02-11 22:52:00.0', 'tuneout': '2021-02-11 22:53:00.0', 'category': 'Suspenso', 'country_of_origin': 'BR'}
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


def test_get_device_used():
    
    output = get_device_used(mock_df, mock_df)
    
    assert type(output) == list
    assert type(output[0]) == dict


def test_get_category_per_showtype():

    output = get_category_per_showtype(mock_df, mock_amount)

    assert type(output) == list
    assert type(output[0]) == dict
    assert len(output) <= mock_amount


def test_get_potential_most_dropped_content():

    output = get_potential_most_dropped_content(mock_df, mock_df, mock_amount)

    assert type(output) == type(mock_df)
    assert output.shape[0] <= mock_amount


def test_get_country_from_watched_content():

    output = get_country_from_watched_content(mock_df)

    assert type(output) == list
    assert type(output[0]) == dict