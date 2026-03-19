from django.test import TestCase, Client
from django.urls import reverse
from core.models import User, ShoppingList, ListItem

class ShoppingListModelTest(TestCase):
    def setUp(self):
        # Prepara dados para os testes desta classe
        self.user = User.objects.create_user(email="test@test.com", password="password123")
        self.lista = ShoppingList.objects.create(owner=self.user, title="Festa do Fim de Semana")
        
        ListItem.objects.create(shopping_list=self.lista, name="Bolo", quantity="1", is_checked=False)
        ListItem.objects.create(shopping_list=self.lista, name="Refrigerante", quantity="2", is_checked=True)

    def test_get_formatted_text_for_sharing(self):
        """Garante que a função de texto para compartilhamento monta a string corretamente."""
        texto = self.lista.get_formatted_text_for_sharing()
        
        self.assertIn("🛒 *Festa do Fim de Semana*", texto)
        self.assertIn("[ ] 1 - Bolo", texto)
        self.assertIn("[x] 2 - Refrigerante", texto)
        self.assertIn("Compartilhado pelo nosso App", texto)


class ListAccessIntegrationTest(TestCase):
    def setUp(self):
        # Cria três usuários diferentes
        self.dono = User.objects.create_user(email="dono@test.com", password="password")
        self.convidado = User.objects.create_user(email="convidado@test.com", password="password")
        self.intruso = User.objects.create_user(email="intruso@test.com", password="password")

        # Dono cria uma lista e compartilha APENAS com o convidado
        self.lista = ShoppingList.objects.create(owner=self.dono, title="Compras da Casa")
        self.lista.shared_with.add(self.convidado)

        # Inicia o cliente de testes (simula um navegador)
        self.client = Client()

    def test_dono_pode_acessar_lista(self):
        """O proprietário da lista deve conseguir ver os detalhes da lista (Status 200)."""
        self.client.force_login(self.dono)
        response = self.client.get(reverse('list_detail', args=[self.lista.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/list_detail.html')

    def test_convidado_pode_acessar_lista(self):
        """Um usuário que recebeu o compartilhamento deve conseguir acessar (Status 200)."""
        self.client.force_login(self.convidado)
        response = self.client.get(reverse('list_detail', args=[self.lista.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/list_detail.html')

    def test_intruso_nao_pode_acessar_lista(self):
        """Um usuário que não tem relação com a lista deve ser barrado."""
        self.client.force_login(self.intruso)
        response = self.client.get(reverse('list_detail', args=[self.lista.id]))
        
        # Como definimos na view, se ele não tem acesso, volta pro dashboard (Status 302)
        self.assertRedirects(response, reverse('dashboard'))
