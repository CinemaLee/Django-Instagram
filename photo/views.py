from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from .models import Photo

# Create your views here.
# 클래스형 뷰로 구현

class PhotoList(ListView):
    model = Photo
    template_name_suffix = '_list'


class PhotoCreate(CreateView):
    model = Photo
    fields=['text','image']
    template_name_suffix = '_create'
    success_url = 'instagram/'


class PhotoDetail(DetailView):
    model = Photo
    template_name_suffix = '_detail'


class PhotoUpdate(UpdateView):
    model = Photo
    fields=['text', 'image']
    template_name_suffix = '_update'
    success_url = 'instagram/'


class PhotoDelete(DeleteView):
    model = Photo
    template_name_suffix = '_delete'
    success_url = 'instagram/'