import json
import os
import vim

from urllib.error import HTTPError
from urllib.request import urlopen, Request

def edit(instruction):
    api_key = os.getenv('OPENAI_API_KEY')

    data = {
        'input': "\n".join(vim.current.buffer),
        'instruction': instruction,
        'model': 'code-davinci-edit-001',
        'n': 1,
        'temperature': float(vim.eval("g:editai_temperature")),
        # 'top_p': float(vim.eval("g:editai_top_p")),
    }

    req = Request(
        url='https://api.openai.com/v1/edits',
        data=json.dumps(data).encode('utf8'),
        headers={
            'Authorization': 'Bearer %s' % (api_key,),
            'Content-Type': 'application/json',
        }
    )

    try:
        with urlopen(req) as res:
            encoded = res.read().decode('utf8')
            response = json.loads(encoded)

            vim.current.buffer[:] = response['choices'][0]['text'].strip().split("\n")
    except HTTPError as e:
        print(e.read().decode('utf8'))
