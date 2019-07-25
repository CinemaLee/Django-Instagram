from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Photo(models.Model):
    # related_name이 없다면 장고는 photo_set 이라는 모델 이름을 만듬. (User에서 photo로의 역관계 이름)
    # user1이라는 객체가 있다면 user1.photo_set.all() 이런식. 하지만 related_name이 있다면
    # user1.user.all() -> user1과 관련이 있는 related_name이 user인 모델의 모든 인스턴스를 가져오라.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', verbose_name='작성자')
    text = models.TextField(blank=True, verbose_name='내용')
    image = models.ImageField(upload_to='timeline_photo/%Y/%m/%d') # settings.py에 추가.
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='작성된 시간')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='수정된 시간')

    like = models.ManyToManyField(User, related_name='like_post', blank=True)
    favorite = models.ManyToManyField(User,related_name='favorite_post', blank=True)

    def __str__(self):
        return "text : "+self.text

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = '게시물들'