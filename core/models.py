from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Gerenciador de modelo de usuário customizado onde o email é o identificador único
    para autenticação em vez de nomes de usuário.
    """
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('O Email deve ser definido'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    # Torne o username opcional e não-único
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    
    # Faça do email o campo único e obrigatório
    email = models.EmailField(_('endereço de email'), unique=True)
    
    telefone = models.CharField(max_length=15, blank=True, null=True)

    # Diga ao Django para usar o email como campo de login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Remova 'email' dos campos obrigatórios no prompt (já que é o username)

    # Associe o novo gerenciador
    objects = CustomUserManager()

    def __str__(self):
        return self.email

class ShoppingList(models.Model):
    owner = models.ForeignKey(User, related_name='owned_lists', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='Nova Lista de Compras')
    shared_with = models.ManyToManyField(User, related_name='shared_lists', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_formatted_text_for_sharing(self):
        """
        Gera uma string formatada da lista de compras para compartilhamento.
        """
        header = f"🛒 *{self.title}*\n\n"
        items_text_list = []
        for item in self.items.all():
            # Usamos [ ] para simular um checkbox
            status = "[x]" if item.is_checked else "[ ]"
            items_text_list.append(f"{status} {item.quantity} - {item.name}")
        
        body = "\n".join(items_text_list)
        footer = "\n\n_Compartilhado pelo nosso App de Lista de Compras!_"
        
        return header + body + footer

    def __str__(self):
        return self.title

class ListItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    quantity = models.CharField(max_length=50, default='1')
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return self.name