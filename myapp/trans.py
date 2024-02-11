import os
import io
import csv
import json
import requests

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

def _trans(text:str, source:str, target:str) -> str:
	request = "https://www.googleapis.com/language/translate/v2?key={}&target={}&source={}&q={}".format(GOOGLE_API_KEY, target, source, text)
	response = requests.get(request)
	text = json.loads(response.text)["data"]["translations"][0]["translatedText"]
	return text

def trans_csv_io(io) -> str:
	response = []

	reader = csv.reader(io)
	for row in reader:
		flower_name = row[0]

		if isinstance(flower_name, bytes):
			flower_name = flower_name.decode("utf-8")
		result = _trans(flower_name, "ja", "en")

		response.append("{},{}".format(result, row[2]))

	return "\n".join(response)

def trans_csv_text(csvtext:str) -> str:
	f = io.StringIO()
	f.write(csvtext)
	f.seek(0)
	return trans_csv_io(f)


if __name__ == "__main__":
  print("------------インプット------------")
  str = """カーネーション(白),200,3,600
カーネーション(赤),200,1,200
カーネーション(黄),200,1,200"""
  print(str)
  print("------------翻訳テスト------------")
  resipe = trans_csv_text(str)
  print(resipe)
