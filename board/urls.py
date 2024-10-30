from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register('board', views.BoardCreateView,basename='board') 
router.register('boards', views.BoarddViewSet,basename='boards') 
router.register('list', views.ListCreateView,basename='list') 
router.register('card', views.CardCreateView,basename='card') 
router.register('cards', views.CardView,basename='cardd') 
router.register('allMember', views.MemberListView) 

urlpatterns = [
    path('', include(router.urls)),
    path('card/card/<int:pk>/', views.CardDetail.as_view(), name='card-detail'),
    path('board/<int:board_id>/list/<int:list_id>/', views.ListUpdateDeleteView.as_view(), name='list-update-delete'),
    path('board/member/<int:pk>/', views.MemberDetailView.as_view(), name='member-detail'),
    path('board/<int:pk>/addmember/', views.AddBoardMemberView.as_view(), name='member'),
    path('list/<int:list_id>/card/', views.CardCreateView.as_view({'post': 'create'}), name='create-card'),
    path('board/<int:board_id>/cardCounts/', views.CardCountView.as_view(), name='card-counts'),
    path('boardCount/', views.BoardCountView.as_view(), name='boardCount'),
]
