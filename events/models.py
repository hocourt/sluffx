from django.db                              import models
from django.utils                           import timezone
from users.models                           import Person

from django.contrib.auth.models             import User
from django.conf                            import settings
from django.contrib.auth                    import get_user_model
from django.urls                            import reverse


class Event(models.Model):
  #author                  = models.ForeignKey                             ('users.Person', related_name="author2", on_delete=models.CASCADE)
  #author                  = models.ForeignKey                             (User, related_name="author2", on_delete=models.CASCADE)
  author                  = models.ForeignKey                             (User, on_delete=models.CASCADE)
  e_date                  = models.DateField                              ('Date of the event, in the format "dd/mm/yy", e.g. for 31st December 2020, enter "31/12/20"', default=timezone.now, blank=True,null=True)
  detail_public           = models.CharField                              ('Title of event, this be shown publicly', max_length= 80, blank=True, default='')
  detail_private          = models.TextField                              ('Details of event', blank=True,null=True)
  notes                   = models.TextField                              (blank=True,null=True)
  attendees               = models.ManyToManyField                        (Person, related_name="bookedin2", blank=True)
  hosts                   = models.ManyToManyField                        (Person, related_name="hh2", blank=True)
  photo_cover             = models.ImageField                             (blank=True, null=True, upload_to='images/')
  created_date            = models.DateTimeField                          (default=timezone.now)
  last_modified           = models.DateTimeField                          (default=timezone.now)
  is_live                 = models.BooleanField                           (default=True)
  editable                = models.BooleanField                           (blank=True,null=True)
  def __str__(self):
    return self.detail_public

class Notice(models.Model):
  author                  = models.ForeignKey                             ('users.Person', related_name="authorn", on_delete=models.CASCADE)
  notice                  = models.TextField                              ('Notice', blank=True, null=True, default='')
  created_date            = models.DateTimeField                          (default=timezone.now)
  last_accessed           = models.DateTimeField                          (default=timezone.now)
  def __str__(self):
    return self.notice

class Amendment(models.Model):
  author                  = models.ForeignKey                             ('users.Person', related_name="authora", on_delete=models.CASCADE)
  event                   = models.ForeignKey                             ('events.Event', related_name="eventa", on_delete=models.CASCADE)
  notice                  = models.TextField                              ('Notice', blank=True, null=True, default='')
  amendment_date          = models.DateTimeField                          (default=timezone.now)
  last_accessed           = models.DateTimeField                          (default=timezone.now)
  def __str__(self):
    return self.id
