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


def filter_word(word, min_len=4, max_len=7):
    invalid_chars = set('áéíóú“”1234567890«¡!"·$%&/()=?¿[]{}`+Ç¨-_.:,;<>äëïöü')
    return len(word) >= min_len and len(word) <= max_len and word not in sw and not any(
        char in invalid_chars for char in word
    )


def get_words(min_len, max_len):
    text_files = glob('**/*.txt', recursive=True)
    text_files = ['./texts/cuento.txt'] + text_files
    words = set()

    for f in text_files:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read().lower()
            words.update(filter(lambda x: filter_word(x, min_len, max_len), content.split()))

    return list(words)


def get_word(words):
    result = choice(words).upper()
    return result


def get_table(word):
    return Table(*[f'Letra {i}' for i, _ in enumerate(word, 1)], show_header=False, show_lines=True)


def count_char(word, char):
    count = 0
    for c in word:
        if c == char:
            count += 1
    return count


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
        pattern = re.compile(
            r'(\[(?:[^(bold)])[a-z]+\]({})\[\/(?:[^(bold)])[a-z]+\])'.format(char),
            flags=re.IGNORECASE,
        )
        test = ''.join(checked_result).lower()
        match = pattern.search(test)
        if prev_char := pattern.search(prev_alpha):
            if match and match.group(1).lower() != prev_char.group(1).lower() and not 'green' in prev_char.group(
                1
            ).lower():
                alpha.append(match.group(1).replace(f']{char}[', f']{char.upper()}['))
            else:
                alpha.append(prev_char.group(1))
            continue
        if not match:
            alpha.append(char.upper())
        else:
            alpha.append(match.group(1).replace(f']{char}[', f']{char.upper()}['))
    return ' '.join(alpha[:14]) + '\n' + ' '.join(alpha[14:])


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
    while True:
        answer = console.input('\nVolver a intentar? [S/N]: \n').upper()
        if answer == 'S':
            return True
        elif answer == 'N':
            return False
        else:
            console.print('Respuesta inválida. Por favor, ingresa S para "Sí" o N para "No".\n', style='yellow')


def play_wordle(game_name, min_len, max_len):
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
                    console.print(Markdown('# ' + game_name))
                    console.print(attempts_table)
                    console.print('\nCorrecto! Ganaste!\n', style='bold green')
                    if not play_again(console):
                        console.clear()
                        return
                    break

            else:
                console.clear()
                console.print(Markdown('# ' + game_name))
                console.print(attempts_table)
                console.print('\nPerdiste.', style='bold red underline')
                console.print(f'\nTu palabra era:', style='yellow')
                console.print('\n' + word, style='bold purple')
                if not play_again(console):
                    console.clear()
                    return
    except KeyboardInterrupt:
        console.clear()

play_wordle('Wordling')
