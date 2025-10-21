from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Autenticação
    path('register/', views.register_view, name='register'),
    # Usando a LoginView pronta do Django, mas apontando para nosso template
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Aplicação
    path('', views.dashboard_view, name='dashboard'),
    path('list/create/', views.create_list_view, name='create_list'),
    path('list/<int:list_id>/', views.list_detail_view, name='list_detail'),
    path('api/item/<int:item_id>/toggle/', views.toggle_item_status, name='toggle_item'),
    path('list/<int:list_id>/share/', views.share_list_view, name='share_list'),
]