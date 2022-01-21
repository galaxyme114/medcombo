from django.conf.urls import url
from .views import Messenger
from .views import ReadMail
from .views import SentMail 
from .views import SentMailDetail
from .views import MessengerModal
from .views import MessageModal
from .views import ChatList, ChatHistory
from .views import load_dialog
from .views import SendMessage
from .views import ListMessage
from .views import GetMessage
from .views import SendMessageExtended
from .views import ModalMSG
from .views import SendMSG
from .views import MessagesSearchData
from .views import ReadMessage
from .views import change_condition
from .views import alert_msg_contact
from .views import alert_msg_mailer
from .views import ListContactAjax
from .views import CheckingAjax
from .views import delete_message
from .views import GetChatsUsers
from .views import SendChatUser
from .views import CheckingChatAjax
from .views import GetChatsChange
from .views import delete_chats
from .views import ListContactModalAjax
from .views import CheckingAjaxToModal
from .views import MessengerModalList
from .views import MessageModalList
from .views import CheckingOnline
from .views import UploadChatAttach, GetChatMute
from .views import GetChatsList, GetChatDelete
from .views import GetUserFromProduct, GetChatBlock
from .views import ImportantMailCheck, ImportantMail, ImportantMailRead, GetMSGNews, MsgInboxDel, MsgSentDel, GetChatsListPin

urlpatterns = [
                url(r'^messenger/inbox$', Messenger.as_view(), name='messenger'),
                url(r'^messenger/send_mail$', SentMail.as_view(), name='sentmail'),
                url(r'^messenger/important$', ImportantMail.as_view(), name='important'),
                url(r'^messenger/important/read/(?P<pk>[0-9]+)$$', ImportantMailRead.as_view(), name='importantread'),
                url(r'^messenger/inbox/read_mail/(?P<pk>[0-9]+)$', ReadMail.as_view(), name='readmail'),
                url(r'^messenger/send_mail/(?P<pk>[0-9]+)$', SentMailDetail.as_view(), name='readsentmail'),
                url(r'^messenger_modal/(?P<pk>[0-9]+)/$', MessengerModal.as_view(), name='messenger_modal'),
                url(r'^ajax/add_message_favorite$', ImportantMailCheck, name='ajax_change_favorite'),
                url(r'^messenger_modal_list/(?P<pk>[0-9]+)/$', MessengerModalList.as_view(), name='messenger_modal_list'),
                url(r'^message_modal/(?P<pk>[^/]+)/(?P<pd>[^/]+)/$', MessageModal.as_view(), name='message_modal'),
                url(r'^message_modal_list/(?P<pk>[^/]+)/(?P<pd>[^/]+)/$', MessageModalList.as_view(), name='message_modal_list'),
                url(r'^modal_msg/$', ModalMSG.as_view(), name='modal_msg'),
                url(r'^send_message/$', SendMessage, name='send_message'),
                url(r'^send_msg/$', SendMSG, name='send_msg'),
                url(r'^extended_message/$', SendMessageExtended, name='extended_message'),
                url(r'^list_message/$', ListMessage, name='list_message'),
                url(r'^get_message/$', GetMessage, name='get_message'),
                url(r'^read_message/$', ReadMessage, name='read_message'),
                url(r'^chat_list/$', ChatList.as_view(), name='chat_list'),
                url(r'^chat_history/(?P<pk>[0-9]+)/$', ChatHistory.as_view(), name='chat_history'),
                url(r'^ajax/load-dialog$', load_dialog, name='ajax_load_dialog'),
                url(r'^messages-autocomplete/$', MessagesSearchData.as_view(), name='messages-autocomplete'),
                url(r'^ajax/change_condition', change_condition, name='ajax_change_condition'),
                url(r'^ajax/alert_msg_contact', alert_msg_contact, name='alert_msg_contact'),
                url(r'^ajax/alert_msg_mailer', alert_msg_mailer, name='alert_msg_mailer'),
                url(r'^ajax/list_contact_ajax', ListContactAjax, name='list_contact_ajax'),
                url(r'^ajax/checking_ajax', CheckingAjax, name='checking_ajax'),
                url(r'^ajax/checking_online', CheckingOnline, name='checking_online'),
                url(r'^delete_messages/$', delete_message, name='delete_messages'),
                url(r'^get_chat_users/$', GetChatsUsers, name='get_chat_users'),
                url(r'^send_chat_user/$', SendChatUser, name='send_chat_user'),
                url(r'^ajax/checking_chat_ajax', CheckingChatAjax, name='checking_chat_ajax'),
                url(r'^get_chat_change/$', GetChatsChange, name='get_chat_change'),
                url(r'^delete_chats/$', delete_chats, name='delete_chats'),
                url(r'^ajax/check_Count', CheckingAjaxToModal, name='check_Count'),
                url(r'^check_ajax_modal_list/$', ListContactModalAjax, name='check_ajax_modal_list'),
                url(r'^ajax/upload_chat_attach', UploadChatAttach, name='upload_chat_attach'),
                url(r'^ajax/get_chat_list', GetChatsList, name='get_chat_list'),
                url(r'^ajax/get_chat_pin_list', GetChatsListPin, name='get_chat_pin_list'),
                url(r'^ajax/get_msg_news', GetMSGNews, name='get_msg_news'),
                url(r'^ajax/get_user_from_product', GetUserFromProduct, name='get_user_from_product'),
                url(r'^ajax_inbox_delete', MsgInboxDel, name='ajax_inbox_delete'),
                url(r'^ajax_sent_delete', MsgSentDel, name='ajax_sent_delete'),
                url(r'^ajax/get_chat_block', GetChatBlock, name='get_chat_block'),
                url(r'^ajax/get-chat-list-del', GetChatDelete, name='get_chat_list_del'),
                url(r'^ajax/get-chat-mute', GetChatMute, name='get_chat_mute'),
                
              ]