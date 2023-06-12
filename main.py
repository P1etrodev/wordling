from json import load
from tools import play_wordle

with open('./config.json', 'r', encoding='utf-8') as f:
    config = load(f)

if __name__ == '__main__':
    play_wordle('Wordling', config.get('min_length'), config.get('max_length'))
