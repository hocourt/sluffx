#import datetime
from django.db                              import models
from django.utils                           import timezone

class Site(models.Model):
  private_site            = models.BooleanField       (default=True)
  daily                   = models.BooleanField       (default=False)
  club                    = models.BooleanField       (default=True)
  criterion4              = models.BooleanField       (default=True)
  criterion5              = models.BooleanField       (default=True)
  criterion6              = models.BooleanField       (default=True)
  advert                  = models.TextField          (blank=True, null=True)
  contact_info            = models.CharField          (max_length=200, blank=True, null=True)
  cover                   = models.ImageField         (blank=True, null=True, upload_to='images/')
  note                    = models.TextField          (blank=True, null=True)
  def __str__(self):
    return str(self.contact_info)

class Photo(models.Model):
  author                  = models.ForeignKey         ('users.Person', related_name="authorp", on_delete=models.CASCADE, null=True)
  priority                = models.IntegerField       (default=100)
  is_live                 = models.BooleanField       (default=True)
  title                   = models.TextField          (blank=True, null=True)
  cover                   = models.ImageField         (blank=True, null=True, upload_to='images/')
  editable                = models.BooleanField       (default=False)
  created_date            = models.DateTimeField      (blank=True, null=True, default=timezone.now)
  def __str__(self):
    return self.title

class EnquiryB(models.Model):
  author                  = models.ForeignKey         ('users.Person', related_name="authory", on_delete=models.CASCADE, null=True)
  priority                = models.IntegerField       (default=100)
  is_live                 = models.BooleanField       (default=True)
  title                   = models.TextField          (blank=True, null=True)
  content                 = models.TextField          (blank=True, null=True)
  created_date            = models.DateTimeField      (blank=True, null=True, default=timezone.now)
  def __str__(self):
    return self.title

"""
class Note(models.Model):
    content               = models.TextField          (null=True)
  created_date            = models.DateTimeField      (blank=True, null=True, default=timezone.now)
  published_date          = models.DateTimeField      (blank=True, null=True)
  def publish(self):
    self.published_date = timezone.now()
    self.save()
  datecolor               = models.CharField          (max_length=20, default='black')
  detailcolor             = models.CharField          (max_length=20, default='#0000C0')
  attendeescolor          = models.CharField          (max_length=20, default='#00C000')
  backgroundcolor         = models.CharField          (max_length=20, default='#F3FFF3')

class Enquiry(models.Model):
    is_live               = models.BooleanField       (default=True)
    content               = models.TextField          (null=True)
    created_date          = models.DateTimeField      (blank=True, null=True, default=timezone.now)

class Enquiry(models.Model):
  author                  = models.ForeignKey         ('users.Person', related_name="authorx", on_delete=models.CASCADE, null=True)
  priority                = models.IntegerField       (default=100)
  is_live                 = models.BooleanField       (default=True)
  title                   = models.TextField          (blank=True, null=True)
  content                 = models.TextField          (blank=True, null=True)
  created_date            = models.DateTimeField      (blank=True, null=True, default=timezone.now)
  def __str__(self):
    return self.title
"""

class Response(models.Model):
    is_live               = models.BooleanField       (default=True)
    content               = models.TextField          (null=True)
    author                = models.ForeignKey         ('users.Person', related_name="authorq", on_delete=models.CASCADE, null=True)
    sent_date             = models.DateTimeField      (blank=True, null=True, default=timezone.now)
