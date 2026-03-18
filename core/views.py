# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import CustomUserCreationForm, RequestOTPForm, VerifyOTPForm
from .models import ShoppingList, ListItem
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from .models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import random
import redis
from django.core.mail import send_mail
from django.conf import settings
from decouple import config

# Configuração do cliente Redis (reaproveitando o mesmo que o channels usa)
redis_host = config('REDIS_HOST', default='127.0.0.1')
redis_client = redis.StrictRedis(host=redis_host, port=6379, db=0, decode_responses=True)

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Loga o usuário automaticamente após o registro
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def request_login_view(request):
    if request.method == 'POST':
        form = RequestOTPForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Se o usuário não existe, criamos a conta na hora (senha inutilizável por ser passwordless)
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = User.objects.create_user(email=email, password=None)

            # Gerar código de 6 dígitos aleatório
            otp_code = str(random.randint(100000, 999999))
            
            # Salvar no Redis com expiração de 5 minutos (300 segundos)
            redis_client.setex(f"otp_{email}", 300, otp_code)
            
            # Enviar o e-mail (vai aparecer no terminal graças ao Console Backend)
            send_mail(
                subject='Seu código de acesso - My Shared List',
                message=f'Seu código de verificação é: {otp_code}\n\nEle expira em 5 minutos.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            
            # Guardamos o e-mail na "sessão" para a próxima tela saber quem está tentando logar
            request.session['login_email'] = email
            return redirect('verify_login')
    else:
        form = RequestOTPForm()
    return render(request, 'core/request_login.html', {'form': form})

def verify_login_view(request):
    email = request.session.get('login_email')
    if not email:
        return redirect('request_login') # Se tentar acessar direto pela URL, volta pro início

    if request.method == 'POST':
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            otp_digitado = form.cleaned_data['otp']
            
            # Busca o código que guardamos no Redis
            otp_salvo = redis_client.get(f"otp_{email}")

            if otp_salvo and otp_salvo == otp_digitado:
                user = User.objects.get(email=email)
                login(request, user) # Faz o login no Django!
                
                # Limpa o Redis e a Sessão por segurança
                redis_client.delete(f"otp_{email}")
                del request.session['login_email']
                
                return redirect('dashboard')
            else:
                messages.error(request, 'Código inválido ou expirado. Tente novamente.')
    else:
        form = VerifyOTPForm()
        
    return render(request, 'core/verify_login.html', {'form': form, 'email': email})

@login_required
def dashboard_view(request):
    # Busca tanto as listas que o usuário é dono quanto as que foram compartilhadas com ele.
    # O .distinct() garante que não haja listas duplicadas.
    lists = ShoppingList.objects.filter(
        Q(owner=request.user) | Q(shared_with=request.user)
    ).distinct()
    return render(request, 'core/dashboard.html', {'lists': lists})

@login_required
def create_list_view(request):
    if request.method == 'POST':
        title = request.POST.get('title', 'Nova Lista de Compras')
        new_list = ShoppingList.objects.create(owner=request.user, title=title)
        return redirect('list_detail', list_id=new_list.id)
    # Se não for POST, apenas redireciona para o dashboard, já que a criação é simples
    return redirect('dashboard')


@login_required
def list_detail_view(request, list_id):
    # Garante que o usuário tem permissão para ver esta lista
    list_obj = get_object_or_404(ShoppingList, id=list_id)
    
    # Validação de segurança crucial
    if not (list_obj.owner == request.user or request.user in list_obj.shared_with.all()):
        # No futuro, podemos redirecionar para uma página de "acesso negado"
        return redirect('dashboard')

    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        item_quantity = request.POST.get('item_quantity', '1')
        if item_name:
            new_item = ListItem.objects.create(
                shopping_list=list_obj, 
                name=item_name, 
                quantity=item_quantity
            )
            
            # <<< INÍCIO DA MODIFICAÇÃO CHANNELS >>>
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'list_{list_id}',
                {
                    'type': 'item_added', # Nome do método no consumer
                    'message': {
                        'id': new_item.id,
                        'name': new_item.name,
                        'quantity': new_item.quantity,
                        'is_checked': new_item.is_checked,
                    }
                }
            )
        return redirect('list_detail', list_id=list_id)

    items = list_obj.items.all()
    return render(request, 'core/list_detail.html', {'list_obj': list_obj, 'items': items})

@api_view(['POST'])
@login_required
def toggle_item_status(request, item_id):
    item = get_object_or_404(ListItem, id=item_id)
    
    # Verificação de segurança: O usuário tem permissão para modificar este item?
    list_obj = item.shopping_list
    if not (list_obj.owner == request.user or request.user in list_obj.shared_with.all()):
        return Response({'status': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)

    # Inverte o status e salva no banco
    item.is_checked = not item.is_checked
    item.save()
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'list_{item.shopping_list.id}',
        {
            'type': 'item_toggled', # Nome do método no consumer
            'message': {
                'id': item.id,
                'is_checked': item.is_checked,
            }
        }
    )
    
    return Response({'status': 'ok', 'is_checked': item.is_checked})


@login_required
def share_list_view(request, list_id):
    list_obj = get_object_or_404(ShoppingList, id=list_id, owner=request.user)

    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user_to_share_with = User.objects.get(email=email)
            # Adiciona o usuário à lista de compartilhamento
            list_obj.shared_with.add(user_to_share_with)
            messages.success(request, f'Lista compartilhada com {email}!')
        except User.DoesNotExist:
            messages.error(request, f'Usuário com email {email} não encontrado.')
    
    return redirect('list_detail', list_id=list_id)