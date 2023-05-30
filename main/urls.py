from django.urls import path
from .import views
app_name="main"
urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.login_user,name="login"),
    path('note/<int:pk>/',views.note_detail,name="note"),
    path('signup/',views.signup_user,name="signup"),
    path('logout/',views.logout_user,name="logout"),
    path('post/',views.create_post,name="post"),
    path('reset_password/',views.password_change,name="passwdchange"),
    path('search/',views.search_view,name="search"),
    path('delete/<int:pk>/',views.delete_note,name="delete"),
    path('edit/<int:pk>/',views.edit_note,name="edit"),

]
