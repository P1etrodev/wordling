from json import load
from tools import play_wordle
import sys
from os.path import dirname, join

if getattr(sys, 'frozen', False):
    config_file = join(dirname(sys.executable), 'config.json')
else:
    config_file = join(dirname(__file__), 'config.json')

with open(config_file, 'r', encoding='utf-8') as f:
    config = load(f)

if __name__ == '__main__':
    play_wordle('Wordling', min_len=config.get('min_length'), max_len=config.get('max_length'))
