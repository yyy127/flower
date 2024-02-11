import os
import io
import csv
from openai import OpenAI

def generate_final_prompt_and_create_image(csv_text:str) -> str:
    # OpenAIクライアントの初期化
    OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # 文字列をcsvライブラリで扱うためのIO
    f = io.StringIO()
    f.write(csv_text)
    f.seek(0)

    prompts = []  # 個々のプロンプトを格納する配列
    
    reader = csv.reader(f)
    #next(reader, None)  # ヘッダーをスキップする場合

    #first_line = True  # 最初の行かどうかを判定するフラグ
    for row in reader:
        product_name = row[0]  # 商品名
        quantity = row[1]  # 本数

        # プロンプトを行に応じて動的に作成、末尾に改行を追加
        #if first_line:
        prompt = f"{quantity} {product_name} in a vase."
        #    first_line = False
        #else:
        #    prompt = f"""
        #    Please generate an image that combines only {quantity} {product_name}.\n"""
        
        prompts.append(prompt)  # 配列にプロンプトを追加

    # 配列内の全てのプロンプトを結合
    final_prompt = "\n".join(prompts) + """Please give me an image that combines these.
I would like this as a reference image for people who want to enjoy flower arranging.
For the background, imagine a bright and transparent space."""
    
    # 結合したプロンプトを使用して画像を生成
    try:
        response = client.images.generate(
            model="dall-e-2",
            prompt=final_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        # 生成された画像のURLを出力
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        print("Error generating image:", e)



if __name__ == "__main__":
    #テスト用に環境変数を設定して使う

    print("------------入力データ------------")
    csv_text = """Carnation (white),3
Carnation (red),1
Carnation (yellow),1"""
    print("------------画像生成テスト------------")
    print(generate_final_prompt_and_create_image(csv_text))
    
