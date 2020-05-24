import argparse
import pandas as pd


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
    hour = date_hour[-8:]

    return {'book': book_author,
            'text': text,
            'type': text_type,
            'page': page,
            'position': position,
            'date': date,
            'hour': hour}


def dataframe_from_notes(save=True, filename='clippings.csv', filter_by=None):

    # TODO: check if already exists '.csv'

    notes_file = 'My Clippings.txt'

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='retrieve notes from kindle')
    parser.add_argument('--list-authors', action='store_true')
    parser.add_argument('--build-all', action='store_true')
    parser.add_argument('--build-only')
    parser.add_argument('--columns')
    parser.add_argument('--save')
    args = parser.parse_args()

    result = None
    
    if args.list_authors:
        notes = dataframe_from_notes(save=False)
        print(notes.book.unique())
    elif args.build_only is not None:
        column, query = args.build_only.split('=')
        notes = dataframe_from_notes(save=False)
        if args.columns is not None:
            columns = args.columns.split(',')
            result = notes.query(f'{column} == "{query}"')[columns]
        else:
            result = notes.query(f'{column} == "{query}"')
    elif args.build_all:
        dataframe_from_notes()

    if result is not None and args.save is not None:
        if args.save == 'json':
            result.to_json('result.json', orient='records', force_ascii=False)
        if args.save == 'csv':
            result.to_csv('result.csv')
    elif result is not None:
        print(result)


