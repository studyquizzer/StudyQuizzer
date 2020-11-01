"""
    Urls route to messaging app.
        get_auth_details fetches auth details to chat backend
        setRoomId sets a room id to a chat object
        getRoomId gets a room id and send back to client
"""

from django.urls import path

from chat.views import get_auth_details
from chat.views import set_room_id
from chat.views import Message
from chat.views import send_room_id


urlpatterns = [
    path("get_auth_details", get_auth_details, name="getDetails"),
    path("<slug:slug>", Message.as_view(), name="message"),
    path("setRoomId/<int:id>", set_room_id, name="roomId"),
    path("getRoomId/<int:id>", send_room_id, name="sendRoomId"),
]
