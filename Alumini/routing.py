from django.urls import path,re_path
from myapp import consumers
websocket_urlpatterns  = [
    re_path(r'ws/connection/(?P<user_id>\d+)/$', consumers.ConnectionConsumer.as_asgi()),
]

