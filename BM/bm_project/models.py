from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

from djongo import models

class Myuser(AbstractUser):
    pass

    class Meta:
        db_table="myuser"

    def __str__(self):
        return self.username

class MaterialManager(models.Manager):

    def get_queryset(self):

        return super(MaterialManager,self).get_queryset().filter()

class Material(models.Model):
    matobj=MaterialManager()
    materialid=models.CharField(max_length=30,verbose_name="mpid")
    prettyformula=models.CharField(max_length=30,verbose_name="化学式")
    elements=models.CharField(max_length=30,verbose_name="元素")
    structure=models.CharField(max_length=500,verbose_name="结构")
    information=models.CharField(max_length=500,verbose_name="信息")

    class Meta:
        db_table="material"

    def __str__(self):
        return self.materialid


