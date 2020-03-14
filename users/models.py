#import datetime
from django.db                              import models
from django.utils                           import timezone
#from django.contrib.auth.models            import User
"""
class Branch(models.Model):
  username                = models.CharField          (max_length=20, unique=True, blank=True, null=True)
  display_name            = models.CharField          (max_length=30, unique=True)
  twitter_name            = models.CharField          (max_length=40, blank=True, null=True)
  email                   = models.CharField          (max_length=40, blank=True, null=True)
  phone_a                 = models.CharField          (max_length=15, blank=True, null=True)
  phone_b                 = models.CharField          (max_length=15, blank=True, null=True)
  password                = models.CharField          (max_length=30, blank=True, null=True)
  status                  = models.IntegerField       (default=38)
  #authorname              = models.CharField          (max_length=20,blank = True, null = True)
  reversevideo            = models.BooleanField       (default=False)
  datecolor               = models.CharField          (max_length=20, default='black')
  detailcolor             = models.CharField          (max_length=20, default='#0000C0')
  attendeescolor          = models.CharField          (max_length=20, default='#00C000')
  backgroundcolor         = models.CharField          (max_length=20, default='#F3FFF3')
  datecolor_rev           = models.CharField          (max_length=20, default='white')
  detailcolor_rev         = models.CharField          (max_length=20, default='aqua')
  attendeescolor_rev      = models.CharField          (max_length=20, default='lawngreen')
  backgroundcolor_rev     = models.CharField          (max_length=20, default='black')
  photo_cover             = models.ImageField         (null=True, upload_to='images/')
  notes                   = models.TextField          (blank=True, null=True)
  #logged_in               = models.BooleanField       (default=False)
  last_login              = models.DateTimeField      (blank = True, null = True)
  last_logout             = models.DateTimeField      (blank = True, null = True)
  last_visited            = models.DateTimeField      (blank = True, null = True)
  created_date            = models.DateTimeField      (default=timezone.now)
  published_date          = models.DateTimeField      (blank=True, null=True)
  class Meta:
    ordering = ['username']
  def publish(self):
    self.published_date = timezone.now()
    self.save()
  def __str__(self):
    return str(self.display_name)
"""

class Person(models.Model):
  STATUSES = (
        (8, 'Contact'),
        (10, 'Public'),
        (15, 'Prospective'),
        (20, 'Member'),
        (30, 'Planner'),
        #(35, 'Introducer'),
        (40, 'Committee'),
        (50, 'Treasurer'),
        (55, 'WebManager'),
        (60, 'Admin'),
  )
  username                = models.CharField                 (max_length=20, unique=True, blank=True, null=True)
  email                   = models.EmailField                (max_length=40, unique=True, blank=True, null=True)
  display_name            = models.CharField                 (max_length=30, unique=True)
  authorname              = models.CharField                 (max_length=20,blank = True, null = True)
  meetup_name             = models.CharField                 (max_length=40, blank=True, null=True)
  twitter_name            = models.CharField                 (max_length=40, blank=True, null=True)
  phone_a                 = models.CharField                 (max_length=20, blank=True, null=True)
  phone_b                 = models.CharField                 (max_length=20, blank=True, null=True)
  password                = models.CharField                 (max_length=30, blank=True, null=True)
  fullmember              = models.BooleanField              (default=False)
  status                  = models.IntegerField              (default=15, choices=STATUSES)
  #status                  = models.IntegerField              (default=15)
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
  logged_in               = models.BooleanField              (default=False)
  last_login              = models.DateTimeField             (blank = True, null = True)
  last_logout             = models.DateTimeField             (blank = True, null = True)
  last_visited            = models.DateTimeField             (blank = True, null = True)
  created_date            = models.DateTimeField             (default=timezone.now)
  published_date          = models.DateTimeField             (blank=True, null=True)
  class Meta:
        ordering = ['username']
  def publish(self):
    self.published_date = timezone.now()
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
    def publish(self):
        self.received_date = timezone.now()
        self.save()
    def __str__(self):
        return str(self.sender)
