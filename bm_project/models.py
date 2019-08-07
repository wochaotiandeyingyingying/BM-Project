from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from djongo import models

class Myuser(AbstractUser):


    class Meta:
        db_table="user"

    def __str__(self):
        return self.username

class MaterialManager(models.Manager):

    def get_queryset(self):

        return super(MaterialManager,self).get_queryset().filter()

class Material(models.Model):
    matobj = MaterialManager()
    slid = models.CharField(max_length=30, verbose_name="slid")
    materialid = models.CharField(max_length=30, verbose_name="mpid")
    prettyformula = models.CharField(max_length=30, verbose_name="化学式")
    elements = models.CharField(max_length=30, verbose_name="元素")
    structure = models.CharField(max_length=500, verbose_name="结构")
    # information = models.CharField(max_length=500, verbose_name="信息")
    energy = models.CharField(max_length=100, verbose_name="能量")
    energyperatom = models.CharField(max_length=100)
    volum = models.CharField(max_length=100)
    formationenergyperatom = models.CharField(max_length=100)
    nsites = models.CharField(max_length=100)
    ishubbard = models.BooleanField()
    nelements = models.CharField(max_length=100)
    eabovehull = models.CharField(max_length=100)
    iscompatible = models.BooleanField()
    bandgap = models.CharField(max_length=100)
    density = models.CharField(max_length=100)
    totalmagnetization = models.CharField(max_length=100)
    oxidetype = models.CharField(max_length=100)
    makerone = models.CharField(max_length=100)
    makertwo = models.CharField(max_length=100)

    class Meta:
        db_table="material"

    def __str__(self):
        return self.materialid