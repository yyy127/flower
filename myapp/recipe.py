from openai import OpenAI

def _call_core(system_prompt, user_prompt):
  client = OpenAI()
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {
        "role": "system",
        "content": system_prompt
      },
      {
        "role": "user",
        "content": user_prompt
      },
    ],
    temperature=0.3,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )

  return response.choices[0].message.content

def _make_system_prompt(budget, month):
  prompt = """###指示###
あなたは花屋の店主です。
花の商品リストからお客様のイメージに沿う花を予算内でなるべく購入できるように選んでください。
商品リストは商品名、色、購入できる季節、一本の価格がcsv形式になっています。
結果は出力形式のフォーマットで応答してください。

###今の季節###
%季節%

###予算###
%予算%

###商品リスト###
商品名,色,購入できる季節,一本の価格(円)
バラ(赤),赤,2月から6月,300
バラ(青),青,2月から6月,300
たんぽぽ,黄,5月から8月,100

###出力形式###
商品名,金額,本数
"""
  return prompt.replace("%季節%", month).replace("%予算%", budget)

def think_flower_recipe(budget, command):
  system_prompt = _make_system_prompt(budget, "4月")
  return _call_core(system_prompt, command)


if __name__ == "__main__":
  #テスト用に環境変数を設定して使う

  print("------------プロンプト生成テスト------------")
  print(_make_system_prompt("100円", "8月"))

  print("------------chatgptテスト------------")
  resipi = think_flower_recipe("3000円", "素朴")
  print(resipi)
