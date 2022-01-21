from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from medcombo.configuration.usercustom.models import User
from django.shortcuts import render
from medcombo.social_network.contacts.models import Contacts
from medcombo.social_network.contacts.forms import SearchFormContact
from django.db.models import Q
from medcombo.configuration.company.models import Company
from django.urls import reverse_lazy, reverse
from medcombo.social_network.contacts.models import Message, ChatUser, ChatExtended
from medcombo.product.models import Product, SuggestionKeyword
from django.http import HttpResponseRedirect, HttpResponse
from medcombo.social_network.contacts.models import MessageExtended, ChatAttach
from django.http import Http404
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from dal import autocomplete
from medcombo.social_network.chat.forms import SearchFormMessages
from collections import OrderedDict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from medcombo.configuration.usercustom.models import UserOnline
import json
from django.http import JsonResponse
from django.core import serializers
import datetime

@login_required
def ListMessage(request):
    my_id = request.POST.get('id')
    mailer = request.POST.get('mailer')
    icon = request.POST.get('icon')
    if mailer == 'Vacio':
        my_messages = Message.objects.filter(mailer=my_id).exclude(removed=True).order_by('-created')
    else:
        my_messages = Message.objects.filter(receiver=my_id,mailer=mailer).exclude(removed_receiver=True).order_by('-created')
    return render(request, 'social_network/chat/search_messages.html', {'my_messages': my_messages,'mailer':mailer,'icon':icon}) 

@login_required
def GetMessage(request):
    my_id = request.POST.get('id')
    zone = request.POST.get('zone')
    my_messages = Message.objects.filter(id=my_id)
    my_messages_extended = MessageExtended.objects.filter(reference=my_id).order_by('-created').exclude(message="", attach_id=None)
    id_message = my_messages[0].id
    return render(request, 'social_network/chat/get_messages.html', {'messages': my_messages,'id':id_message,'extended':my_messages_extended, 'zone':zone})

@login_required
def SendMessageExtended(request):
    if request.is_ajax():
        if request.method == 'POST':
            id_msg = request.POST.get('id')
            my_text = request.POST.get('text')
            my_user = request.user.id
            zone = request.POST.get('zone')
            reference = Message.objects.get(id=id_msg)
            user = User.objects.get(id=my_user)
            send_msg = MessageExtended(reference=reference, message=my_text, mailer=user)
            send_msg.save()
            temp_msg = Message.objects.filter(id=id_msg)
            for temp in temp_msg:
                if temp.mailer.id == my_user:
                    change_message = Message.objects.get(id=id_msg)
                    change_message.read = False
                    change_message.save()
                else:
                    change_message = Message.objects.get(id=id_msg)
                    change_message.read_mailer = False
                    change_message.save()
            msg = MessageExtended.objects.filter(reference=id_msg).order_by('-created').exclude(message="", attach_id=None)
            return render(request, 'social_network/chat/messages_extended.html', {'msg': msg, 'zone':zone})
    return HttpResponse('<p>Error in Request!</p>')

@login_required
def ReadMessage(request):
    mailer = request.POST.get('mailer')
    message = request.POST.get('message')
    if int(mailer) != int(request.user.id):
        my_read = Message.objects.get(id=message)
        if my_read.read == False:
            my_read.read = True
            my_read.save()
        return HttpResponse('Ok')
    else:
        my_read = Message.objects.get(id=message)
        if my_read.read_mailer == False:
            my_read.read_mailer = True
            my_read.save()
        return HttpResponse('Ok')
    return HttpResponse('Error in request!')

class MyFormListView(FormMixin, ListView):
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})
        context = self.get_context_data(object_list=self.object_list, form=self.form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

@login_required
def SendMSG(request):
    if request.is_ajax():
        if request.method == 'POST':
            text = request.POST.get('text')
            user = request.user.id
            owner = request.POST.get('owner')
            subject = request.POST.get('subject')
            my_user = User.objects.get(id=user)
            my_owner = User.objects.get(username=owner)
            if text == '' or text is None:
                return HttpResponse('Empty')
            else:
                message = Message(mailer=my_user, receiver=my_owner, subject=subject, message=text, read_mailer=True)
                message.save()
                return HttpResponse('Ok')
    return HttpResponse('Error in request!')

@login_required
def alert_msg_contact(request):
    if request.is_ajax():
        if request.method == 'POST':
            mailer = request.POST.get('mailer')
            receiver = request.user.id
            my_flag = Message.objects.filter(mailer=mailer,receiver=receiver,read=False).count()
            return HttpResponse(my_flag)
    return HttpResponse('Error in request!')

@login_required
def alert_msg_mailer(request):
    if request.is_ajax():
        if request.method == 'POST':
            receiver = request.user.id
            my_flag = Message.objects.filter(mailer=receiver,read_mailer=False).count()
            return HttpResponse(my_flag)
    return HttpResponse('Error in request!')

class ModalMSG(LoginRequiredMixin, MyFormListView):
    model = Message
    form_class = SearchFormContact
    template_name = "social_network/chat/modal_msg.html"

class Messenger(LoginRequiredMixin, ListView):
    #slug_field = 'username'
    #slug_url_kwarg = 'username'
    model = Message
    template_name = "social_network/chat/messenger.html"

    def get_context_data(self, **kwargs):
        ctx = super(Messenger, self).get_context_data(**kwargs)
        my_user = self.request.user.id
        info_user = User.objects.filter(id=my_user)
        my_messages = Message.objects.filter(receiver=my_user).order_by('-created')
        my_messages_list = Message.objects.filter(receiver=my_user).exclude(removed_receiver=True).order_by('read')
        my_sent = Message.objects.filter(mailer=my_user).exclude(removed=True)
        list_contacts = []
        my_contacts = []
        for my_msg in my_messages_list:
            list_contacts.append(my_msg.mailer)
        #New list ordered. This list has not elements repeated
        my_contacts = OrderedDict.fromkeys(list_contacts).keys()
        #my_contacts = set(list_contacts)
        my_msg_form = SearchFormMessages
        ctx['list_contacts'] = my_contacts
        ctx['list_messages'] = my_messages
        ctx['list_user'] = my_user
        ctx['mgs_sent'] = my_sent
        ctx['info_user'] = info_user
        ctx['msg_form'] = my_msg_form
        return ctx

class ReadMail(LoginRequiredMixin, DetailView):

    model = Message
    template_name = "social_network/chat/read_mail.html"

    def get_context_data(self, **kwargs):
        ctx = super(ReadMail, self).get_context_data(**kwargs)
        my_user = self.request.user.id
        my_messages = Message.objects.get(receiver=my_user, id=self.kwargs.get('pk'))
        if my_messages.read != 'True':
            Message.objects.filter(receiver=my_user, id=self.kwargs.get('pk')).update(read='True')
        else:
            pass

        ctx["message_read"] = my_messages

        return ctx

class SentMail(LoginRequiredMixin, ListView):
    
    model = Message
    template_name = "social_network/chat/mailsent.html"

    def get_context_data(self, **kwargs):
        ctx = super(SentMail, self).get_context_data(**kwargs)
        send_user = self.request.user.id
        send_messages = Message.objects.filter(mailer=send_user).order_by("-created")
        ctx["message_sent"] = send_messages

        return ctx

class SentMailDetail(LoginRequiredMixin, DetailView):
    
    model = Message
    template_name = "social_network/chat/mailsent_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super(SentMailDetail, self).get_context_data(**kwargs)
        my_user = self.request.user.id
        sent_detail_messages = Message.objects.get(mailer=my_user, id=self.kwargs.get('pk'))
        ctx["message_sent_detail"] = sent_detail_messages

        return ctx

@login_required
def ImportantMailCheck(request):
    msg_id = request.POST.get('msg_id')
    msg = Message.objects.get(pk=msg_id)
    if msg.important == True:
        Message.objects.filter(pk=msg_id).update(important="False")
        print("eliminado de favorito")
    else:
        Message.objects.filter(pk=msg_id).update(important="True")
        print("actualizado a favorito")
    return HttpResponse('OK')

class ImportantMail(LoginRequiredMixin, ListView):
    
    model = Message
    template_name = "social_network/chat/mail_favorite.html"

    def get_context_data(self, **kwargs):
        ctx = super(ImportantMail, self).get_context_data(**kwargs)
        send_user = self.request.user.id
        favorite_messages = Message.objects.filter(receiver=send_user, important="True")
        ctx["favorite_messages"] = favorite_messages

        return ctx
        
class ImportantMailRead(LoginRequiredMixin, DetailView):
    
    model = Message
    template_name = "social_network/chat/mail_favorite_read.html"

    def get_context_data(self, **kwargs):
        ctx = super(ImportantMailRead, self).get_context_data(**kwargs)
        my_user = self.request.user.id
        my_messages = Message.objects.get(receiver=my_user, id=self.kwargs.get('pk'))
        ctx["message_read"] = my_messages

        return ctx

class MessengerModal(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('view_login')
    model = User
    template_name = "social_network/chat/messenger_modal.html"

    def get_context_data(self, **kwargs):
        context = super(MessengerModal,self).get_context_data(**kwargs)
        user = UserOnline.objects.get(user=self.kwargs.get('pk'))
        print(user)
        context['my_list'] = UserOnline.objects.filter(user=self.kwargs.get('pk'))
        context['user_id'] = user.pk
        current_user = UserOnline.objects.get(user=user.pk)
        context['current_user'] = current_user
        return context

class MessengerModalList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('view_login')
    model = User
    template_name = "social_network/chat/messenger_modal.html"

    def get_context_data(self, **kwargs):
        context = super(MessengerModalList,self).get_context_data(**kwargs)
        user = User.objects.get(company=self.kwargs.get('pk'))
        context['my_list'] = UserOnline.objects.filter(user=user.pk)
        context['user_id'] = user.pk
        current_user = UserOnline.objects.get(user=user.pk)
        context['current_user'] = current_user
        return context

@login_required
def GetUserFromProduct(request):
    company_id = request.POST.get('company_id')
    user = User.objects.get(company_id=company_id)
    current_user = UserOnline.objects.get(user=user.pk)
    return JsonResponse({'user_id': current_user.user.id, 'user_name': current_user.user.username, 
        'first_name':current_user.user.first_name, 'last_name':current_user.user.last_name, 'company_name': current_user.user.company.name})
@login_required
def SendMessage(request):
    if request.is_ajax():
        if request.method == 'POST':
            text = request.POST.get('text')
            user = request.user.id
            owner = request.POST.get('owner')
            product = request.POST.get('product')
            subject = request.POST.get('subject')
            amount = request.POST.get('amount')
            my_user = User.objects.get(id=user)
            my_owner = User.objects.get(id=owner)
            if product is None or product == '':
                if text == '' or text is None:
                    return HttpResponse('Empty')
                else:
                    message = Message(mailer=my_user, receiver=my_owner, subject=subject, message=text, read_mailer=True)
                    message.save()
                    return HttpResponse('Ok')
            else:
                my_product = Product.objects.get(id=product)
                if text == '' or text is None:
                    return HttpResponse('Empty')
                else:
                    message = Message(mailer=my_user, receiver=my_owner, subject=subject, message=text, product=my_product, amount=amount, read_mailer=True)
                    message.save()
                    return HttpResponse('Ok')
    return HttpResponse('Error in request!')

class MessageModal(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('view_login')
    model = Message
    template_name = "social_network/chat/message_modal.html"

    def get_context_data(self, **kwargs):
        ctx = super(MessageModal, self).get_context_data(**kwargs)
        receiver = self.kwargs.get('pk')
        product = self.kwargs.get('pd')
        mailer = self.request.user.id
        if product == 'None':
            products = 'None'
        else:
            products = Product.objects.get(id=product)
        owner = User.objects.get(id=receiver)
        ctx['info_owner'] = owner
        ctx['info_product'] = products
        ctx['info_user'] = mailer
        return ctx

class MessageModalList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('view_login')
    model = Message
    template_name = "social_network/chat/message_modal.html"

    def get_context_data(self, **kwargs):
        ctx = super(MessageModalList, self).get_context_data(**kwargs)
        user = User.objects.get(company=self.kwargs.get('pk'))
        receiver = user.pk
        product = self.kwargs.get('pd')
        mailer = self.request.user.id
        if product == 'None':
            products = 'None'
        else:
            products = Product.objects.get(id=product)
        owner = User.objects.get(id=receiver)
        ctx['info_owner'] = owner
        ctx['info_product'] = products
        ctx['info_user'] = mailer
        return ctx

class ChatHistory(LoginRequiredMixin, ListView):
    model = UserOnline
    template_name = 'social_network/chat/chat_history.html'
    def get_context_data(self, **kwargs):
        ctx = super(ChatHistory, self).get_context_data(**kwargs)
        current_user_id = self.kwargs.get('pk')

        current_user = UserOnline.objects.get(user=current_user_id)
        ctx['current_user'] = current_user
        return ctx
class ChatList(LoginRequiredMixin, ListView):
    model = UserOnline
    ordering = ['-active']
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'social_network/chat/chat.html'

    def get_context_data(self, **kwargs):
        ctx = super(ChatList, self).get_context_data(**kwargs)
        owner_user = self.request.user.id
        my_chat_user = ChatUser.objects.filter(receiver=self.request.user.id)
        my_mailer_chat = ChatUser.objects.filter(mailer=self.request.user.id)
        list_first = []
        list_second = []
        if my_chat_user:
            for f in my_chat_user:
                user_online = UserOnline.objects.get(user=f.mailer.id)
                list_first.append(user_online)
        if my_mailer_chat:
            for s in my_mailer_chat:
                user_online_second = UserOnline.objects.get(user=s.receiver.id)
                list_second.append(user_online_second)
        list_first.extend(list_second)
        result_list = set(list_first)
        #Chats Number
        my_new_chats = ChatUser.objects.filter(receiver=self.request.user.id, read=False)
        chat_change = ChatUser.objects.filter(Q(receiver=self.request.user.id) | Q(mailer=self.request.user.id))
        counter_chat_change = 0
        list_users = []
        list_new = []
        for n in my_new_chats:
            user_new = User.objects.get(id=n.mailer.id)
            list_new.append(user_new)
        for c in chat_change:
            extend_chat_change = ChatExtended.objects.filter(reference=c.id,read=False).exclude(mailer=self.request.user.id).count()
            counter_chat_change += extend_chat_change
            msg_chat = ChatExtended.objects.filter(reference=c.id,read=False).exclude(mailer=self.request.user.id).order_by('-created')
            if msg_chat:
                user = User.objects.get(id=msg_chat[0].mailer.id)
                list_users.append(user)
        
        list_new = set(list_new)
        list_users.extend(list_new)
        list_users = set(list_users)
        my_count_users = UserOnline.objects.all().filter(active=True).exclude(user=owner_user).exclude(user__username="admin").count()
        #my_query = MyChat.objects.filter(dialog_id__owner_id=owner_user, read=False)
        ctx['counter_initial'] = my_count_users
        ctx['list_chats_online'] = result_list
        ctx['user_msg'] = list_users
        return ctx

@login_required
def load_dialog(request):
    id = request.GET.get('user')
    my_user = User.objects.filter(id=id).order_by('username')
    return render(request, 'social_network/chat/dialog.html', {'my_user': my_user})

@login_required
def change_condition(request):
    if request.is_ajax():
        if request.method == 'POST':
            """my_chat = MyChat.objects.filter(read=False).exclude(sender_id=request.user.id)
            for chats in my_chat:
                change = MyChat.objects.get(id=chats.id)
                change.read = True
                change.save()
            return HttpResponse('It is made!')"""
    return HttpResponse('Something is wrong!')

class MessagesSearchData(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Message.objects.filter(receiver=self.request.user.id)
        if self.q:
            qs = qs.filter(relationship__username__istartswith=self.q)
        return qs

@login_required
def ListContactAjax(request):
    my_chat_user = ChatUser.objects.filter(receiver=request.user.id)
    my_mailer_chat = ChatUser.objects.filter(mailer=request.user.id)
    list_first = []
    list_second = []
    if my_chat_user:
        for f in my_chat_user:
            user_online = UserOnline.objects.get(user=f.mailer.id)
            list_first.append(user_online)
    if my_mailer_chat:
        for s in my_mailer_chat:
            user_online_second = UserOnline.objects.get(user=s.receiver.id)
            list_second.append(user_online_second)
    list_first.extend(list_second)
    result_list = set(list_first)
    #Chats Number
    my_new_chats = ChatUser.objects.filter(receiver=request.user.id, read=False)
    chat_change = ChatUser.objects.filter(Q(receiver=request.user.id) | Q(mailer=request.user.id))
    counter_chat_change = 0
    list_users = []
    list_new = []
    for n in my_new_chats:
        user_new = User.objects.get(id=n.mailer.id)
        list_new.append(user_new)
    for c in chat_change:
        extend_chat_change = ChatExtended.objects.filter(reference=c.id,read=False).exclude(mailer=request.user.id).count()
        counter_chat_change += extend_chat_change
        msg_chat = ChatExtended.objects.filter(reference=c.id,read=False).exclude(mailer=request.user.id).order_by('created')
        if msg_chat:
            user = User.objects.get(id=msg_chat[0].mailer.id)
            list_users.append(user)
    
    list_new = set(list_new)
    list_users.extend(list_new)
    list_users = set(list_users)
    return render(request, 'social_network/chat/ajax_contacts_list.html', {'list_contacts_object': result_list, 'user_msg': list_users})

@login_required
def CheckingOnline(request):
    id_receiver = request.POST.get('id')
    count_users = UserOnline.objects.filter(active=True, user_id=id_receiver).count()
    return HttpResponse(count_users)

@login_required
def CheckingAjax(request):
    count_users = UserOnline.objects.filter(active=True).exclude(user=request.user.id).count()
    return HttpResponse(count_users)

@login_required
def delete_message(request):
    msg_id = request.POST.get('value')
    msg = Message.objects.get(id=msg_id)
    if msg.receiver.id == request.user.id:
        msg.removed_receiver = True
        msg.save()
    else:
        msg.removed = True
        msg.save()
    total_delete = Message.objects.get(id=msg_id)
    if total_delete.removed == True and total_delete.removed_receiver == True:
        total_delete.delete()
        print('borrado')
    return HttpResponse('Ok')

@login_required
def GetChatsUsers(request):
    id_receiver = request.POST.get('id')
    zone = request.POST.get('zone')
    id_mailer = request.user.id
    print("id_receiver", id_receiver)
    print("id_mailer",id_mailer)
    if ChatUser.objects.filter(Q(mailer=id_receiver, receiver=id_mailer) | Q(mailer=id_mailer, receiver=id_receiver)).exists():
        if ChatUser.objects.filter(mailer=id_receiver, receiver=id_mailer):
            block_item = ChatUser.objects.get(mailer=id_receiver, receiver=id_mailer)
        else:
            block_item = ChatUser.objects.get(mailer=id_mailer, receiver=id_receiver) 
    else:
        block_item = {}
    if ChatUser.objects.filter(receiver=id_mailer).exists():
        mute_item = ChatUser.objects.filter(receiver=id_mailer)[0]
    else:
        mute_item = {}

    my_messages = ChatUser.objects.filter(Q(mailer=id_mailer,receiver=id_receiver) | Q(mailer=id_receiver,receiver=id_mailer))
    if my_messages:
        id_msg = my_messages[0].id
        print("+++++++++++++++++++",id_msg)
        chat_change = ChatUser.objects.get(id=id_msg)
        chat_change.read = True
        chat_change.save()
        if my_messages[0].removed == True and request.user.id == my_messages[0].mailer.id:
            extend = ChatExtended.objects.filter(reference=id_msg, active=True).exclude(message="", attach_id=None).order_by('created')
            if extend:
                extended = extend
            else:
                extended = None
        elif my_messages[0].removed_receiver == True and request.user.id == my_messages[0].receiver.id:
            extended = None
        else:
            extended = ChatExtended.objects.filter(reference=id_msg).exclude(message="", attach_id=None).order_by('created')
            for e in extended:
                if e.mailer.id != request.user.id:
                    e.read = True
                    e.save() 
    else:
        extended = None
    return render(request, 'social_network/chat/get_chats.html', {'messages': my_messages, 'extended': extended, 'zone':zone, 'block_item': block_item, 'mute_item':mute_item})

@login_required
def GetChatsList(request):
    zone = request.POST.get('zone')
    owner_id = request.POST.get('owner_id')
    my_chat_user = ChatUser.objects.filter(receiver=owner_id).order_by("-pin")
    my_mailer_chat = ChatUser.objects.filter(mailer=owner_id).order_by("-pin")
    list_first = []
    list_second = []
    if my_chat_user:
        for f in my_chat_user:
            user_online = UserOnline.objects.get(user=f.mailer.id)
            user_online.new_msg = ChatExtended.objects.filter(reference=f.id, read=False).exclude(mailer=owner_id).count()
            list_first.append(user_online)
    if my_mailer_chat:
        for s in my_mailer_chat:
            user_online_second = UserOnline.objects.get(user=s.receiver.id)
            user_online_second.new_msg = ChatExtended.objects.filter(reference=s.id, read=False).exclude(mailer=owner_id).count()
            list_second.append(user_online_second)
            
    
    list_first.extend(list_second)
    result_list = sorted(set(list_first), key=list_first.index)
    return render(request, 'social_network/chat/ajax_chats_list.html', {'chat_users': result_list, 'zone':zone})

@login_required
def GetChatsListPin(request):
    owner_id = request.POST.get('owner_id')
    select_id = request.POST.get('select_id')
    nowdate = datetime.datetime.now()
    pin = (str(nowdate.year) + str(nowdate.strftime("%m")) + str(nowdate.strftime("%d")) + str(nowdate.strftime("%H")) + str(nowdate.strftime("%M")) + str(nowdate.strftime("%S")))
    if ChatUser.objects.filter(Q(receiver=owner_id, mailer=select_id) | Q(receiver=select_id, mailer=owner_id)):
        if  ChatUser.objects.filter(receiver=owner_id, mailer=select_id).exists():
            my_pin = ChatUser.objects.get(receiver=owner_id, mailer=select_id)
        else:
            my_pin = ChatUser.objects.get(receiver=select_id, mailer=owner_id)
        my_pin.pin = pin
        my_pin.save()
        
    return HttpResponse("OK")

@login_required
def GetChatBlock(request):
    owner = request.POST.get('owner')
    select = request.POST.get('select')
    my_block = ChatUser.objects.get(receiver=owner, mailer=select)
    my_block.block = True
    my_block.save()
    return HttpResponse("OK")

@login_required
def GetChatMute(request):
    owner = request.POST.get('owner_id')
    mute = ChatUser.objects.filter(receiver=owner)
    for m in mute:
        m.mute = True
        m.save()
    return HttpResponse("OK")

@login_required
def GetChatDelete(request):
    owner = request.POST.get('owner_id')
    select = request.POST.get('select_id')
    my_block = ChatUser.objects.get(Q(receiver=owner, mailer=select) | Q(receiver=select, mailer=owner))
    my_block.delete()
    return HttpResponse("OK")

@login_required
def GetMSGNews(request):
    owner_id = request.POST.get('owner_id')
    my_msg_news = Message.objects.filter(receiver=owner_id, read="False").count()
    return render(request, 'social_network/chat/ajax_message_news.html', {'my_msg_news': my_msg_news})

@login_required
def SendChatUser(request):
    if request.is_ajax():
        if request.method == 'POST':
            text = request.POST.get('text')
            mailer = request.user.id
            receiver = request.POST.get('id')
            zone = request.POST.get('zone')
            attach_id = request.POST.get('attach_id')
            my_user = User.objects.get(id=receiver)
            my_owner = User.objects.get(id=mailer)
            my_messages = ChatUser.objects.filter(Q(mailer=mailer,receiver=receiver) | Q(mailer=receiver,receiver=mailer))
            if my_messages:
                chat = ChatUser.objects.get(id=my_messages[0].id)
                extended_message = ChatExtended(reference=chat, message=text, mailer=my_owner, read=False, attach_id=attach_id)
                extended_message.save()
                extended = ChatExtended.objects.filter(id=extended_message.pk).exclude(message="", attach_id=None).order_by('created')
                return render(request, 'social_network/chat/get_extend.html', {'extended': extended,'zone':zone})
            else:
                chat = ChatUser(receiver=my_user, mailer=my_owner, message=text, read=False)
                chat.save()
                my_message_user = ChatUser.objects.filter(id=chat.pk)
                return render(request, 'social_network/chat/get_extend_first.html', {'messages': my_message_user,'zone':zone})
    return HttpResponse('Error in request!')

@login_required
def CheckingChatAjax(request):
    user = request.POST.get('data')
    count_chats = ChatUser.objects.all().filter(read=False).filter(Q(mailer=request.user.id,receiver=user) | Q(mailer=user,receiver=request.user.id)).count()
    return HttpResponse(count_chats)

@login_required
def GetChatsChange(request):
    id_receiver = request.POST.get('id')
    zone = request.POST.get('zone')
    id_mailer = request.user.id
    my_messages = ChatUser.objects.filter(Q(mailer=id_mailer,receiver=id_receiver) | Q(mailer=id_receiver,receiver=id_mailer))#mailer=id_mailer,receiver=id_receiver)
    count = 0
    if my_messages:
        id_msg = my_messages[0].id
        extended = ChatExtended.objects.filter(reference=id_msg, read=False).exclude(message="", attach_id=None).order_by('created')
        count = extended.count()
        if extended:
            if extended[0].mailer.id != request.user.id:
                extended[0].read = True
                extended[0].save()
        else:
            if my_messages[0].receiver.id == request.user.id:
                if my_messages[0].read == False:
                    my_messages[0].read = True
                    my_messages[0].save()
                    my_message_user = ChatUser.objects.filter(Q(mailer=id_mailer,receiver=id_receiver) | Q(mailer=id_receiver,receiver=id_mailer))
                    return render(request, 'social_network/chat/get_extend_first.html', {'messages': my_message_user,'zone':zone})
    else:
        extended = None
    if count != 0:
        if extended:
            if extended[0].mailer.id == request.user.id:
                return HttpResponse('No')
            else:
                return render(request, 'social_network/chat/get_extend.html', {'messages': my_messages, 'extended': extended,'zone':zone})
    else:
        return HttpResponse('No')

@login_required
def delete_chats(request):
    user_id = request.POST.get('value')
    chats = ChatUser.objects.filter(Q(mailer=request.user.id,receiver=user_id) | Q(mailer=user_id,receiver=request.user.id))
    if chats:
        chat = ChatUser.objects.get(Q(mailer=request.user.id,receiver=user_id) | Q(mailer=user_id,receiver=request.user.id))
        if chat.receiver.id == request.user.id:
            extended = ChatExtended.objects.filter(reference=chat.id)
            for e in extended:
                e.read = True
                e.active = False
                e.save()
            chat.removed_receiver = True
            chat.save()
        else:
            extended = ChatExtended.objects.filter(reference=chat.id)
            for e in extended:
                e.read = True
                e.active = False
                e.save()
            chat.removed = True
            chat.save()
        total_delete = ChatUser.objects.get(Q(mailer=request.user.id,receiver=user_id) | Q(mailer=user_id,receiver=request.user.id))
        if total_delete.removed == True and total_delete.removed_receiver == True:
            total_delete.delete()
            print('borrado')
    return HttpResponse('Ok')

@login_required
def CheckingAjaxToModal(request):
    id_data = request.POST.get('data')
    count_user = UserOnline.objects.filter(active=True,user=int(id_data)).count()
    return HttpResponse(count_user)

@login_required
def ListContactModalAjax(request):
    id_data = request.POST.get('data')
    list_contacts_object = UserOnline.objects.filter(user=int(id_data))
    return render(request, 'social_network/chat/ajax_contacts_modal_list.html', {'my_list': list_contacts_object})

@login_required
def UploadChatAttach(request):
    if request.method == 'POST':
        attach = ChatAttach(
            name = request.FILES['file'],
            file = request.FILES.get('file')
            )
        attach.save()
        return HttpResponse(attach.id)

@login_required
def MsgInboxDel(request):
    remove = request.POST.get('remove')
    if remove:
        remove_each = remove.split(",")
        for each in remove_each:
            if each != "":
                Del = Message.objects.get(pk=each)
                Del.delete()
            else:
                print("this is empty string!")

        return HttpResponse('OK')
    else:
        return HttpResponse('NO')

@login_required
def MsgSentDel(request):
    remove = request.POST.get('remove')
    if remove:
        remove_each = remove.split(",")
        for each in remove_each:
            if each != "":
                Del = Message.objects.get(pk=each)
                Del.delete()
            else:
                print("this is empty string!")

        return HttpResponse('OK')
    else:
        return HttpResponse('NO')