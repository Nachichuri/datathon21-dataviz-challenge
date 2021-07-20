import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import get_clean_serie_name

def test_get_clean_serie_name():
    assert get_clean_serie_name('T:3 Ep:02 Attack on Titan') == 'Attack on Titan'
    assert get_clean_serie_name('T:0 Ep:01 Loki') == 'Loki'
    assert get_clean_serie_name('Ep:04 Peaky Blinders') == 'Peaky Blinders'