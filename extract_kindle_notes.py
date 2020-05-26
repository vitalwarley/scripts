import re
import argparse
from datetime import datetime
import pandas as pd


def convert_date(date):
    months = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
            'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
    months_dict = dict(zip(months, range(1, 13)))
    day, month, year = date.split(' de ')
    day = int(day)
    month = months_dict[month]
    year = int(year)
    return datetime(year, month, day)
    

def extract_info(nota):
    """
    Types of clippings

        Tao Te Ching: O Livro do Caminho e da Virtude (Tse, Lao)
        - Sua nota ou posição 187 | Adicionado: quinta-feira, 10 de outubro de 2019 22:52:45
        
        Conhecimento de si é um conhecimento nao-vazio?

        Game Of Life (Leary, Timothy)
        - Seu destaque ou posição 1089-1091 | Adicionado: domingo, 1 de setembro de 2019 23:13:35
        
        Crowley’s transmissions were primarily concerned with the Fifth Circuit. Sex-magick. Self-definition as a polymorphous erotic receiver. Somatic control. The tantric union of male-female. The Pan, Dionysus rapture myth. The alchemy of aphrodisiac drugs.

        Atomic Habits (Clear, James)
        - Sua nota na página 45 | posição 619 | Adicionado: sexta-feira, 22 de maio de 2020 08:50:36
        
        Effective to what metric? Energy consumption I guess. Principle of the least effort.

        Ultralearning (Young, Scott)
        - Seu destaque na página 69 | posição 1010-1011 | Adicionado: sábado, 23 de maio de 2020 10:00:47
        
        The benefits of ultralearning aren’t always apparent from the first project because that first project occurs when you’re at your lowest level of metalearning ability.

    They all follow the same structure, except at second line, esp. in highlight_position
        0 book_author
        1 highlight_page_position [ | position ] | date_hour
        2
        3 text

    Spliting the second line with "|" can give a list with len = 2 or len = 3

    So, except the date_hour, the split of the second line can have
        'Sua nota ou posição X[-Y]'
        'Seu destaque ou posição X[-Y]'
        'Sua nota na página X[-Y]' and 'posição X[-Y]'
        'Seu destaque na página X[-Y]' and 'posição X[-Y]'

    Then we check len and split by ' ' accordingly.
    """
    parts = nota.split('\n')
    text = parts[3]
    book_author = parts[0].replace('\ufeff', '').strip()
    text_type = None
    position = None
    page = None

    *text_type_position, date_hour = parts[1].split(' | ')
    if len(text_type_position) == 1:
        text_type_position = text_type_position[0].split(' ')
        text_type = text_type_position[2]
        position = text_type_position[-1]
    else: # 2
        text_type_page = text_type_position[0].split(' ')
        text_type = text_type_page[2]
        page = text_type_page[-1]
        position = text_type_position[1].split(' ')[1]
    date_hour = date_hour.split(', ')[1]
    date = date_hour[:-9]
    date = convert_date(date)
    hour = date_hour[-8:]

    if page is None:
        page = 0

    page = int(page)

    return {'book': book_author,
            'text': text,
            'type': text_type,
            'page': page,
            'position': position,
            'date': date,
            'hour': hour}


def dataframe_from_notes(notes_file, save=True, filename='clippings.csv', filter_by=None):
    """Convert kindle clippings to dataframe."""

    # TODO: check if already exists '.csv'

    with open(notes_file, 'r', encoding='utf-8-sig') as f:
        lines = f.read()

    notes = lines.split('=' * 10 + '\n')[:-1]  # discard last empty

    notes_df = pd.DataFrame([], columns=['book', 'text', 'type', 'page', 'position', 'date', 'hour'])
    for i, note in enumerate(notes):
        info = extract_info(note)
        notes_df = notes_df.append([info], ignore_index=True)

    if filter_by is not None:
        notes_df = notes_df.query('book = filter_by')
    
    if save and isinstance(filename, str):
        notes_df.to_csv(filename)
    else:
        return notes_df


def parse_filter_options(options):
    # split columns
    # TODO: improve regex manipulation; this way column keys can be a substring in column values
    columns = ['book', 'text', 'type', 'page', 'position', 'date', 'hour']
    regex = ("({})|" * len(columns)).format(*columns)[:-1] 
    regex = '(' + '|'.join(columns) + ')'
    regex = re.compile(regex)
    split = re.split(regex, options)[1:]
    keys = split[::2]
    # split op and value
    regex = re.compile('(=|>|<)')
    ops_values = split[1::2]
    ops_values = [re.split(regex, ov)[1:] for ov in ops_values] 
    # make dict
    options = {}
    for key, ov in zip(keys, ops_values):
        # op can be [op, '', op, value] or [op, value]
        op = ov[:-1]
        if len(op) > 1:
            op = op[0] + op[2]
        else:
            op = op[0]
        value = ov[-1]
        if value[-1] == ',': value = value[:-1]
        options[key] = dict(op=op, value=value)

    return options


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='retrieve notes from kindle')
    parser.add_argument('--list-authors', action='store_true')
    parser.add_argument('--columns')
    parser.add_argument('--save')
    parser.add_argument('--input')
    parser.add_argument('--output')
    parser.add_argument('--filter', help="filter data (i.e. date='2020-05-25'). you can add more filters with ','")
    parser.add_argument('--sort-by')
    args = parser.parse_args()

    if args.input is None:
        print("Error: Need a input file!")
        import sys
        sys.exit()
    else:
        notes_file = args.input

    if args.output is None:
        output = 'result'
    else:
        output = args.output

    result = None

    if args.list_authors:
        notes = dataframe_from_notes(notes_file, save=False)
        # result = notes.book.unique()
        result = notes.groupby('book').size().to_json(force_ascii=False)
    elif any([args.sort_by, args.filter, args.columns]):
        result = dataframe_from_notes(notes_file, save=False)

        if args.sort_by is not None: 
            col = args.sort_by
            result = result.iloc[eval(f'result.{col}.sort_values().index')]

        if args.filter is not None:
            # now a dict
            # for example: book='Atomic Habits (Clear, James)',date='2020-05-25'
            # { book: { op: '=', value: 'Atomic Habits (Clear, James)' },
            #   date: { op: '=', value: '2020-05-25' }}
            options = parse_filter_options(args.filter)
            for key in options:
                value = options[key]['value']
                op = options[key]['op']
                if op not in ['<', '<=', '>', '>=', '=']:
                    raise ValueError('Incorrect filter operation!')
                if op == '=': op += '='
                result = result.query(f'{key} {op} "{value}"')

        if args.columns is not None:
            columns = args.columns.split(',')
            result = result[columns]
    else:
        dataframe_from_notes(notes_file)

    if result is not None and args.save is not None:
        if args.save == 'json':
            result.to_json(f'{output}.json', orient='records', force_ascii=False)
        if args.save == 'csv':
            result.to_csv(f'{output}.csv')
    elif result is not None:
        import json
        result = json.loads(result)
        for book in result:
            print('Total notes: {:5} \t Book: {}'.format(result[book], book))

