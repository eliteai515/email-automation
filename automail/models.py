from typing import Iterable, Optional
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

from encrypted_model_fields.fields import EncryptedCharField, EncryptedEmailField

from user.models import User

domain_name_validator = RegexValidator(regex='^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9](?:\.[a-zA-Z]{2,})+$')

class EMAIL_SEND_RULES(models.IntegerChoices):

    """
        These rules determine how the follow up messages should be sent, eg: if ALL is set as
        rule the follow up will be sent to everyone to whom the first mail was sent.
    """

    ALL = (0, 'Respond for all')    
    NOT_RESPONDED = (1, 'Reply for not responded')
    RESPONDED = (2, 'Reply for responded')


class EmailConfiguration(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=40, null=True, blank=True)

    host = models.CharField(max_length=255)
    use_ssl = models.BooleanField(default=True)
    port = models.SmallIntegerField(default=465) # use ssl port

    imap_host = models.CharField(max_length=255, default='')

    email = EncryptedEmailField()
    password = EncryptedCharField(max_length=100)

    signature = models.TextField(null=True, blank=True, max_length=400)
    
    is_verified = models.BooleanField(default=False) # if the added email has been 

    def __str__(self) -> str:
        return f'{self.email}'

class EmailTemplate(models.Model):

    name = models.CharField(max_length=50, default="Sample Template")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    subject = models.CharField(max_length=250, null=True, blank=True)

    body = models.TextField(max_length=10000)
    datetime = models.DateTimeField(auto_now=True)

    variables = models.TextField(max_length=2000, null=True, blank=True) # variables in the email structure, stored seperated by a comma

    public = models.BooleanField(default=False) # is this template public template

    copy_count = models.PositiveIntegerField(default=0) # this keeps a track of number copies of this template made

    def __str__(self) -> str:
        return f'{self.subject[:30]} #{self.pk}'
    

class EmailTemplateAttachment(models.Model):

    template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='attachments/')

    def __str__(self) -> str:
        return self.template.subject[:30]


class EmailCampaign(models.Model):

    name = models.CharField(max_length=30, default='campaign', null=True, blank=True)

    email_lookup = models.CharField(default='Email', max_length=150) # this is the field lookup upon uploading xls sheet
    created_datetime = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    file = models.FileField(upload_to='email-files/')
    save_to_inbox = models.BooleanField(default=True)
    discontinued = models.BooleanField(default=False) # if there are too many errors related to campaign discontinue the campaign

    def __str__(self) -> str:
        return f'{self.name}'
    

class EmailCampaignTemplate(models.Model):

    email = models.ForeignKey(EmailConfiguration, on_delete=models.CASCADE)
    campaign = models.ForeignKey(EmailCampaign, on_delete=models.CASCADE)
    template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE)

    followup =  models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    email_send_rule = models.PositiveSmallIntegerField(choices=EMAIL_SEND_RULES.choices, default=EMAIL_SEND_RULES.ALL, null=True)
    
    completed = models.BooleanField(default=False)

    created_datetime = models.DateTimeField(auto_now=True)
    sent_count = models.PositiveIntegerField(default=0)

    failed_count = models.PositiveIntegerField(default=0)
    failed_emails = models.TextField(max_length=4000, default='', null=True, blank=True) 
    error = models.TextField(max_length=4000, null=True, blank=True)
    smtp_error_count = models.PositiveIntegerField(default=0) 

    schedule = models.DateTimeField(null=True, blank=True)
    scheduled = models.BooleanField(default=False)
    
    created_datetime = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f'{self.campaign.name}'

class BlacklistedEmailDomains(models.Model):

    """
        commonly known blacklisted email domains
    """

    domain = models.CharField(validators=[RegexValidator], max_length=255)