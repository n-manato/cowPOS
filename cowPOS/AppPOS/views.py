# 個々のページのviews

from django.shortcuts import render
from datetime import datetime, timedelta
from django.views import View
from django.db.models import Max, Min
from . import models
from django.utils import timezone
from django.utils.timezone import localtime
from django.urls import reverse
import json

# http://127.0.0.1:8000/pos_page/


def pos_page(request):
    # 初期化等
    Prodacts_Info = models.Prodact_Name.objects.all()
    Prodacts_dict = {}

    # Prodactを辞書型へ
    for data in Prodacts_Info:
        Prodacts_dict[data.P_name] = data.P_price
    print(Prodacts_dict)

    # SUBMITボタンが押された時

    if request.method == 'POST':
        print(request.POST)
        for data in Prodacts_Info:
            submited = models.Accounting_Data()
            print(data)
            submited.name = data
            submited.price = data.P_price
            submited.saled = request.POST.get('saled' + data.P_name)
            submited.save()
  
    menu_items = [
        {'name': 'Submit', 'url': reverse('AppPOS:POS_page')},
        {'name': 'Results', 'url': reverse('AppPOS:results')},
        {'name': 'Order', 'url': reverse('AppPOS:order')},
        {'name': 'Admin', 'url': reverse('admin:index')},
    ]

    stats = {
        'Prodacts_dict': Prodacts_dict,
        'menu_items': menu_items,
    }
    
    return render(request, 'POS_page.html', stats)


# http://127.0.0.1:8000/results/
def results_page(request):
    # 初期化等ß
    today_date = timezone.now() #- timedelta(days=1)
    Prodacts_Info = models.Prodact_Name.objects.all()
    Accounting_Info = models.Accounting_Data.objects.filter(
        c_time__date=today_date)
    max_date = today_date
    min_date = today_date
    max_date = models.Accounting_Data.objects.filter(
        c_time__date=today_date).aggregate(Max('c_time'))['c_time__max']
    min_date = models.Accounting_Data.objects.filter(
        c_time__date=today_date).aggregate(Min('c_time'))['c_time__min']
    accounting_dict = {}
    # 1時間ごとのリストを作成
    date_list = []
     # 最小日付から開始
    if max_date is None:
        max_date = today_date
    if min_date is None:
        min_date = today_date
    current_date = min_date  
    total_price = 0
    sumtotal_price = 0
    total_skewer = 0
    totals_price = []
    print(max_date)
    print(min_date)

    # 日付作成
    while current_date <= max_date + timedelta(minutes=1):
        date_list.append(current_date.strftime("%H:%M:00"))
        current_date += timedelta(minutes=1)
    
    # totalデータ作成
    for date in date_list:
        for data in Accounting_Info:
            if data.c_time.strftime("%H:%M:00") == date:
                total_price += data.price * data.saled
                total_skewer += data.saled
        totals_price.append(total_price)
        total_price = 0
    sumtotal_price = sum(totals_price)
    print('totals_price:', totals_price)
    print('sumtotal_price:', sumtotal_price)
    print('total_skewer:', total_skewer)

    # accountingデータ作成
    # P_nameごとにデータ挿入
    for accounting in Prodacts_Info:
        accounting_dict[accounting.P_name] = []
    for data in Prodacts_Info:
        for data2 in Accounting_Info:
            if data.P_name == data2.name.P_name:
                accounting_dict[data.P_name].append(data2.price * data2.saled)

    # 商品名と時間ごとの合計&各商品の売れた串数
    accounting_timedata = {}
    times_skewer = {}
    timedata = 0
    timeskewer = 0
    for accounting in Prodacts_Info:
        accounting_timedata[accounting.P_name] = []
        times_skewer[accounting.P_name] = []
    for date in date_list:
        for data in Prodacts_Info:
            for data2 in Accounting_Info:
                if data.P_name == data2.name.P_name and data2.c_time.strftime("%H:%M:00") == date:
                    timedata += data2.price * data2.saled
                    timeskewer += data2.saled
            accounting_timedata[data.P_name].append(timedata)
            times_skewer[data.P_name].append(timeskewer)
            timedata = 0
            timeskewer = 0
    print('accounting_timedata:', accounting_timedata)
    # 　それぞれの売れた串の数をsum
    for key, data in times_skewer.items():
        times_skewer[key] = []
        times_skewer[key] = sum(data)
    print('times_skewer:', times_skewer)

    # 各商品の合計金額
    for key, value in accounting_dict.items():
        accounting_dict[key] = []
        accounting_dict[key] = sum(value)
    print('accounting_dict;', accounting_dict)

    # 一人当たりの配当金

    give_maney = 0
    people = 31
    dividend = 0
    dividend = (sumtotal_price - give_maney) / people

    # 時間の調整
    fix_date_list = []
    for date_str in date_list:
        original_date = datetime.strptime(date_str, "%H:%M:00")
        fix_date = original_date + timedelta(minutes=9)
        fix_date_str = fix_date.strftime("%H:%M:00")
        fix_date_list.append(fix_date_str)
    print('fix_date_list:', fix_date_list)

    menu_items = [
        {'name': 'Submit', 'url': reverse('AppPOS:POS_page')},
        {'name': 'Results', 'url': reverse('AppPOS:results')},
        {'name': 'Order', 'url': reverse('AppPOS:order')},
        {'name': 'Admin', 'url': reverse('admin:index')},
    ]

    stats = {
        'dividend': json.dumps(int(dividend)),  # 一人当たりの配当金(int)
        'dates': json.dumps(fix_date_list),  # 日付リスト(list)
        # 　合計金額
        'accounting_dict': json.dumps(accounting_dict),  # 各商品の合計金額（dict）
        'sumtotal_price': json.dumps(sumtotal_price),  # 全体の合計金額（int）
        # １時間ごとの金額
        # 各商品の1時間ごとの金額(dict)
        'accounting_timedata': json.dumps(accounting_timedata),
        'totals_price': json.dumps(totals_price),  # 全体のの1時間ごとの金額(dict)
        # 串関連
        'times_skewer': json.dumps(times_skewer),  # 各商品ごとの串合計データ(dict)
        'total_skewer': json.dumps(total_skewer),  # 串の合計(int)
        'menu_items': menu_items,
    }
    return render(request, 'results.html', stats)

def order_page(request):
    # --- 変数初期化 ---
    ord_id = []
    name = []
    saled = []
    date = []
    target_day = datetime(2023, 10, 22)
    target_time = timezone.make_aware(target_day)
    print(target_time)
        
    # --- リロードされたとき ---
    if request.method == 'POST':
        print('post!!')
        new_id = request.POST['ord_id'].split(',')
        new_name = request.POST['name'].split(',')
        new_saled = request.POST['saled'].split(',')
        new_date = request.POST['date'].split(',')
        check_list = request.POST['check_list'].split(',')
        print(check_list)
        # --- チェックボックスが入力された行を取得 ---
        for i, tmp in enumerate(check_list):
            if tmp == 'true':
                index = i
            else:
                break
        print(new_date[index])
        print(target_day.strptime("%H:%M:%S"))
        target_time = datetime.today().strptime("%Y-%m-%d %H:%M:%S")
        print(target_time)
        
    # target_timeより新しく追加されたデータを取得
    target_time_after = models.Accounting_Data.objects.filter(c_time__gt=target_time)
    for data in target_time_after:
        if data.saled != 0:
            name.append(data.name.P_name)
            saled.append(data.saled)
            date.append(data.c_time.strftime("%H:%M:%S"))

    # --- データ送信 ---
    menu_items = [
        {'name': 'Submit', 'url': reverse('AppPOS:POS_page')},
        {'name': 'Results', 'url': reverse('AppPOS:results')},
        {'name': 'Order', 'url': reverse('AppPOS:order')},
        {'name': 'Admin', 'url': reverse('admin:index')},
    ]
    stats={
        'menu_items': menu_items,
        'ord_id':json.dumps(ord_id),
        'name': json.dumps(name), 
        'saled': json.dumps(saled),
        'date': json.dumps(date),

    }
    return render(request, 'order.html', stats)










