import os
import sys
import pandas as pd
import pyperclip

filename = sys.argv[1]
notes = pd.read_csv(
    filename,
    header=0,
    names=["type", "position", "star", "annotation"],
    skiprows=[1, 2, 3, 4, 5, 6, 7],
)

notes['type'] = notes.type.str.split(r'(Nota|Amarelo|Azul|Rosa)', expand=True)[1]

output = ''
previous = None
tabs = {'Azul': 2, 'Amarelo': 3, 'Rosa': 4}
for idx, row in notes.iterrows():
    if row.type == 'Azul':
        output += f'\t- {row.annotation}\n'
    elif row.type == 'Amarelo':
        output += f'\t\t- {row.annotation}\n'
    elif row.type == 'Rosa':
        output += f'\t\t\t- {row.annotation}\n'
    elif row.type == 'Nota':
        output += "{}- {}\n".format(tabs[previous] * '\t', row.annotation)
    previous = row.type

pyperclip.copy(output)
