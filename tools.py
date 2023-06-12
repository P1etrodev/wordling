from os import system
from random import choice
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from nltk.corpus import stopwords
from nltk import download
from glob import glob

download('stopwords', quiet=True)

letters = 'abcdefghijklmnñopqrstuvwxyz'.upper()
sw = stopwords.words('spanish')

# def filter_word(word):
#     return (len(word) >= min_len and len(word) <= max_len) and (word not in sw) and (not any([char in 'áéíóú' or char in '“”1234567890«¡!"·$%&/()=?¿[]{}`+Ç¨-_.:,;<>' for char in word]))
def filter_word(word, min_len = 4, max_len = 7):
    invalid_chars = set('áéíóú“”1234567890«¡!"·$%&/()=?¿[]{}`+Ç¨-_.:,;<>')
    return len(word) >= min_len and len(word) <= max_len and word not in sw and not any(char in invalid_chars for char in word)

# def get_words():
#     text_files = glob('**/*.txt', root_dir='.')
#     text_files = ['./texts/cuento.txt'] + text_files
#     content = ''
#     for f in text_files:
#         with open(f, 'r', encoding='utf-8') as file:
#             content += file.read().lower()
#     words = set(filter(filter_word, content.split()))
#     return list(words)

def get_words():
    text_files = glob('**/*.txt', recursive=True)
    text_files = ['./texts/cuento.txt'] + text_files
    words = set()
    
    for f in text_files:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read().lower()
            words.update(filter(filter_word, content.split()))

    return list(words)

def get_word(words):
    result = choice(words).upper()
    return result

def get_table(word):
    return Table(*[f'Letra {i}' for i, _ in enumerate(word, 1)], show_header=False, show_lines=True)

# def count_char(word, char):
#     import re
#     pattern = re.escape(char) + '+'
#     return len(pattern.findall(word))

def count_char(word, char):
    count = 0
    for c in word:
        if c == char:
            count += 1
    return count

# def check_word(word: str, guess: str):
#     result = []
#     _word = word
#     for g, _w in zip(guess, _word):

#         if g not in _word:
#             formatted_char = f'[red]{g}[/red]'
#         else:
#             if g == _w:
#                 formatted_char = f'[green]{g}[/green]'
#                 _word = _word.replace(g,'', 1)
#             else:
#                 formatted_char = f'[yellow]{g}[/yellow]'
#                 _word = _word.replace(g,'', 1)

#         formatted_char = f'[bold]{formatted_char}[/bold]'
#         result.append(formatted_char)

#     return result

def check_word(word: str, guess: str):
    result = []
    remaining_chars = list(word)
    
    for g, _w in zip(guess, word):
        if g not in remaining_chars:
            formatted_char = f'[red]{g}[/red]'
        elif g == _w:
            formatted_char = f'[green]{g}[/green]'
            remaining_chars.remove(g)
        else:
            formatted_char = f'[yellow]{g}[/yellow]'
            remaining_chars.remove(g)
            
        formatted_char = f'[bold]{formatted_char}[/bold]'
        result.append(formatted_char)
    
    return result

def get_alpha(checked_result: str, prev_alpha: str):
    import re
    alpha = []
    for char in 'abcdefghijklmnñopqrstuvwxyz':
        pattern = re.compile(r'(\[(?:[^(bold)])[a-z]+\]({})\[\/(?:[^(bold)])[a-z]+\])'.format(char), flags=re.IGNORECASE)
        test = ''.join(checked_result).lower()
        match = pattern.search(test)
        if prev_char:=pattern.search(prev_alpha):
            if match and match.group(1).lower() != prev_char.group(1).lower() and not 'green' in prev_char.group(1).lower():
                alpha.append(match.group(1).replace(f']{char}[', f']{char.upper()}['))
            else:
                alpha.append(prev_char.group(1))
            continue
        if not match:
            alpha.append(char.upper())
        else:
            alpha.append(match.group(1).replace(f']{char}[', f']{char.upper()}['))
    return ' '.join(alpha[:14]) +'\n'+ ' '.join(alpha[14:])

# def get_alpha(checked_result: str, prev_alpha: str):
#     alpha = []
#     checked_result = checked_result.lower()
#     prev_alpha = prev_alpha.lower()
    
#     for char in 'abcdefghijklmnñopqrstuvwxyz':
#         if char in prev_alpha:
#             prev_char = prev_alpha[prev_alpha.index(char)]
#             if char in checked_result and checked_result.index(char) != prev_alpha.index(char):
#                 alpha.append(checked_result.replace(char, char.upper()))
#             else:
#                 alpha.append(prev_char)
#         else:
#             alpha.append(char.upper())
    
#     alpha_chunked = [alpha[:14], alpha[14:]]
#     return '\n'.join([' '.join(chunk) for chunk in alpha_chunked])

# def get_guess(console, word, attempts):
#     guess = console.input('[purple]Introduzca una palabra:[/purple] \n').upper()
#     if len(guess) != len(word):
#         console.print(f'\nTu palabra debe tener {len(word)} caracteres.\n', style='yellow')
#         guess = get_guess(console, word, attempts)
#     if guess in attempts:
#         console.print('\nYa intentaste con esa palabra.\n', style='yellow')
#         guess = get_guess(console, word, attempts)
#     if any([n in guess for n in '1234567890']):
#         console.print('\nTu respuesta no puede contener números.\n', style='yellow')
#         guess = get_guess(console, word, attempts)
#     return guess

def get_guess(console, word, attempts):
    while True:
        guess = console.input('[purple]Introduzca una palabra:[/purple] \n').upper()
        
        if len(guess) != len(word):
            console.print(f'\nTu palabra debe tener {len(word)} caracteres.\n', style='yellow')
            continue
        
        if guess in attempts:
            console.print('\nYa intentaste con esa palabra.\n', style='yellow')
            continue
        
        if any(char.isdigit() for char in guess):
            console.print('\nTu respuesta no puede contener números.\n', style='yellow')
            continue
        
        return guess

def play_again(console):
    answer = console.input('\nVolver a intentar? [S/N]: \n').upper()
    if answer == 'S':
        return True
    elif answer == 'N':
        return False
    else:
        return play_again(console)

# def play_wordle(game_name):
#     console = Console()
#     words = get_words()
#     try:
#         word = get_word(words)
#         max_attempts = 6

#         attempts = []
#         attempts_table = None
#         guess = None
#         alpha = ''
        
#         while len(attempts) < max_attempts:
#             system('cls')
#             console.print(Markdown(f'# {game_name}'))
#             console.print('[red]CTRL+C para salir[/red]')
#             if attempts_table:
#                 console.print(attempts_table)
#             if alpha:
#                 console.print(alpha)
#             # console.print(f'\n[bold]{" ".join()}[/bold]\n')
#             console.print(f'\n[bold]Intento {len(attempts) + 1}/{max_attempts} [yellow]({len(word)} caracteres)[/yellow][/bold]\n')

#             guess = get_guess(console, word, attempts)
#             result = check_word(word, guess)
#             attempts.append(guess)

#             if not attempts_table:
#                 attempts_table = get_table(word)
#             # if not alpha:
#             alpha = get_alpha(result, alpha)
#             attempts_table.add_row(*result)

#             if guess == word:
#                 system('cls')
#                 console.print(Markdown('# '+game_name))
#                 console.print(attempts_table)
#                 console.print('\nCorrecto! Ganaste!\n', style='bold green')
#                 if not play_again(console):
#                     system('cls')
#                     return
#                 attempts_table = None
#                 guess = None
#                 attempts = []
#                 alpha = ''
#                 word = get_word(words)

#         system('cls')
#         console.print(Markdown('# '+game_name))
#         console.print(attempts_table)
#         console.print('\nPerdiste.', style='bold red underline')
#         console.print(f'\nTu palabra era:', style='yellow')
#         console.print('\n'+word, style='bold purple')
#         if play_again(console):
#             play_wordle(game_name)
#     except KeyboardInterrupt:
#         system('cls')

def play_wordle(game_name):
    console = Console()
    console.clear()
    console.print(Markdown(f'# {game_name}'))
    console.print('Cargando...', style='bold purple')
    words = get_words()
    try:
        max_attempts = 6

        while True:
            word = get_word(words)

            attempts = []
            attempts_table = None
            guess = None
            alpha = ''
            
            for attempt in range(max_attempts):
                console.clear()
                console.print(Markdown(f'# {game_name}'))
                console.print('[red]CTRL+C para salir[/red]')
                
                if attempts_table:
                    console.print(attempts_table)
                if alpha:
                    console.print(alpha)
                
                console.print(f'\n[bold]Intento {attempt + 1}/{max_attempts} [yellow]({len(word)} caracteres)[/yellow][/bold]\n')

                guess = get_guess(console, word, attempts)
                result = check_word(word, guess)
                attempts.append(guess)

                if not attempts_table:
                    attempts_table = get_table(word)
                
                alpha = get_alpha(''.join(result), alpha)
                attempts_table.add_row(*result)

                if guess == word:
                    console.clear()
                    console.print(Markdown('# '+game_name))
                    console.print(attempts_table)
                    console.print('\nCorrecto! Ganaste!\n', style='bold green')
                    if not play_again(console):
                        console.clear()
                        return
                    break

            else:
                console.clear()
                console.print(Markdown('# '+game_name))
                console.print(attempts_table)
                console.print('\nPerdiste.', style='bold red underline')
                console.print(f'\nTu palabra era:', style='yellow')
                console.print('\n'+word, style='bold purple')
                if not play_again(console):
                    console.clear()
                    return
    except KeyboardInterrupt:
        console.clear()
