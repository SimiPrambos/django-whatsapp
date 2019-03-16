# from background_task import background
# from messages_app.models import WhatsappChatMessages, WhatsappMediaMessages
# from .drivers import send_message

# @background()
# def send_message_task(id):
#     is_running, is_logged_in = [status for status in status_instance(id)]
#     if is_running and is_logged_in:
#         chats = WhatsappChatMessages.objects.filter(
#             number_id=id, message_type='OUT',
#             message_status='P', send_retry__lt=3
#         )
#         medias = WhatsappMediaMessages.objects.filter(
#             number_id=id, message_type='OUT',
#             message_status='P', send_retry__lt=3
#         )

#         if chats:
#             print("Send message to ", chat.get_chatid)
#             chat.message_status = send_message(id, chat.get_chatid, chat.message_content)
#             chat.save()