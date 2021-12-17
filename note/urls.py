from django.urls import path
from note import views


urlpatterns = [
    path('list_note',views.list_note,name="list_note"),
    path('update',views.update,name="update"),
    path('delete',views.delete_note,name="delete"),
    path('detail',views.detail,name="detail"),
    path('export',views.export_data,name="ex")
]