# 個々のページのviews

from django.shortcuts import render  
from datetime import datetime, timedelta
from django.views import View 
from django.db.models import Max, Min 
from . import models
from django.utils import timezone
from django.utils.timezone import localtime

# http://127.0.0.1:8000/AppPOS/pos_page/
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
            submited.price = request.POST.get('price' + data.P_name)
            submited.saled = request.POST.get('saled' + data.P_name)
            submited.save()

    stats = {
        'Prodacts_dict' : Prodacts_dict,
    }
    return render(request, 'POS_page.html', stats)


# http://127.0.0.1:8000/AppPOS/results/
def results_page(request):
    # 初期化等
    today_date = timezone.now()
    Accounting_Info = models.Accounting_Data.objects.filter(c_time__date=today_date)
    max_date = models.Accounting_Data.objects.filter(c_time__date=today_date).aggregate(Max('c_time'))['c_time__max']
    min_date = models.Accounting_Data.objects.filter(c_time__date=today_date).aggregate(Min('c_time'))['c_time__min']
    Accounting_dict = {}
    print(max_date)
    print(min_date)
    # 1時間ごとのリストを作成
    date_list = []
    current_date = min_date   # 最小日付から開始
    max_date += timedelta(hours=1)
    total = 0
    totals = []
    while current_date <= max_date:
        date_list.append(current_date.strftime("%H:00"))
        current_date += timedelta(hours=1)
        print(date_list)
    for date in date_list:
        for data in Accounting_Info:
            if data.c_time.strftime("%H:00") < date:
                totals.append(total)
                break
            total += data.price * data.saled
    print(totals)

    stats = {'name':1}
    return render(request, 'results.html', stats)