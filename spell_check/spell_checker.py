import requests
import json
import re
import sys
import io

# sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

class SpellChecker:
    def __init__(self):
        self.passport_key = None
        self.base_url = None

    def fetch_passport_key(self):
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://search.naver.com/',
        }
        response = requests.get("https://search.naver.com/search.naver?query=맞춤법+검사기", headers=headers)
        match = re.search(r'(?<={new SpellingCheck\({API:{checker:").*?(?="},selector)', response.text)
        if not match:
            raise RuntimeError("Error: Unable to retrieve passport key from Naver page.")
        self.base_url, self.passport_key = match.group(0).split("?passportKey=")

    def spell_check(self, text):
        if self.passport_key is None or self.base_url is None:
            self.fetch_passport_key()
        payload = {
            'passportKey': self.passport_key,
            'where': 'nexearch',
            'color_blindness': 0,
            'q': text
        }
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://search.naver.com/',
        }
        result_response = requests.get(self.base_url, headers=headers, params=payload)
        result_json = result_response.json()
        return result_json['message']['result']['notag_html']