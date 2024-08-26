from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register('board', views.BoardCreateView) 
router.register('list', views.ListCreateView,basename='list') 
router.register('card', views.CardCreateView) 
router.register('allMember', views.MemberListView) 

urlpatterns = [
    path('', include(router.urls)),
    path('card/<int:pk>/', views.CardDetail.as_view(), name='card-detail'),
    path('board/<int:board_id>/list/<int:list_id>/', views.ListUpdateDeleteView.as_view(), name='list-update-delete'),
     path('board/member/<int:pk>/', views.MemberDetailView.as_view(), name='member-detail'),
     path('board/<int:pk>/addmember/', views.AddBoardMemberView.as_view(), name='member'),
     path('list/<int:list_id>/card/', views.CardCreateView.as_view({'post': 'create'}), name='create-card'),
    
    # path('board/<int:board_id>/lists/create/', views.ListByBoardView.as_view(), name='list-create')
    # path('board/<int:board_id>/addMember/', views.AddMemberToBoardView.as_view(), name='add-member'),
]