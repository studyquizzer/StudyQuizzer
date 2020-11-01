from difflib import SequenceMatcher as match
from fuzzywuzzy import fuzz


def similar(a, b):
    return match(None, a, b).ratio()


def similar_(a, b) -> int:
    return fuzz.token_sort_ratio(a, b)


def create_chat(chat, user1_already_exist, user2_already_exist):
    from pusher_chatkit import PusherChatKit
    from pusher_chatkit.backends import RequestsBackend, TornadoBackend

    chatkit = PusherChatKit(
        "v1:us1:97ddda7c-e92a-4443-a768-fa12c03b0fff",
        "5ec3ae22-2851-4e5b-8024-b70940ce21f8:htxGjZqQNtjRY29JZsoB62a+bQRqLHBiWbbcnJtyiDE=",
        RequestsBackend or TornadoBackend,
    )

    if not user1_already_exist:
        chatkit.create_user(chat.user1.username, chat.user1.profile.slug)
    if not user2_already_exist:
        chatkit.create_user(chat.user2.username, chat.user2.profile.slug)
