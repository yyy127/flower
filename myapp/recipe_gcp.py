import os
import google.generativeai as genai

def _flower_list() -> str:
  return """商品名,色,購入できる季節,一本の価格[円]
バラ(赤),赤,春と秋,300
バラ(ピンク),ピンク,春と秋,300
バラ(黄),黄,春と秋,300
バラ(白),白,春と秋,300
バラ(オレンジ),オレンジ,春と秋,300
バラ(紫),紫,春と秋,300
ユリ(白),白,夏,300
ユリ(黄),黄,夏,300
ユリ(ピンク),ピンク,夏,300
ラン(三本立ち),白,通年,10000
ガーベラ(赤),赤,春から秋,200
ガーベラ(黄),黄,春から秋,200
ガーベラ(ピンク),ピンク,春から秋,200
カーネーション(ピンク),ピンク,春から初冬,200
カーネーション(白),白,春から初冬,200
カーネーション(赤),赤,春から初冬,200
カーネーション(黄),黄,春から初冬,200
チューリップ(赤),赤,冬から春,200
チューリップ(黄),黄,冬から春,200
チューリップ(オレンジ),オレンジ,冬から春,200
チューリップ(ピンク),ピンク,冬から春,200
チューリップ(白),白,冬から春,200
チューリップ(紫),紫,冬から春,200
アジサイ(青),青,梅雨,1000
アジサイ(白),白,梅雨,1000
アジサイ(緑),緑,梅雨,1000
ヒマワリ,黄,夏,200
菊(白),白,秋から冬,250
菊(黄),黄,秋から冬,250
菊(青),青,秋から冬,250
菊(ピンク),ピンク,秋から冬,250"""

def _make_system_prompt() -> str:
  system_prompt = """
###指示###あなたは花屋の店主です。
ユーザーからは季節と予算とイメージが入力されます。
花の商品リストからお客様のイメージに沿う花を組み合わせて出力してください。
また、商品リストは商品名、色、購入できる季節、一本の価格がcsv形式になっています。

###商品リスト###
商品名,色,購入できる季節,一本の価格[円]
%商品一覧%

###ユーザー入力###
季節,予算(上限合計金額),イメージ

###出力###
* 合計金額
* 商品名,単価,数量,金額(単価×数量)

###制約###
合計金額がユーザー入力の上限合計金額を超えないようにしてください。
"""
  return system_prompt.replace("%商品一覧%", _flower_list())

def _make_prompt_parts(budget:str, command:str, season:str) -> list[str]:
  return [
    _make_system_prompt(),
    "ユーザー入力 2024/11/13,2000円,ゴージャス",
    "合計金額 1900",
    "出力 バラ(赤),300,3,900\nバラ(ピンク),300,2,600\nチューリップ(赤),200,2,400",
    "ユーザー入力 2024/8/1,1000円,落ち着いた雰囲気",
    "合計金額 1000",
    "出力 カーネーション(白),200,3,600\nカーネーション(赤),200,1,200\nカーネーション(黄),200,1,200",
    "ユーザー入力 冬,5000円,大人な雰囲気",
    "合計金額 5000",
    "出力 菊(白),250,8,2000\n菊(黄),250,4,1000\n菊(青),250,4,1000\n菊(ピンク),250,4,1000",
    "ユーザー入力 {},{},{}".format(season, budget, command),
    "合計金額 ",
  ]

def _call_core(prompt_parts:list[str]) -> str:
  GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
  genai.configure(api_key=GOOGLE_API_KEY)

  # Set up the model
  generation_config = {
    "temperature": 0.5,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
  }

  safety_settings = [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
  ]

  model = genai.GenerativeModel(model_name="gemini-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)
  return model.generate_content(prompt_parts).text

def _format_csv(response:str) -> str:
  # "出力"の文字があるかチェック
  is_output_phrase = response.find("出力")
  if is_output_phrase >= 0:
    return response.split("出力")[1].lstrip()
  
  # 改行文字が存在するかチェック
  first_lf = response.find("\n")
  if first_lf >= 0:
    return response[first_lf+1:]

  return response

def think_flower_recipe(budget:str, command:str, season:str) -> str:
  prompt = _make_prompt_parts(budget, command, season)
  response = _call_core(prompt)
  print(response)
  response_csv = _format_csv(response)
  return response_csv

if __name__ == "__main__":
  import datetime

  print("------------_format_csvテスト------------")
  test_text_1 = """1000出力 チューリップ(白),200,2,400
チューリップ(ピンク),200,2,400
チューリップ(黄),200,2,400
チューリップ(紫),200,2,400"""
  print("------------_format_csvテスト1 before------------")
  print(test_text_1)
  print("------------_format_csvテスト1 after------------")
  print(_format_csv(test_text_1))

  test_text_2 = """1000
チューリップ(白),200,2,400
チューリップ(ピンク),200,2,400
チューリップ(黄),200,2,400
チューリップ(紫),200,2,400"""
  print("------------_format_csvテスト2 before------------")
  print(test_text_2)
  print("------------_format_csvテスト2 after------------")
  print(_format_csv(test_text_2))

  test_text_3 = """チューリップ(紫),200,2,400"""
  print("------------_format_csvテスト3 before------------")
  print(test_text_3)
  print("------------_format_csvテスト3 after------------")
  print(_format_csv(test_text_3))

  print("------------Geminiテスト------------")
  resipi = think_flower_recipe("1000 円", "炭酸水がおいしいイメージ", datetime.datetime.today().strftime("%Y/%m/%d"))
  print("------------Geminiテスト 結果------------")
  print(resipi)
