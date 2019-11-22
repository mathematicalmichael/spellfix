import pandas as pd
from spellfix import format_str
import json
a = pd.read_csv('client_list.csv', header=None)
a[0].apply(lambda x: format_str(x))
a = a.set_index([0])
d = a.to_dict()[1]
with open('client_list-unknown-words.json', 'w') as f:
    json.dump(d, f)
with open('client_list.txt', 'w') as f:
    f.write('\n'.join(list(d.keys())))
