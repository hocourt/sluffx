#import datetime
from django.db                              import models
from django.utils                           import timezone
#from django.contrib.auth.models            import User

class Person(models.Model):
  STATUSES = (
        (5, 'Contact'),
        (10, 'Public'),
        (15, 'Prospective'),
        (30, 'Member'),
        (40, 'Committee'),
        (50, 'Treasurer'),
        (60, 'Chair'),
  )
  username                = models.CharField                 (max_length=20, unique=True, blank=True, null=True)
  email                   = models.EmailField                (max_length=40, unique=True, blank=True, null=True)
  display_name            = models.CharField                 (max_length=30, unique=True)
  authorname              = models.CharField                 (max_length=20,blank = True, null = True)
  twitter_name            = models.CharField                 (max_length=40, blank=True, null=True)
  phone_a                 = models.CharField                 (max_length=20, blank=True, null=True)
  phone_b                 = models.CharField                 (max_length=20, blank=True, null=True)
  password                = models.CharField                 (max_length=30, blank=True, null=True)
  status                  = models.IntegerField              (default=15, choices=STATUSES)
  reversevideo            = models.BooleanField              (default=False)
  datecolor               = models.CharField                 (max_length=20, default='black')
  detailcolor             = models.CharField                 (max_length=20, default='#0000C0')
  attendeescolor          = models.CharField                 (max_length=20, default='#00C000')
  backgroundcolor         = models.CharField                 (max_length=20, default='#F3FFF3')
  datecolor_rev           = models.CharField                 (max_length=20, default='white')
  detailcolor_rev         = models.CharField                 (max_length=20, default='aqua')
  attendeescolor_rev      = models.CharField                 (max_length=20, default='lawngreen')
  backgroundcolor_rev     = models.CharField                 (max_length=20, default='black')
  cover                   = models.ImageField                (blank=True, null=True, upload_to='images/')
  notes                   = models.TextField                 (blank=True, null=True)
  last_login_date         = models.DateTimeField             (blank = True, null = True)
  last_logout_date        = models.DateTimeField             (blank = True, null = True)
  created_date            = models.DateTimeField             (default=timezone.now)
  class Meta:
        ordering = ['username']
  def create(self):
    self.created_date = timezone.now()
    self.save()
  def __str__(self):
    return str(self.display_name)

class Message(models.Model):
    sender                = models.CharField          (max_length=20)
    recipient             = models.CharField          (max_length=20)
    sent_date             = models.DateTimeField      (blank=True, null=True, default=timezone.now)
    received_date         = models.DateTimeField      (blank=True, null=True)
    is_live_sender        = models.BooleanField       (default=True)
    is_live_recipient     = models.BooleanField       (default=True)
    content               = models.TextField          (blank=True, null=True)
    class Meta:
        ordering = ['sent_date']
    def sent(self):
        self.sent_date = timezone.now()
        self.save()
    def received (self):
        self.received_date  = timezone.now()
        self.save()
    def __str__(self):
        return str(self.sender)
