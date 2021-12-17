from django.db import models
from user.models import User

# Create your models here.
class Note(models.Model):
    title = models.CharField('标题',max_length=100,default='默认值')
    content = models.TextField('内容',null=True)
    create_time = models.DateTimeField('创建时间',auto_now_add=True)
    update_time = models.DateTimeField('更新时间',auto_now=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    note_file = models.FileField('文件',upload_to='note_file',null=True)
    class Meta:
        db_table = 'note'
        verbose_name_plural = '笔记内容'