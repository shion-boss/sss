from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path("index/",views.index,name="index"),
    path('logout/',views.logout_view,name='logout'),
    path('select/',views.login_select_view,name='loginselect'),
    path('afirieito/<str:introducer>/',views.userregi_view,name='userregi'),
    path('parts/<str:search_kind>/',views.parts_search_view,name='partkind'),
    path('parts/<str:username>/<int:id>/',views.parts_part_view,name='part'),
    path('parts/list/<str:username>/<int:categories_id>/',views.parts_list_view,name='partslist'),
    path('account/<str:username>/<str:kind>/',views.accountkind_view,name='accountkind'),
    path('account/metapost/',views.metapost_view,name='metapost'),
    path('community/',views.community_view,name='community'),
    path('community/<int:id>/',views.community2_view,name='community_event'),
    path('album/<int:id>/',views.album_view,name='album'),
    path('ranking/',views.ranking_view,name='ranking'),
    path('tech/<str:category>/<int:w>/<int:num>/',views.tech_view,name='tech'),
    path('tech/<str:category>/series/<int:num>/',views.tech_series_view,name='techseries'),
    path('footer/<str:category>/',views.footer_view,name='footer'),
    path('touko/',views.touko_view,name='touko'),
    path('edit/<str:username>/<int:id>/',views.toukoedit_view,name='toukoedit'),
    path('edit/series/<str:username>/<int:id>/',views.editcate_view,name='edit_cate'),
    path('editsave/<str:username>/<int:id>/',views.editsave_view,name='editsave'),
    path('delete/',views.delete_cate_view,name='delete_cate'),
    path('deletepart/<str:username>/<int:id>/',views.delete_part_view,name='delete_part'),
    path('',views.technext_view,name='technext'),
    path('story/',views.tb_view,name='tb'),
    path("ajax/", views.like_ajax_response,name='ajax'),
    path("ajaxf/",views.favorite_ajax_view,name='ajaxf'),
    path("ajaxc/",views.channel_ajax_view,name='ajaxc'),
    path('404/',views.error404_view,name='error404'),
    path('500/',views.my_error_handler,name='error500'),
]

###############################################
#API
from rest_framework import routers
from .views import LikeViewSet, FavoriteViewSet,ChannelViewSet


router = routers.DefaultRouter()
router.register('like', LikeViewSet)
router.register('favorite', FavoriteViewSet)
router.register('channel', ChannelViewSet)

###############################################
