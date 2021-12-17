from django.contrib import admin
from .models import Note

# Register your models here.
class NoteManager(admin.ModelAdmin):
    list_display = ['title','create_time','update_time','user_id']
admin.site.register(Note,NoteManager)
