#python3

import json
import requests
# 讀取Jupyter Notebook檔案的內容
def get_content_of_notebook(notebook_path, base, headers):
    url = base + '/api/contents' + notebook_path
    response = requests.get(url, headers=headers)
    file = json.loads(response.text)
return file['content']
