from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import myapp.recipe_gcp
import myapp.trans
import myapp.picture
import csv
import datetime

# Create your views here.
def input(request):
    # GETリクエストの処理: 初期フォームを表示
    return render(request, 'myapp/input.html')

@csrf_protect
def response(request):
    # POSTリクエストの処理: フォームデータを変数に格納
    textbox1_value = request.POST.get('textboxBudget')
    textbox2_value = request.POST.get('textboxCommand')
    
    # ここで変数の値を使って何かする
    if textbox1_value == None:
        # 何かしらの処理。例えばデフォルト値を設定するなど。
        textbox1_value = "2000"

    if textbox2_value == None:
        # 何かしらの処理。例えばデフォルト値を設定するなど。
        textbox2_value = "春の季節をイメージした花束を、食卓に飾りたいです。花だけでなく、葉も入れた花束で、落ち着いた大人な雰囲気の花束にしてください。"

    csv_data = myapp.recipe_gcp.think_flower_recipe(textbox1_value + "円", textbox2_value, datetime.datetime.today().strftime("%Y/%m/%d"))

    # 画像生成に投げるCSV
    # 次のような文字列
    #------------インプット------------
    #カーネーション(白),200,3,600
    #カーネーション(赤),200,1,200
    #カーネーション(黄),200,1,200
    #------------翻訳テスト------------
    #Carnation (white),3
    #Carnation (red),1
    #Carnation (yellow),1
    image_recipe_csv = myapp.trans.trans_csv_text(csv_data)

    image_url = myapp.picture.generate_final_prompt_and_create_image(image_recipe_csv)

    lines = csv_data.splitlines()
    reader = csv.reader(lines)
    parsed_csv = list(reader)  # パースされたCSVデータをリストに変換

    # 合計額が間違っている可能性があるため再計算をする
    for row in parsed_csv:
        unit_price = int(row[1])  # 単価
        quantity = int(row[2])    # 数量
        total_price = unit_price * quantity  # 合計額の計算
        row[3] = str(total_price)  # 計算した合計額をリストに戻す

    # 合計金額を計算
    total_amount = sum(int(row[3]) for row in parsed_csv)

    # テンプレートにデータを渡す
    context = {
        'textbox1_value': textbox1_value,
        'textbox2_value': textbox2_value,
        'data': parsed_csv,
        'image_url': image_url,
        'total_amount': total_amount,
    }
    return render(request, 'myapp/response.html', context)

    # # テンプレートにデータを渡す
    # context = {'data': parsed_csv}
    # return render(request, 'myapp/response.html', {
    #     'textbox2_value': context,
    #     'image_url': image_url,
    # })