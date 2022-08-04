from django.urls import path,re_path
from .views import SearchView

app_name='accounts'

urlpatterns=[
    path('search/',SearchView.as_view(),name='search')
]