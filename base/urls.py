from django.urls import path
from . import views

urlpatterns=[
    path('login/',views.loginpage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.registerUser,name="register"),
    path('',views.home,name="home"),
    path('user_profile/<str:pk>/',views.user_profile,name="userProfile"),
    path('cuck/<str:pk>/',views.room,name="room"),
    path('cuck/<str:pk>/fuck/',views.room2,name="rooom2"),
    path('create_room/',views.createRoom,name="createRoom"),
    path('update_room/<str:pk>/',views.updateRoom,name="updateRoom"),
    path('delete_room/<str:pk>/',views.deleteRoom,name="deleteRoom"),
     path('delete_message/<str:pk>/',views.deleteMessage,name="deleteMsg"),
    path('edit_user/',views.edit_user,name='editUser'),
    path('topicpage/',views.topicpage,name='topicPage'),
]