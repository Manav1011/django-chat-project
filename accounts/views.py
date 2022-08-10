import email
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import HttpResponse
from allauth.account.views import PasswordChangeView
from django.contrib.auth.models import User
from django.views.generic import ListView
# Create your views here.

class SearchView(ListView):    
    template_name='snippets/search_view.html'
    context_object_name='qs'    
    def get_queryset(self):
        user_object=User.objects.all()
        query=self.request.GET.get('q',None)
        if query is not None:
            queryset=User.objects.filter(username__icontains=query).exclude(username=self.request.user.username)
            print(queryset)
            return queryset        
        else:
            queryset=None
            return queryset
            
    