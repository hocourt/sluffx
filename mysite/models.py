#import datetime
from django.db                              import models
from django.utils                           import timezone

class Sitesettings(models.Model):
  private_site            = models.BooleanField       (default=True)
  advert                  = models.TextField          (blank=True, null=True)
  contact_info            = models.CharField          (max_length=200, blank=True, null=True)
  status                  = models.IntegerField       ()
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
  created_date            = models.DateTimeField      (blank=True, null=True, default=timezone.now)
  published_date          = models.DateTimeField      (blank=True, null=True)
  def publish(self):
    self.published_date = timezone.now()
    self.save()
  def __str__(self):
    return str(self.contact_info)

class Photo(models.Model):
  author                  = models.ForeignKey         ('users.Person', related_name="authorp", on_delete=models.CASCADE, null=True)
  priority                = models.IntegerField       (default=100)
  is_live                 = models.BooleanField       (default=True)
  title                   = models.TextField          (null=True)
  cover                   = models.ImageField         (null=True, upload_to='images/')
  created_date            = models.DateTimeField      (blank=True, null=True, default=timezone.now)
  def __str__(self):
    return self.title

class Note(models.Model):
  note_content            = models.TextField          (null=True)



