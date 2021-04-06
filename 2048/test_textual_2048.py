from game2048.textual_2048 import *
import pytest



def test_read_player_command(monkeypatch):
    responses = iter(['d', 'g','k', 'h', 'b'])
    monkeypatch.setattr('builtins.input', lambda msg: next(responses))
    assert read_player_command() == 'd'
    assert read_player_command() == 'g'
    assert read_player_command() == 'h'
    assert read_player_command() == 'b'

def test_read_theme_grid(monkeypatch):
    responses = iter(['d', 'g','0', '1', '2','no','yess','11', '0','1','no'])
    monkeypatch.setattr('builtins.input', lambda msg: next(responses))
    assert read_theme_grid() == "0"
    assert read_theme_grid() == "1"
    assert read_theme_grid() == "2"
    assert read_theme_grid() == "0"
    assert read_theme_grid() == "1"
    

def test_read_size_grid(monkeypatch):
    responses = iter(['1','-2','kaka','nooo','you cant win', '2.99999', '4','5','haha','6','7'])
    monkeypatch.setattr('builtins.input', lambda msg: next(responses))
    assert read_size_grid() == 4
    assert read_size_grid() == 5
    assert read_size_grid() == 6
    assert read_size_grid() == 7
