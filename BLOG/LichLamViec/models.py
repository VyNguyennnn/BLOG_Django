from django.db import models
from django import forms


# # Create your models here.
class TK_tmp:
    def __init__(self):
        self.tk = ''
        self.mk = ''
        self.getTK()

    def getTK(self):
        return self.tk

    def setTK(self, tk):
        self.tk = tk

    def setMK(self, mk):
        self.mk = mk


class TaiKhoan(models.Model):
    usr = models.CharField(max_length=80)
    pwd = models.CharField(max_length=80)
    mail = models.CharField(max_length=80)

class Tuan(models.Model):
    NgayBD = models.DateField()
    NgayKT = models.DateField()
    sd = models.IntegerField()

class Thu2(models.Model):
    ThoiGianBD = models.TimeField()
    ThoiGianKT = models.TimeField()
    TieuDe = models.CharField(max_length=50)
    NoiDung = models.CharField(max_length=80)
    id_tuan = models.ForeignKey(Tuan, on_delete=models.CASCADE)

class Thu3(models.Model):
    ThoiGianBD = models.TimeField()
    ThoiGianKT = models.TimeField()
    TieuDe = models.CharField(max_length=50)
    NoiDung = models.CharField(max_length=80)
    id_tuan = models.ForeignKey(Tuan, on_delete=models.CASCADE)

class Thu4(models.Model):
    ThoiGianBD = models.TimeField()
    ThoiGianKT = models.TimeField()
    TieuDe = models.CharField(max_length=50)
    NoiDung = models.CharField(max_length=80)
    id_tuan = models.ForeignKey(Tuan, on_delete=models.CASCADE)

class Thu5(models.Model):
    ThoiGianBD = models.TimeField()
    ThoiGianKT = models.TimeField()
    TieuDe = models.CharField(max_length=50)
    NoiDung = models.CharField(max_length=80)
    id_tuan = models.ForeignKey(Tuan, on_delete=models.CASCADE)

class Thu6(models.Model):
    ThoiGianBD = models.TimeField()
    ThoiGianKT = models.TimeField()
    TieuDe = models.CharField(max_length=50)
    NoiDung = models.CharField(max_length=80)
    id_tuan = models.ForeignKey(Tuan, on_delete=models.CASCADE)

class Thu7(models.Model):
    ThoiGianBD = models.TimeField()
    ThoiGianKT = models.TimeField()
    TieuDe = models.CharField(max_length=50)
    NoiDung = models.CharField(max_length=80)
    id_tuan = models.ForeignKey(Tuan, on_delete=models.CASCADE)

class ChuNhat(models.Model):
    ThoiGianBD = models.TimeField()
    ThoiGianKT = models.TimeField()
    TieuDe = models.CharField(max_length=50)
    NoiDung = models.CharField(max_length=80)
    id_tuan = models.ForeignKey(Tuan, on_delete=models.CASCADE)

class MatKhauXemLich(models.Model):
    MatKhau = models.CharField(max_length=20)
    sd = models.BooleanField()