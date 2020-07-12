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

notes['type'] = notes.type.str.split(r'(Nota|Amarelo|Azul)', expand=True)[1]

output = ''
for idx, row in notes.iterrows():
    if row.type == 'Azul':
        output += f'\t- {row.annotation}\n'
    else:
        output += f'\t\t- {row.annotation}\n'

pyperclip.copy(output)
