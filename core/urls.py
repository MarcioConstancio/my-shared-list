from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Autenticação
    # Novo fluxo de Login/Cadastro Passwordless
    path('login/', views.request_login_view, name='login'),
    path('login/verify/', views.verify_login_view, name='verify_login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Aplicação
    path('', views.dashboard_view, name='dashboard'),
    path('list/create/', views.create_list_view, name='create_list'),
    path('list/<int:list_id>/', views.list_detail_view, name='list_detail'),
    path('api/item/<int:item_id>/toggle/', views.toggle_item_status, name='toggle_item'),
    path('list/<int:list_id>/share/', views.share_list_view, name='share_list'),
]