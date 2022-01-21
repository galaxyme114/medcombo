from .models import User
from .models import UserOnline
from medcombo.configuration.company.models import Company
from medcombo.social_network.contacts.models import Contacts
from medcombo.crm.dashboard_admin.models import Banner, Campaign, BannerUser
from medcombo.crm.task.models import Task
from medcombo.myweb.dashboard_client.post.models import Post
from medcombo.product.forms import SearchFormProduct
from medcombo.product.models import Keyword, Product, SuggestionKeyword, FavoriteProduct
from medcombo.crm.dashboard_admin.models import BannerIndex
from medcombo.social_network.contacts.models import Message as Messages
from medcombo.social_network.contacts.models import ChatExtended, ChatUser
from django.utils import translation
from django.contrib.sessions.models import Session
from django.utils import timezone
import threading
import os.path
from django.db.models import Q
from medcombo.myweb.job.models import Job
from medcombo.crm.dashboard_admin.models import LanguageCampaign


#Completed Registration
def return_registration(registration):
    add_value = 0
    for list_user in registration:
        #email
        if list_user.email != '' or list_user.email is None:
            add_value += 12
        #work
        if list_user.work_id != 0 or list_user.work_id is None:
            add_value += 12
        #company
        if list_user.company_id != 0 or list_user.company_id is None:
            add_value += 12
        #country
        if list_user.country_id != '' or list_user.country_id is None:
            add_value += 12
        #telephone
        if list_user.telephone != '' or list_user.telephone is None:
            add_value += 12
        #first_name
        if list_user.first_name != '' or list_user.first_name is None:
            add_value += 12
        #last_name
        if list_user.last_name != '' or list_user.last_name is None:
            add_value += 12
        #picture
        if list_user.picture != '' or list_user.picture is None:
            add_value += 16
        return add_value

#Banner Slide
def return_slide():
    actual_lang = translation.get_language()
    my_list = []
    slide = Banner.objects.all()
    for my_value in slide:
        if my_value.language_campaign.value_language == actual_lang and my_value.banner_campaign.activate_campaign == True:
            my_list.append(my_value.picture_campaign)
    return my_list

def datauser(request):
    actual_lang = translation.get_language()
    if actual_lang == 'es':
        idlang = 4
    elif actual_lang == 'de':
        idlang = 2
    elif actual_lang == 'en':
        idlang = 3
    elif actual_lang == 'fr':
        idlang = 5
    elif actual_lang == 'it':
        idlang = 6
    elif actual_lang == 'pt':
        idlang = 7
    elif actual_lang == 'zh-hans':
        idlang = 8
    elif actual_lang == 'ja':
        idlang = 9
    elif actual_lang == 'zh-hant':
        idlang = 1
    task_pendientes = Task.objects.filter(done=True, language=idlang).count()
    palabras_claves = SuggestionKeyword.objects.filter(status='En Proceso', notify=True).count()
    notificaciones_myweb2 =  Company.objects.filter(approved=False, notify= True).exclude(pk=1)
    excluir_leads=0
    for empresa in notificaciones_myweb2:
        idempresa= empresa.pk
        user= User.objects.filter(company_id=idempresa,lead=True)
        if user:
            excluir_leads= excluir_leads+1
    user_alarm = User.objects.filter(is_staff=False, indicated=True, lead=False,employee=False).count()
    notificaciones_myweb= notificaciones_myweb2.count()-excluir_leads
    #total_notificaciones= notificaciones_myweb + user_alarm + palabras_claves + task_pendientes
    total_notificaciones= notificaciones_myweb + user_alarm + palabras_claves
    language_filters = LanguageCampaign.objects.all().order_by('value_language')

    if request.user.id == None:
        
        user = User.objects.all().filter(pk=request.user.id)
        request_id = request.path.split('/')[2:-1]
        id_myweb =  ''.join(map(str, request_id))
        #Banner Slide
        banner_slide = return_slide()
        #-----------------------
        my_form = SearchFormProduct
        #IN LOGIN 
        language_select_act = translation.get_language()
        my_foot_banner = BannerIndex.objects.filter(activate=True,language__value_language=language_select_act).order_by('-date','-pk')
        my_foot_banner_count = BannerIndex.objects.filter(activate=True,language__value_language=language_select_act).count()
        return {'language_filters': language_filters, 'context': user,'next': request.GET.get('next'), 'id_myweb': id_myweb, 'banner_slide': banner_slide, 'my_form': my_form, 'language_selected': idlang, 'foot_banner': my_foot_banner, 'my_foot_banner_count': my_foot_banner_count,
        'palabras_claves': palabras_claves, 'user_alarm': user_alarm, 'notificaciones_myweb': notificaciones_myweb, 'task_pendientes': task_pendientes, 'total_notificaciones': total_notificaciones}
    else:
        actual_lang = translation.get_language()
        if actual_lang == 'es':
            idlang = 4
        elif actual_lang == 'de':
            idlang = 2
        elif actual_lang == 'en':
            idlang = 3
        elif actual_lang == 'fr':
            idlang = 5
        elif actual_lang == 'it':
            idlang = 6
        elif actual_lang == 'pt':
            idlang = 7
        elif actual_lang == 'zh-hans':
            idlang = 8
        elif actual_lang == 'ja':
            idlang = 9
        elif actual_lang == 'zh-hant':
            idlang = 1
        user = User.objects.all().filter(pk=request.user.id)
        contactscontext = Contacts.objects.values_list('relationship', flat=True).filter(owner=request.user)
        request_id = request.path.split('/')[2:-1]
        id_myweb =  ''.join(map(str, request_id))
        #Completed Registration
        registration = User.objects.all().filter(pk=request.user.id)
        profile_completed = False
        completed_registration = return_registration(registration)
        if completed_registration == 100:
            profile_completed = True
        #-----------------------
        #Banner Slide
        banner_slide = return_slide()
        #-----------------------
        #post info
        my_posts = Post.objects.filter(user=request.user.id).count()
        #--------------
        #score info
        my_user = User.objects.filter(id=request.user.id)
        my_score = my_user[0].score
        #--------------
        #contac info
        my_contacts = Contacts.objects.filter(owner=request.user.id, notification=True).count()
        #--------------
        #message info
        my_messages = Messages.objects.filter(receiver=request.user.id,read=False).count()
        my_messages_mailer = Messages.objects.filter(mailer=request.user.id,read_mailer=False).count()
        #chat info
        my_chats = ChatUser.objects.filter(receiver=request.user.id, read=False).count()
        chat_change = ChatUser.objects.filter(Q(receiver=request.user.id) | Q(mailer=request.user.id))
        #favorite info
        my_favorite = FavoriteProduct.objects.filter(user_id=request.user.id).count()

        counter_chat_change = 0
        for c in chat_change:
            extend_chat_change = ChatExtended.objects.filter(reference=c.id,read=False).exclude(mailer=request.user.id).count()
            counter_chat_change += extend_chat_change
        #jobs info
        my_jobs = 0
        my_job = Job.objects.filter(user=request.user.id)
        if my_job:
            for job in my_job:
                my_jobs += job.pending
        else:
            my_jobs = 0
        #Search Index
        my_form = SearchFormProduct
        
        if request.user.is_authenticated:
            user_active = UserOnline.objects.filter(user=request.user.id)
            #Editing
            if user_active:
                user_online_actual = UserOnline.objects.get(user=request.user.id)
                user_online_actual.active = True
                user_online_actual.save()
            #Creating
            else:
                user_actual = User.objects.get(id=request.user.id)
                new_active_user = UserOnline(user=user_actual,active=True)
                new_active_user.save()
        language_select_act = translation.get_language()
        my_foot_banner = BannerIndex.objects.filter(activate=True,language__value_language=language_select_act).order_by('-date', '-pk')
        my_foot_banner_count = BannerIndex.objects.filter(activate=True,language__value_language=language_select_act).count()
        url_to_banner = BannerUser.objects.filter(language__value_language=language_select_act)
        return {
            'language_filters': language_filters,
            'context': user,
            'contactscontext':contactscontext,
            'id_myweb': id_myweb,
            'completed_registration': completed_registration,
            'profile_completed': profile_completed,
            'banner_slide': banner_slide,
            'my_posts': my_posts,
            'my_score': my_score,
            'my_contacts': my_contacts,
            'my_form': my_form,
            'my_msgs': my_messages + my_messages_mailer,
            'my_chats': my_chats + counter_chat_change,
            'my_jobs': my_jobs,
            'language_selected': idlang,
            'foot_banner': my_foot_banner,
            'my_foot_banner_count': my_foot_banner_count,
            'banner_user': url_to_banner,
            'palabras_claves': palabras_claves,
            'user_alarm': user_alarm,
            'notificaciones_myweb': notificaciones_myweb,
            'task_pendientes': task_pendientes,
            'total_notificaciones': total_notificaciones,
            'my_favorite': my_favorite
        }


    