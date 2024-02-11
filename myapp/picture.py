import csv
from openai import OpenAI

def generate_final_prompt_and_create_image(csv_file_path):
    # OpenAIクライアントの初期化
    client = OpenAI(api_key="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")
    
    prompts = []  # 個々のプロンプトを格納する配列
    
    # CSVファイルを開いてデータを読み込む
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # ヘッダーをスキップする場合

        #first_line = True  # 最初の行かどうかを判定するフラグ
        for row in reader:
            product_name = row[1]  # 商品名
            quantity = row[3]  # 本数

            # プロンプトを行に応じて動的に作成、末尾に改行を追加
            #if first_line:
            prompt = f"""
                {quantity} {product_name} in a vase \n"""
            #    first_line = False
            #else:
            #    prompt = f"""
            #    Please generate an image that combines only {quantity} {product_name}.\n"""
            
            prompts.append(prompt)  # 配列にプロンプトを追加

    # 配列内の全てのプロンプトを結合
    final_prompt = "".join(prompts) ,f"""
        Please give me an image that combines these.
        I would like this as a reference image for people who want to enjoy flower arranging.
        For the background, imagine a bright and transparent space.
    """
    
    ################テスト用##################
    #print(f"Product Name: {generate_final_prompt_and_create_image.product_name}, Quantity: {generate_final_prompt_and_create_image.quantity}, Final Prompt: {generate_final_prompt_and_create_image.final_prompt}")
    #########################################

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
        print("Generated image URL:", image_url)
    except Exception as e:
        print("Error generating image:", e)



if __name__ == "__main__":
  #テスト用に環境変数を設定して使う

  print("------------csvファイル生成テスト------------")
  print(generate_final_prompt_and_create_image("/Users/araishuichi/Desktop/ハッカソン_開発フォルダ/test_csvファイル/ハッカソンテスト2.csv"))
  
