#alert request send

# from channels.db import database_sync_to_async
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from django.contrib.auth.models import User
# from .models import Connection  # Adjust according to where your Connection model is located

# # Using sync_to_async to wrap database operations
# @database_sync_to_async
# def create_connection(sender, receiver):
#     return Connection.objects.create(sender=sender, receiver=receiver, status='Pending')

# @database_sync_to_async
# def get_user_by_id(user_id):
#     return User.objects.get(id=user_id)




# class ConnectionConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Get user ID from URL
#         self.user = self.scope['url_route']['kwargs']['user_id']

#         self.room_group_name = f'user_{self.user}'  # Unique group for each user
#         print(self.room_group_name)

#         # Join WebSocket group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave WebSocket group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Handle message from WebSocket (connection request)
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message_type = text_data_json.get('type')

#         if message_type == 'send_connection_request':
#             receiver_user_id = text_data_json['receiver_user_id']
#             sender_username = text_data_json['sender_username']

#             # Fetch receiver user asynchronously
#             receiver = await get_user_by_id(receiver_user_id)
#             sender_user = await get_user_by_id(self.user)  # Get sender user instance

#             # Debugging log
#             print(f"Fetched Receiver: {receiver.username}, Sender: {sender_user.username}")

#             # Create connection request in the database (using sync_to_async)
#             await create_connection(sender_user, receiver)

#             # Send connection request notification to receiver's WebSocket group
#             receiver_group_name = f'user_{receiver.id}'

#             # Debugging log to confirm group targeting
#             print(f"Sending connection request to group: {receiver_group_name}")

#             await self.channel_layer.group_send(
#                 receiver_group_name,  # Send to the receiver's WebSocket group
#                 {
#                     'type': 'connection_request',
#                     'sender_username': sender_user.username  # Use the sender's actual username
#                 }
#             )

#     # Handle connection request notification
#     async def connection_request(self, event):
#         sender_username = event['sender_username']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'type': 'connection_request',
#             'sender_username': sender_username
#         }))

        





#connection request send

# from channels.db import database_sync_to_async
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from django.contrib.auth.models import User
# from .models import Connection  # Adjust the import according to your project structure

# # Asynchronous utility to fetch pending request count
# @database_sync_to_async
# def get_pending_request_count(user_id):
#     return Connection.objects.filter(receiver_id=user_id, status="Pending").count()

# @database_sync_to_async
# def create_connection(sender, receiver):
#     return Connection.objects.create(sender=sender, receiver=receiver, status="Pending")

# @database_sync_to_async
# def get_user_by_id(user_id):
#     return User.objects.get(id=user_id)


# class ConnectionConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user_id = self.scope['url_route']['kwargs']['user_id']
#         self.room_group_name = f'user_{self.user_id}'

#         # Join the WebSocket group for the logged-in user
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()

#         # Send the current request count to the user upon connection
#         pending_count = await get_pending_request_count(self.user_id)
#         await self.send(text_data=json.dumps({
#             'type': 'update_request_count',
#             'pending_count': pending_count
#         }))

#     async def disconnect(self, close_code):
#         # Leave the WebSocket group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         if data['type'] == 'send_connection_request':
#             receiver_id = data['receiver_user_id']
#             sender_username = data['sender_username']

#             # Fetch receiver and sender users
#             receiver = await get_user_by_id(receiver_id)
#             sender = await get_user_by_id(self.user_id)

#             # Create the connection request
#             await create_connection(sender, receiver)

#             # Update the pending request count for the receiver
#             pending_count = await get_pending_request_count(receiver_id)

#             # Notify the receiver about the new request and update the count
#             await self.channel_layer.group_send(
#                 f'user_{receiver_id}',
#                 {
#                     'type': 'connection_request',
#                     'sender_username': sender_username,
#                     'pending_count': pending_count
#                 }
#             )

#     async def connection_request(self, event):
#         # Send the notification and updated count to the WebSocket
#         await self.send(text_data=json.dumps({
#             'type': 'connection_request',
#             'sender_username': event['sender_username'],
#             'pending_count': event['pending_count']
#         }))






# accept button

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from django.contrib.auth.models import User
# from .models import Connection

# # Database-related functions (wrapped in database_sync_to_async)
# @database_sync_to_async
# def get_user_by_id(user_id):
#     return User.objects.get(id=user_id)

# @database_sync_to_async
# def create_connection(sender, receiver):
#     return Connection.objects.create(sender=sender, receiver=receiver, status='Pending')

# @database_sync_to_async
# def get_sender_and_receiver(connection_id):
#     connection = Connection.objects.get(id=connection_id)
#     return connection.sender, connection.receiver


# class ConnectionConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope['url_route']['kwargs']['user_id']
#         self.room_group_name = f'user_{self.user}'

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message_type = text_data_json.get('type')

#         # Handle sending a connection request
#         if message_type == 'send_connection_request':
#             receiver_user_id = text_data_json['receiver_user_id']
#             sender_username = text_data_json['sender_username']

#             receiver = await get_user_by_id(receiver_user_id)  # Get the receiver from DB
#             sender_user = await get_user_by_id(self.user)  # Get the sender from DB

#             # Create a connection between sender and receiver
#             await create_connection(sender_user, receiver)

#             receiver_group_name = f'user_{receiver.id}'
#             # Notify the receiver about the connection request
#             await self.channel_layer.group_send(
#                 receiver_group_name,
#                 {
#                     'type': 'connection_request',
#                     'sender_username': sender_user.username
#                 }
#             )

#         # Handle accepting a connection request
#         elif message_type == 'accept_connection_request':
#             request_id = text_data_json['request_id']
#             sender, receiver = await get_sender_and_receiver(request_id)  # Get sender and receiver from DB

#             sender_group_name = f'user_{sender.id}'
#             receiver_group_name = f'user_{receiver.id}'

#             # Notify both sender and receiver that the connection request has been accepted
#             await self.channel_layer.group_send(
#                 sender_group_name,
#                 {
#                     'type': 'connection_accepted',
#                     'request_id': request_id,
#                     'status': 'Accepted'
#                 }
#             )
#             await self.channel_layer.group_send(
#                 receiver_group_name,
#                 {
#                     'type': 'connection_accepted',
#                     'request_id': request_id,
#                     'status': 'Accepted'
#                 }
#             )

#     async def connection_request(self, event):
#         sender_username = event['sender_username']
#         await self.send(text_data=json.dumps({
#             'type': 'connection_request',
#             'sender_username': sender_username
#         }))

#     async def connection_accepted(self, event):
#         request_id = event['request_id']
#         status = event['status']

#         await self.send(text_data=json.dumps({
#             'type': 'connection_accepted',
#             'request_id': request_id,
#             'status': status
#         }))



#database save connection accept
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from django.contrib.auth.models import User
# from .models import Connection


# # Database-related functions (wrapped in database_sync_to_async)
# @database_sync_to_async
# def get_user_by_id(user_id):
#     return User.objects.get(id=user_id)


# @database_sync_to_async
# def create_connection(sender, receiver):
#     return Connection.objects.create(sender=sender, receiver=receiver, status='Pending')


# @database_sync_to_async
# def get_sender_and_receiver(connection_id):
#     connection = Connection.objects.get(id=connection_id)
#     return connection.sender, connection.receiver


# @database_sync_to_async
# def update_connection_status(connection_id, status):
#     connection = Connection.objects.get(id=connection_id)
#     connection.status = status
#     connection.save()
#     return connection


# class ConnectionConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope['url_route']['kwargs']['user_id']
#         self.room_group_name = f'user_{self.user}'

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message_type = text_data_json.get('type')

#         # Handle sending a connection request
#         if message_type == 'send_connection_request':
#             receiver_user_id = text_data_json['receiver_user_id']
#             sender_username = text_data_json['sender_username']

#             receiver = await get_user_by_id(receiver_user_id)  # Get the receiver from DB
#             sender_user = await get_user_by_id(self.user)  # Get the sender from DB

#             # Create a connection between sender and receiver
#             connection = await create_connection(sender_user, receiver)

#             receiver_group_name = f'user_{receiver.id}'
#             # Notify the receiver about the connection request
#             await self.channel_layer.group_send(
#                 receiver_group_name,
#                 {
#                     'type': 'connection_request',
#                     'sender_username': sender_user.username
#                 }
#             )

#         # Handle accepting a connection request
#         elif message_type == 'accept_connection_request':
#             request_id = text_data_json['request_id']
#             sender, receiver = await get_sender_and_receiver(request_id)  # Get sender and receiver from DB

#             # Update connection status to "Accepted" in the database
#             updated_connection = await update_connection_status(request_id, 'Accepted')

#             sender_group_name = f'user_{sender.id}'
#             receiver_group_name = f'user_{receiver.id}'

#             # Notify both sender and receiver that the connection request has been accepted
#             await self.channel_layer.group_send(
#                 sender_group_name,
#                 {
#                     'type': 'connection_accepted',
#                     'request_id': request_id,
#                     'status': updated_connection.status
#                 }
#             )
#             await self.channel_layer.group_send(
#                 receiver_group_name,
#                 {
#                     'type': 'connection_accepted',
#                     'request_id': request_id,
#                     'status': updated_connection.status
#                 }
#             )

#     async def connection_request(self, event):
#         sender_username = event['sender_username']
#         await self.send(text_data=json.dumps({
#             'type': 'connection_request',
#             'sender_username': sender_username
#         }))

#     async def connection_accepted(self, event):
#         request_id = event['request_id']
#         status = event['status']

#         await self.send(text_data=json.dumps({
#             'type': 'connection_accepted',
#             'request_id': request_id,
#             'status': status
#         }))







# for connection count , final request accept
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from django.contrib.auth.models import User
# from .models import Connection


# # Database-related functions (wrapped in database_sync_to_async)
# @database_sync_to_async
# def get_user_by_id(user_id):
#     return User.objects.get(id=user_id)


# @database_sync_to_async
# def create_connection(sender, receiver):
#     return Connection.objects.create(sender=sender, receiver=receiver, status='Pending')


# @database_sync_to_async
# def get_sender_and_receiver(connection_id):
#     connection = Connection.objects.get(id=connection_id)
#     return connection.sender, connection.receiver


# @database_sync_to_async
# def update_connection_status(connection_id, status):
#     connection = Connection.objects.get(id=connection_id)
#     connection.status = status
#     connection.save()
#     return connection


# @database_sync_to_async
# def get_pending_request_count(user_id):
#     return Connection.objects.filter(receiver_id=user_id, status='Pending').count()


# class ConnectionConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope['url_route']['kwargs']['user_id']
#         self.room_group_name = f'user_{self.user}'

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()

#         # Send pending request count on connection
#         pending_count = await get_pending_request_count(self.user)
#         await self.send(text_data=json.dumps({
#             'type': 'pending_request_count',
#             'count': pending_count
#         }))

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message_type = text_data_json.get('type')

#         # Handle sending a connection request
#         if message_type == 'send_connection_request':
#             receiver_user_id = text_data_json['receiver_user_id']
#             sender_username = text_data_json['sender_username']

#             receiver = await get_user_by_id(receiver_user_id)  # Get the receiver from DB
#             sender_user = await get_user_by_id(self.user)  # Get the sender from DB

#             # Create a connection between sender and receiver
#             connection = await create_connection(sender_user, receiver)

#             receiver_group_name = f'user_{receiver.id}'

#             # Notify the receiver about the connection request and update the count
#             await self.channel_layer.group_send(
#                 receiver_group_name,
#                 {
#                     'type': 'update_pending_request_count',
#                     'count': await get_pending_request_count(receiver.id)
#                 }
#             )

#         # Handle accepting a connection request
#         elif message_type == 'accept_connection_request':
#             request_id = text_data_json['request_id']
#             sender, receiver = await get_sender_and_receiver(request_id)  # Get sender and receiver from DB

#             # Update connection status to "Accepted" in the database
#             updated_connection = await update_connection_status(request_id, 'Accepted')

#             sender_group_name = f'user_{sender.id}'
#             receiver_group_name = f'user_{receiver.id}'

#             # Notify both sender and receiver that the connection request has been accepted
#             await self.channel_layer.group_send(
#                 sender_group_name,
#                 {
#                     'type': 'connection_accepted',
#                     'request_id': request_id,
#                     'status': updated_connection.status
#                 }
#             )
#             await self.channel_layer.group_send(
#                 receiver_group_name,
#                 {
#                     'type': 'connection_accepted',
#                     'request_id': request_id,
#                     'status': updated_connection.status
#                 }
#             )

#     async def update_pending_request_count(self, event):
#         count = event['count']
#         await self.send(text_data=json.dumps({
#             'type': 'pending_request_count',
#             'count': count
#         }))

#     async def connection_request(self, event):
#         sender_username = event['sender_username']
#         await self.send(text_data=json.dumps({
#             'type': 'connection_request',
#             'sender_username': sender_username
#         }))

#     async def connection_accepted(self, event):
#         request_id = event['request_id']
#         status = event['status']

#         await self.send(text_data=json.dumps({
#             'type': 'connection_accepted',
#             'request_id': request_id,
#             'status': status
#         }))






# for delete button final code

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from django.contrib.auth.models import User
# from .models import Connection


# # Database-related functions (wrapped in database_sync_to_async)
# @database_sync_to_async
# def get_user_by_id(user_id):
#     return User.objects.get(id=user_id)


# @database_sync_to_async
# def create_connection(sender, receiver):
#     return Connection.objects.create(sender=sender, receiver=receiver, status="Pending")


# @database_sync_to_async
# def get_sender_and_receiver(connection_id):
#     connection = Connection.objects.get(id=connection_id)
#     return connection.sender, connection.receiver


# @database_sync_to_async
# def update_connection_status(connection_id, status):
#     connection = Connection.objects.get(id=connection_id)
#     connection.status = status
#     connection.save()
#     return connection


# @database_sync_to_async
# def get_pending_request_count(user_id):
#     return Connection.objects.filter(receiver_id=user_id, status="Pending").count()


# class ConnectionConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope["url_route"]["kwargs"]["user_id"]
#         self.room_group_name = f"user_{self.user}"

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name,
#         )
#         await self.accept()

#         # Send pending request count on connection
#         pending_count = await get_pending_request_count(self.user)
#         await self.send(
#             text_data=json.dumps(
#                 {
#                     "type": "pending_request_count",
#                     "count": pending_count,
#                 }
#             )
#         )

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name,
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message_type = text_data_json.get("type")

#         # Handle sending a connection request
#         if message_type == "send_connection_request":
#             receiver_user_id = text_data_json["receiver_user_id"]
#             sender_username = text_data_json["sender_username"]

#             receiver = await get_user_by_id(receiver_user_id)  # Get the receiver from DB
#             sender_user = await get_user_by_id(self.user)  # Get the sender from DB

#             # Create a connection between sender and receiver
#             connection = await create_connection(sender_user, receiver)

#             receiver_group_name = f"user_{receiver.id}"

#             # Notify the receiver about the connection request and update the count
#             await self.channel_layer.group_send(
#                 receiver_group_name,
#                 {
#                     "type": "update_pending_request_count",
#                     "count": await get_pending_request_count(receiver.id),
#                 },
#             )

#         # Handle accepting a connection request
#         elif message_type == "accept_connection_request":
#             request_id = text_data_json["request_id"]
#             sender, receiver = await get_sender_and_receiver(request_id)  # Get sender and receiver from DB

#             # Update connection status to "Accepted" in the database
#             updated_connection = await update_connection_status(request_id, "Accepted")

#             sender_group_name = f"user_{sender.id}"
#             receiver_group_name = f"user_{receiver.id}"

#             # Notify both sender and receiver that the connection request has been accepted
#             await self.channel_layer.group_send(
#                 sender_group_name,
#                 {
#                     "type": "connection_accepted",
#                     "request_id": request_id,
#                 },
#             )
#             await self.channel_layer.group_send(
#                 receiver_group_name,
#                 {
#                     "type": "connection_accepted",
#                     "request_id": request_id,
#                 },
#             )

       

#         # Handle rejecting a connection request
#         elif message_type == "delete_connection_request":
#             request_id = text_data_json["request_id"]
#             sender, receiver = await get_sender_and_receiver(request_id)
#             rejected_connection = await update_connection_status(request_id, "Rejected")

#             sender_group_name = f"user_{sender.id}"
#             receiver_group_name = f"user_{receiver.id}"

#             await self.channel_layer.group_send(
#                 sender_group_name,
#                 {
#                     "type": "connection_rejected",
#                     "request_id": request_id,
#                 },
#             )
#             await self.channel_layer.group_send(
#                 receiver_group_name,
#                 {
#                     "type": "connection_rejected",
#                     "request_id": request_id,
#                 },
#             )

#     async def update_pending_request_count(self, event):
#         count = event["count"]
#         await self.send(
#             text_data=json.dumps(
#                 {
#                     "type": "pending_request_count",
#                     "count": count,
#                 }
#             )
#         )

#     async def connection_accepted(self, event):
#         request_id = event["request_id"]

#         await self.send(
#             text_data=json.dumps(
#                 {
#                     "type": "connection_accepted",
#                     "request_id": request_id,
#                 }
#             )
#         )

#     async def connection_rejected(self, event):
#         request_id = event["request_id"]

#         await self.send(
#             text_data=json.dumps(
#                 {
#                     "type": "connection_rejected",
#                     "request_id": request_id,
#                 }
#             )
#         )






# for show connected

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Connection

# Database-related functions (wrapped in database_sync_to_async)
@database_sync_to_async
def get_user_by_id(user_id):
    return User.objects.get(id=user_id)

@database_sync_to_async
def create_connection(sender, receiver):
    return Connection.objects.create(sender=sender, receiver=receiver, status="Pending")

@database_sync_to_async
def get_sender_and_receiver(connection_id):
    connection = Connection.objects.get(id=connection_id)
    return connection.sender, connection.receiver

@database_sync_to_async
def update_connection_status(connection_id, status):
    connection = Connection.objects.get(id=connection_id)
    connection.status = status
    connection.save()
    return connection

@database_sync_to_async
def get_pending_request_count(user_id):
    return Connection.objects.filter(receiver_id=user_id, status="Pending").count()

class ConnectionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["url_route"]["kwargs"]["user_id"]
        self.room_group_name = f"user_{self.user}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

        # Send pending request count on connection
        pending_count = await get_pending_request_count(self.user)
        await self.send(
            text_data=json.dumps(
                {
                    "type": "pending_request_count",
                    "count": pending_count,
                }
            )
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get("type")

        # Handle sending a connection request
        if message_type == "send_connection_request":
            receiver_user_id = text_data_json["receiver_user_id"]
            sender_username = text_data_json["sender_username"]

            receiver = await get_user_by_id(receiver_user_id)
            sender_user = await get_user_by_id(self.user)

            # Create a connection between sender and receiver
            connection = await create_connection(sender_user, receiver)

            receiver_group_name = f"user_{receiver.id}"

            # Notify the receiver about the connection request and update the count
            await self.channel_layer.group_send(
                receiver_group_name,
                {
                    "type": "update_pending_request_count",
                    "count": await get_pending_request_count(receiver.id),
                },
            )

        # Handle accepting a connection request
        # elif message_type == "accept_connection_request":
        #     request_id = text_data_json["request_id"]
        #     sender, receiver = await get_sender_and_receiver(request_id)

        #     # Update connection status to "Accepted" in the database
        #     updated_connection = await update_connection_status(request_id, "Accepted")

        #     sender_group_name = f"user_{sender.id}"
        #     receiver_group_name = f"user_{receiver.id}"

        #     # Notify both sender and receiver that the connection request has been accepted
        #     await self.channel_layer.group_send(
        #         sender_group_name,
        #         {
        #             "type": "connection_accepted",
        #             "request_id": request_id,
        #             "receiver_id": receiver.id,
        #             "sender_username": sender.username
        #         },
        #     )
        #     await self.channel_layer.group_send(
        #         receiver_group_name,
        #         {
        #             "type": "connection_accepted",
        #             "request_id": request_id,
        #             "receiver_id": receiver.id,
        #             "sender_username": sender.username
        #         },
        #     )
        
        elif message_type == "accept_connection_request":
            request_id = text_data_json["request_id"]
            sender, receiver = await get_sender_and_receiver(request_id)

            # Update connection status to "Accepted" in the database
            updated_connection = await update_connection_status(request_id, "Accepted")

            sender_group_name = f"user_{sender.id}"
            receiver_group_name = f"user_{receiver.id}"

    # Notify both sender and receiver that the connection request has been accepted
            await self.channel_layer.group_send(
                sender_group_name,
                {
                    "type": "connection_accepted",
                    "request_id": request_id,
                    "receiver_id": receiver.id,
                    "sender_username": sender.username,
                },
    )
            await self.channel_layer.group_send(
                receiver_group_name,
                {
                    "type": "connection_accepted",
                    "request_id": request_id,
                    "receiver_id": receiver.id,
                    "sender_username": sender.username,
                },
            )


        # Handle rejecting a connection request
        elif message_type == "delete_connection_request":
            request_id = text_data_json["request_id"]
            sender, receiver = await get_sender_and_receiver(request_id)
            rejected_connection = await update_connection_status(request_id, "Rejected")

            sender_group_name = f"user_{sender.id}"
            receiver_group_name = f"user_{receiver.id}"

            await self.channel_layer.group_send(
                sender_group_name,
                {
                    "type": "connection_rejected",
                    "request_id": request_id,
                },
            )
            await self.channel_layer.group_send(
                receiver_group_name,
                {
                    "type": "connection_rejected",
                    "request_id": request_id,
                },
            )

    async def update_pending_request_count(self, event):
        count = event["count"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "pending_request_count",
                    "count": count,
                }
            )
        )

    async def connection_accepted(self, event):
        request_id = event["request_id"]
        receiver_id = event["receiver_id"]
        sender_username = event["sender_username"]

        await self.send(
            text_data=json.dumps(
                {
                    "type": "connection_accepted",
                    "request_id": request_id,
                    "receiver_id": receiver_id,
                    "sender_username": sender_username
                }
            )
        )

    async def connection_rejected(self, event):
        request_id = event["request_id"]

        await self.send(
            text_data=json.dumps(
                {
                    "type": "connection_rejected",
                    "request_id": request_id,
                }
            )
        )







