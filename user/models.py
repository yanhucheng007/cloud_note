from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30,unique=True,verbose_name='用户名')
    password = models.CharField(max_length=32,verbose_name='密码')
    created_time = models.DateTimeField('创建时间',auto_now_add=True)
    update_time = models.DateTimeField('更新时间',auto_now=True)
    class Meta:
        db_table = 'user'
        verbose_name_plural = '用户-客户端'
    def __str__(self):
        return '用户' + self.username