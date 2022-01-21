from django.conf.urls import url
from .views import  PostDelete, PostDetail, PostUpdate, ListAndCreate, load_post, DeleteUpdatePost, PostDeleteAjax



urlpatterns = [   
			   url(r'^post_createList', ListAndCreate.as_view(), name='post_createList'),   
               url(r'^post_detail/(?P<pk>\d+)/$', PostDetail.as_view(), name='post_detail'),
               url(r'^post_update/(?P<pk>\d+)/$', PostUpdate.as_view(), name='post_update'),
               url(r'^post_delete/(?P<pk>\d+)/$', PostDelete.as_view(), name='post_delete'),
               url(r'^ajax/load_post', load_post, name='ajax_load_post'),
               url(r'^DeleteUpdate/Post/(?P<pk>[0-9]+)/$', DeleteUpdatePost.as_view(), name='DeleteUpdatePost'),
               url(r'^ajax/delete_post', PostDeleteAjax, name='PostDeleteAjax'),
              ]  