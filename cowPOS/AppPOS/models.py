from django.db import models
from django.utils import timezone

# Create your models here.


class Prodact_Name(models.Model):
    class Meta:
        db_table = '商品に関するデータ一覧'  # DB内で使用するテーブル名
        verbose_name_plural = '商品に関するデータ一覧'  # Admionサイトで表示するテーブル名
    P_name = models.CharField('商品名', max_length=255,
                              null=True, blank=True)  # 品名
    P_price = models.IntegerField('商品の値段', null=True, blank=True)  # デフォの値段

    def __str__(self):
        return self.P_name


class Accounting_Data(models.Model):
    class Meta:
        db_table = '会計データの一覧'  # DB内で使用するテーブル名
        verbose_name_plural = '会計データ一覧'  # Admionサイトで表示するテーブル名
    name = models.ForeignKey(Prodact_Name, on_delete=models.SET_NULL,
                             null=True, related_name='related_prodact_name')
    price = models.IntegerField(
        '売れた個数', default=0, null=True, blank=True)  # 売れた個数
    saled = models.IntegerField(
        '売れた値段', default=0, null=True, blank=True)  # 売れた定価
    c_time = models.DateTimeField('登録時間', default=timezone.now)  # 登録した時間と日時

    def __str__(self):
        return self.c_time.strftime('%Y-%m-%d %H:%M:%S')
