from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'

# models.py 와 views.py를 거치지 않고 바로 템플릿만으로 구현 가능.
# settings.py에 로그인 성공했을 때 연결될 url연결해줌.
urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout')
]