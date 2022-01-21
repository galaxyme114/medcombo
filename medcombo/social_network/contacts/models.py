from django.db import models
from medcombo.configuration.usercustom.models import User
from medcombo.product.models import Product

def chat_attach_file(instance, filename):
    return 'chat/{1}'.format(instance, filename)

class Contacts(models.Model):
    relationship = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name = 'owner_contact')
    favorite= models.BooleanField(default=False)
    notification = models.BooleanField(default=False)

    def __str__(self):
        return self.relationship.username

class Message(models.Model):
    mailer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name = 'owner_message')
    receiver = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    subject = models.CharField(max_length=150, null=True)
    message = models.CharField(max_length=250, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modifiedd = models.DateTimeField(auto_now_add=True)
    removed = models.BooleanField(default=False)
    removed_receiver = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    read_mailer = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.CharField(max_length=12, null=True)
    important = models.BooleanField(default=False)
    
    def __str__(self):
        return self.subject

class MessageExtended(models.Model):
    reference = models.ForeignKey(Message, on_delete=models.CASCADE, blank=True, null=True, related_name='referenced')
    created = models.DateTimeField(auto_now_add=True)
    modifiedd = models.DateField(auto_now_add=True)
    message = models.CharField(max_length=250, null=True)
    mailer = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'the_mailer', blank=True, null=True)

    def __str__(self):
        return self.message

class ChatUser(models.Model):
    mailer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name = 'owner_chat')
    receiver = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    subject = models.CharField(max_length=150, null=True, blank=True)
    message = models.CharField(max_length=250, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    removed = models.BooleanField(default=False)
    removed_receiver = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    read_mailer = models.BooleanField(default=False)
    pin = models.IntegerField(blank=True, null=True)
    block = models.BooleanField(default=False)
    mute = models.BooleanField(default=False)

    def __str__(self):
        return self.message

class ChatAttach(models.Model):
    name = models.CharField(max_length=250, blank=True)
    file = models.FileField(upload_to=chat_attach_file, blank=True)
    def __str__(self):
        return self.name
    def extension(self):
        return self.name.split('.')[1]

class ChatExtended(models.Model):
    reference = models.ForeignKey(ChatUser, on_delete=models.CASCADE, blank=True, null=True, related_name='chat_reference')
    created = models.DateTimeField(auto_now_add=True)
    modifiedd = models.DateField(auto_now_add=True)
    message = models.CharField(max_length=250, null=True)
    attach = models.ForeignKey(ChatAttach, on_delete=models.CASCADE, related_name = 'chat_attach', blank=True, null=True)
    mailer = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'chat_mailer', blank=True, null=True)
    read = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    active_mailer = models.BooleanField(default=True)

    def __str__(self):
        return self.message