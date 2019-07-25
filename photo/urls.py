from django.urls import path, include
from .views import PhotoCreate, PhotoDelete, PhotoDetail, PhotoList, PhotoUpdate,\
PhotoLike, PhotoFavorite, PhotoFavoriteList, PhotoLikeList

app_name = 'photo'

urlpatterns = [
    path('', PhotoList.as_view(), name='index'),
    path('create/', PhotoCreate.as_view(), name='create'),
    path('detail/<int:pk>', PhotoDetail.as_view(), name='detail'),
    path('update/<int:pk>', PhotoUpdate.as_view(), name='update'),
    path('delete/<int:pk>', PhotoDelete.as_view(), name='delete'),
    path('like/<int:photo_id>/',PhotoLike.as_view(), name='like'),
    path('favorite/<int:photo_id>/', PhotoFavorite.as_view(), name='favorite'),
    path('like/',PhotoLikeList.as_view(), name='like_list'),
    path('favorite/', PhotoFavoriteList.as_view(), name='favorite_list')

]