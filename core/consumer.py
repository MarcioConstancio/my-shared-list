# core/consumers.py

import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import ListItem

class ShoppingListConsumer(WebsocketConsumer):
    def connect(self):
        # Pega o ID da lista da URL
        self.list_id = self.scope['url_route']['kwargs']['list_id']
        self.list_group_name = f'list_{self.list_id}'

        # Entra no "grupo" do canal da lista
        async_to_sync(self.channel_layer.group_add)(
            self.list_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Sai do grupo do canal
        async_to_sync(self.channel_layer.group_discard)(
            self.list_group_name,
            self.channel_name
        )

    # Estes são os métodos que serão chamados quando uma mensagem
    # for enviada do backend para o grupo.
    # O nome do método corresponde ao valor da chave 'type' na mensagem.

    def item_added(self, event):
        item = event['message']
        # Envia a mensagem para o WebSocket (cliente)
        self.send(text_data=json.dumps({
            'event_type': 'item_added',
            'item': item,
        }))

    def item_toggled(self, event):
        item = event['message']
        # Envia a mensagem para o WebSocket (cliente)
        self.send(text_data=json.dumps({
            'event_type': 'item_toggled',
            'item': item,
        }))