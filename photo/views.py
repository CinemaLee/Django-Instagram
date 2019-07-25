from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.base import View
from .models import Photo
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseRedirect
from urllib.parse import urlparse
# Create your views here.
# 클래스형 뷰로 구현

class PhotoList(ListView):
    model = Photo
    template_name_suffix = '_list'


class PhotoCreate(CreateView):
    model = Photo
    fields=['text','image']
    template_name_suffix = '_create'
    success_url = '/instagram'

    # 사진을 업로드하기 위해서는 이렇게 폼의 유효성을 판단한 후 저장.
    def form_valid(self, form): 
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('/instagram')
        else:
            return render(request, 'photo/photo_create.html', {'form':form})


class PhotoDetail(DetailView):
    model = Photo
    template_name_suffix = '_detail'


# 사진을 업로드하기 위해서는 이렇게 폼의 유효성을 판단한 후 저장.
class PhotoUpdate(UpdateView):
    model = Photo
    fields=['text', 'image']
    template_name_suffix = '_update'
    success_url = '/instagram'
    
    def form_valid(self, form): 
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('/instagram')
        else:
            return render(request, 'photo/photo_create.html', {'form':form})

    
    # 여러 개의 인자를 받기 위해서 *args의 형태로 파라미터를 작성함. 튜플로 받은 것처럼 인식.(이름은 *a, *aaaaa 등등 상관없음)
    # **kwargs는 (키워드 = 특정 값) 형태로 함수를 호출 할 수 있다. 딕셔너리 형태로 함수 내부로 전달.

    # 주소로 직접입력하여 들어오는 경우에 권한을 주기 위한 방법. get방식 post방식 2가지 모두 커버. 
    def dispatch(self, request, *args, **kwargs):

        # 사용자가 접속했을 때 get이냐 post냐를 결정하고 분기를 자동으로 해준다.
        object = self.get_object()

        # 작성자와 요청자가 서로 다르다면
        if object.author != request.user:
            messages.warning(request, '수정할 권한이 없습니다.')
            return redirect('photo:index')
        # 같다면 super을 써줘서 원래 PhotoUpdate가 실행되도록 함
        else:
            return super(PhotoUpdate, self).dispatch(request, *args, **kwargs)
    


class PhotoDelete(DeleteView):
    model = Photo
    template_name_suffix = '_delete'
    success_url = '/instagram'

    # 주소로 직접입력하여 들어오는 경우에 권한을 주기 위한 방법. get방식 post방식 2가지 모두 커버. 
    def dispatch(self, request, *args, **kwargs):

        # 사용자가 접속했을 때 get이냐 post냐를 결정하고 분기를 자동으로 해준다.
        object = self.get_object()

        # 작성자와 요청자가 서로 다르다면
        if object.author != request.user:
            messages.warning(request, '삭제할 권한이 없습니다.')
            return redirect('photo:index')
        # 같다면 super을 써줘서 원래 PhotoUpdate가 실행되도록 함
        else:
            return super(PhotoDelete, self).dispatch(request, *args, **kwargs)



class PhotoLike(View):
    # get방식으로 들어온 경우
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated: # 로그인되지 않았다면
            return redirect('accounts:login')
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.like.all(): # 하트가 눌린상태면
                    photo.like.remove(user) # 디비에서 삭제
                else:# 아니면
                    photo.like.add(user) # 디비에 추가
            
            # 하트를 눌르는 행위는 결국 url을 바꾸지않겠다는 의미. 현재의 url을 유지해주는.
            referer_url = request.META.get('HTTP_REFERER') # 기존 url분석
            path = urlparse(referer_url).path # path를 가져와서
            return HttpResponseRedirect(path)



class PhotoFavorite(View):
    # get방식으로 들어온 경우
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated: # 로그인되지 않았다면
            return redirect('accounts:login')
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.favorite.all(): # 저장하기가 눌린상태면
                    photo.favorite.remove(user) # 디비에서 삭제
                else:# 아니면
                    photo.favorite.add(user) # 디비에 저장
            
            # 하트를 눌르는 행위는 결국 url을 바꾸지않겠다는 의미. 현재의 url을 유지해주는.
            referer_url = request.META.get('HTTP_REFERER') # 기존 url분석
            path = urlparse(referer_url).path # path를 가져와서
            return HttpResponseRedirect(path)






class PhotoFavoriteList(ListView):
    model = Photo
    template_name = 'photo/photo_list.html' # 템플릿을 직접 지정

    # 주소로 직접입력하여 들어오는 경우에 권한을 주기 위한 방법. get방식 post방식 2가지 모두 커버. 
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated: # 로그인 확인
            return redirect('accounts:login')
        return super(PhotoFavoriteList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self): # 쿼리를 날려준다. 그 쿼리는 object_list에 담긴다.
        # 쿼리셋을 정의하고 요청한 유저의 좋아요한 포스터를 전부 리턴하도록 설계
        # 내가 좋아요한 글 보여주기
        user = self.request.user
        queryset = user.favorite_post.all() # 모델설계할 때 related_name

        return queryset


class PhotoLikeList(ListView):
    model = Photo
    template_name = 'photo/photo_list.html' # 템플릿을 직접 지정

    # 주소로 직접입력하여 들어오는 경우에 권한을 주기 위한 방법. get방식 post방식 2가지 모두 커버.
    # 눈에 보이는 부분은 html에서 해결.
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated: # 로그인 확인
            return redirect('accounts:login')
        return super(PhotoLikeList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self): # 쿼리를 날려준다. 그 쿼리는 object_list에 담긴다.
        # 쿼리셋을 정의하고 요청한 유저의 좋아요한 포스터를 전부 리턴하도록 설계
        # 내가 좋아요한 글 보여주기
        user = self.request.user
        queryset = user.like_post.all() # 모델설계할 때 related_name
        return queryset


