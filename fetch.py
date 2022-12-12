import sys
import requests


url = f'https://adventofcode.com/2022/day/{sys.argv[1]}/input'
cookies = dict(session=sys.argv[2])
x = requests.get(url, cookies=cookies)

with open(sys.argv[3], 'w') as f:
    f.write(x.text)
