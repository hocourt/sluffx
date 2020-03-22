from django.shortcuts               import render, get_object_or_404, redirect
from django.utils                   import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models     import User
from users.models                   import Person
from mysite.models                  import Site, Photo
from .models                        import Event,Notice,Amendment
from .forms                         import EventForm, HostForm, AttendeeForm, NoticeForm
from mysite.settings                import TITLE

from django.views.generic           import CreateView
from django.views.generic           import UpdateView
from django.views.generic           import DeleteView
from django.urls                    import reverse_lazy

"""
class EventList(ListView):
    model                       = Event
    context_object_name         = 'events'
    template_name               = 'event_list_b.html'
"""

#@login_required
class EventInsert(CreateView):
    model                       = Event
    form_class                  = EventForm
    template_name               = 'events/event_insert_update.html'
    success_url                 = reverse_lazy('homepage')
    def form_valid(self, form):
      form.instance.author      = self.request.user
      return super(EventInsert, self).form_valid(form)

#@login_required
class EventUpdate(UpdateView):
    model                       = Event
    form_class                  = EventForm
    template_name               = 'events/event_insert_update.html'
    success_url                 = reverse_lazy('homepage')

class EventDelete(DeleteView):
    model                       = Event
    form_class                  = EventForm
    template_name               = 'events/event_delete.html'
    success_url                 = reverse_lazy('homepage')


# functions which do not update the database
# and don't require a pk as they don't refer to an specific record
def event_list(request, periodsought='current'):

    if periodsought == 'current':
        events = Event.objects.filter(is_live=True, e_date__gte=timezone.now()).order_by('e_date')
    else:
        events = Event.objects.exclude(is_live=True, e_date__gte=timezone.now()).order_by('-e_date')

    site                                            =  get_object_or_404(Site)
    notice                                    =  get_object_or_404(Notice).notice
    #if request.user.is_authenticated():
    if request.user.is_authenticated == True:
        activeuser                          = User.objects.get(id=request.user.id)
        activeperson                        = Person.objects.get(username=activeuser.username)
        activeperson.last_login             = timezone.now()
        activeperson.save()
    else:
        activeperson                        = Person.objects.get(username='notloggedin')
        activeuser                          = User.objects.get(username=activeperson.username)

    events_augmented = []
    #stored_event_date = '2000-01-01'
    for event in events:

        hosts_list = []
        for host in event.hosts.all():
            hosts_list.append(host.display_name)
        hosts_string   = ', '.join(hosts_list)

        attendees_list = []
        for attendee in event.attendees.all():
            attendees_list.append(attendee.display_name)
        attendees_string   = ', '.join(attendees_list)

        if activeperson.status                   >=  40                         \
        or event.author                          ==  activeuser                 \
        or activeperson in event.hosts.all():
            event.editable                       =   True
        else:
            event.editable                       =   False

        if event.e_date                          <  timezone.localtime(timezone.now()).date():
          event_status_now                       =  'past'
        elif event.is_live                       == True:
          event_status_now                       =  'live'
        else:
          event_status_now                       = 'deletednonpast'

        amendments_list                          = []
        amendments                               = Amendment.objects.filter(event=event)
        for amendment in amendments:
          amendment_person                       = Person.objects.get(id=amendment.author_id)
          amendment_augmented                    = {'id': amendment.id, 'name':amendment_person.display_name,'date':amendment.amendment_date}
          #amendments_list.append(amendment_person.display_name)
          amendments_list.append(amendment_augmented)
        #amendments_string                        = ', '.join(amendments_list)

        event_augmented = \
        {"event":event, "attendees":attendees_string, "hosts":hosts_string, \
        'event_status_now': event_status_now, 'first_insert': amendments_list[0:1], 'amendments': amendments_list[1:]}
        events_augmented.append(event_augmented)
    photos 									= Photo.objects.filter(is_live=True).order_by('-priority')
    context = {'events': events_augmented, 'periodsought':periodsought, 'activeperson': activeperson, 'TITLE': TITLE, \
	    'site': site, 'notice': notice, 'photos' : photos, 'logged_in' : request.user.is_authenticated}
    return render(request, 'events/event_list.html', context)


# functions which do not update the database
# but do require a pk as they refer to an existing record
@login_required
def event_detail(request, pk):
  event                                 =  get_object_or_404(Event, pk=pk)     # get details of event to be updated/displayed/deleted

  if event.e_date                     <  timezone.localtime(timezone.now()).date():
    event_status_now                      =  'past'
  elif event.is_live                      == False:
    event_status_now                      =  'deletednonpast'
  else:
    event_status_now                      =  'live'

  persons_list = []
  for person in event.attendees.all():
    persons_list.append(person.display_name)
  persons_string   = ', '.join(persons_list)
  return render(request, 'events/event_detail.html', {'event': event, 'event_status_now': event_status_now, 'persons':persons_string, 'TITLE':TITLE})


# functions which update the database using parameters in the url, without using forms
# but do not require a pk
#        None. All require a pk to specify the event.

# functions which update the database using parameters in the url, without using forms
# and do require a pk to specify the event.
@login_required
def event_delete(request, pk):
  event                                     = get_object_or_404(Event, pk=pk)
  if event.e_date                         < timezone.localtime(timezone.now()).date():
    periodsought                          = 'notcurrent'
  else:
    periodsought                          = 'current'
  event.is_live                         = False
  event.save()
  return redirect('eventlist', periodsought)

@login_required
def event_deleteperm(request, pk):
  event                                     = get_object_or_404(Event, pk=pk)
  if event.e_date                         < timezone.localtime(timezone.now()).date():
    periodsought                          = 'notcurrent'
  else:
    periodsought                          = 'current'
  amendments                               = Amendment.objects.filter(event=event)
  for x in amendments:
    x.delete()
  event.delete()

  return redirect('eventlist', periodsought)

@login_required
def bookinto(request, pk):
  event                                     = get_object_or_404(Event, pk=pk)
  if event.e_date                         < timezone.localtime(timezone.now()).date():
    periodsought                          = 'notcurrent'
  else:
    periodsought                          = 'current'
  activeuser = User.objects.get(id=request.user.id)        #(username = request.user)
  updated_attendee = Person.objects.get(username=activeuser.username)        #(username = request.user)
  event.attendees.add(updated_attendee)
  event.save()
  return redirect('eventlist', periodsought)

@login_required
def leave(request, pk):
  event                                     = get_object_or_404(Event, pk=pk)
  if event.e_date                         < timezone.localtime(timezone.now()).date():
    periodsought                          = 'notcurrent'
  else:
    periodsought                          = 'current'
  activeuser = User.objects.get(id=request.user.id)        #(username = request.user)
  updated_attendee = Person.objects.get(username=activeuser.username)        #(username = request.user)
  event.attendees.remove(updated_attendee)
  event.save()
  return redirect('eventlist', periodsought)


@login_required
def restore(request, pk):
  event                                     = get_object_or_404(Event, pk=pk)
  if event.e_date                         < timezone.localtime(timezone.now()).date():
    periodsought                          = 'notcurrent'
  else:
    periodsought                          = 'current'
  event.is_live                         = True
  event.save()
  return redirect('eventlist', periodsought)


# functions which update the database in two stages,  using forms
# but don't require a pk as they don't refer to an existing record
"""
@login_required
def event_insert(request):
  activeuser                                  =  User.objects.get(id=request.user.id)
  activeperson                                =  Person.objects.get(username=activeuser.username)
  if request.method                           != 'POST':
    form = EventForm()
    return render(request, 'events/insert_update.html', {'form': form})                   # ask user for event details
  else:
    form = EventForm(request.POST)
    if form.is_valid():
      event                                   = form.save(commit=False)
      if event.e_date                         < timezone.localtime(timezone.now()).date():
        error_message                         = 'event date cannot be in the past, please enter a valid date'
        return render(request, 'events/insert_update.html', {'form': form, 'error_message': error_message})
                                              # events cannot be posted for dates in past
      else:
        periodsought                          = 'current'
      activeperson_status                     =  0
      if request.user.is_authenticated == True:
        activeuser                          =  User.objects.get(id=request.user.id)
        activeperson_status                 =  20
        try:
          activeperson                    = Person.objects.get(username=activeuser.username)
          activeperson_status             = activeperson.status
        except:
          pass
      if activeperson_status                >= 30:
        #event.author_name                     = activeperson.username
        event.author                          = activeperson
        updated_host                      = Person.objects.get(username=activeuser.username)        #(username = request.user)
        event.save()
        event.hosts.add(updated_host)
        event.save()
        amendment = Amendment(event=event, author=activeperson)
        amendment.save()
        form.save_m2m()
        return redirect('eventlist', periodsought)
      else:
        return render(request, 'events/insert_update.html', {'form': form})
    else:                                                                                  # i.e. form is not valid, ask user to resubmit it
      return render(request, 'events/insert_update.html', {'form': form})

# functions which update the database in two stages,  using forms
# and do require a pk as they refer to an existing record

@login_required
def event_update(request, pk):
  activeuser                                  =  User.objects.get(id=request.user.id)
  activeperson                                =  Person.objects.get(username=activeuser.username)
  event                                     = get_object_or_404(Event, pk=pk)
  event_saved                                     = get_object_or_404(Event, pk=pk)                           # change 1006
                                              # i.e. function in ['detail', 'update', 'repeat',
                                              #'restore', 'bookinto', 'leave', 'delete', 'deleteperm']
  if request.method                           != 'POST':
    form = EventForm(instance=event)
    return render(request, 'events/insert_update.html', {'form': form})                   # ask user for event details
  else:
    form = EventForm(request.POST, instance=event)
    if form.is_valid():
      event                                   = form.save(commit=False)
      if event.e_date                         < timezone.localtime(timezone.now()).date():
        error_message                         = 'event date cannot be in the past, please enter a valid date'
        return render(request, 'events/insert_update.html', {'form': form, 'error_message': error_message})
                                              # events cannot be posted for dates in past
      else:
        periodsought                          = 'current'
      activeperson_status                     =  0
      if request.user.is_authenticated == True:
        activeuser                          =  User.objects.get(id=request.user.id)
        activeperson_status                 =  20
        try:
          activeperson                    = Person.objects.get(username=activeuser.username)
          activeperson_status             = activeperson.status
        except:
          pass
# change 1006
      if event.e_date                  == event_saved.e_date                     \
      and event.detail_public              == event_saved.detail_public          \
      and event.detail_private             == event_saved.detail_private:
        return redirect('eventlist', periodsought)
        #return redirect('memberlist')
      else:
        if activeperson_status                   >=  40                         \
        or event.author                          ==  activeuser                 \
        or activeperson in event.hosts.all():
          amendment = Amendment(event=event, author=activeperson)
          event.save()
          amendment.save()
          form.save_m2m()
          return redirect('eventlist', periodsought)
        else:
          return render(request, 'events/insert_update.html', {'form': form})
    else:                                                                                  # i.e. form is not valid, ask user to resubmit it
      return render(request, 'events/insert_update.html', {'form': form})
"""

@login_required
def hosts_update(request, pk):
  activeuser                                  =  User.objects.get(id=request.user.id)
  activeperson                                =  Person.objects.get(username=activeuser.username)
  event                                     = get_object_or_404(Event, pk=pk)

  if request.method                           != 'POST':
    form = HostForm(instance=event)
    return render(request, 'events/event_insert_update.html', {'form': form})                   # ask user for event details
  else:
    form = HostForm(request.POST, instance=event)
    if form.is_valid():
      event                                   = form.save(commit=False)
      if event.e_date                         < timezone.localtime(timezone.now()).date():
        error_message                         = 'event date cannot be in the past, please enter a valid date'
        return render(request, 'events/event_insert_update.html', {'form': form, 'error_message': error_message})
                                              # events cannot be posted for dates in past
      else:
        periodsought                          = 'current'

      activeperson_status                     =  0

      if request.user.is_authenticated == True:
        activeuser                          =  User.objects.get(id=request.user.id)
        try:
          activeperson                    = Person.objects.get(username=activeuser.username)
          activeperson_status             = activeperson.status
        except:
          pass

      if activeperson_status                   >=  40                         \
      or event.author                          ==  activeuser                 \
      or activeperson in event.hosts.all():
        event.save()
        form.save_m2m()
        return redirect('eventlist', periodsought)
      else:
        return render(request, 'events/event_insert_update.html', {'form': form})
    else:                                                                                  # i.e. form is not valid, ask user to resubmit it
      return render(request, 'events/event_insert_update.html', {'form': form})

@login_required
def attendees_update(request, pk):
  activeuser                                  =  User.objects.get(id=request.user.id)
  activeperson                                =  Person.objects.get(username=activeuser.username)
  event                                     = get_object_or_404(Event, pk=pk)

  if request.method                           != 'POST':
    form = AttendeeForm(instance=event)
    return render(request, 'events/event_insert_update.html', {'form': form})                   # ask user for event details
  else:
    form = AttendeeForm(request.POST, instance=event)
    if form.is_valid():
      event                                   = form.save(commit=False)
      if event.e_date                         < timezone.localtime(timezone.now()).date():
        error_message                         = 'event date cannot be in the past, please enter a valid date'
        return render(request, 'events/event_insert_update.html', {'form': form, 'error_message': error_message})                                            # events cannot be posted for dates in past
      else:
        periodsought                          = 'current'

      activeperson_status                     =  0

      if request.user.is_authenticated == True:
        activeuser                          =  User.objects.get(id=request.user.id)
        activeperson_status                 =  20
        try:
          activeperson                    = Person.objects.get(username=activeuser.username)
          activeperson_status             = activeperson.status
        except:
          pass
      if activeperson_status                   >=  40                         \
      or event.author                          ==  activeuser                 \
      or activeperson in event.hosts.all():
        event.save()
        form.save_m2m()
        return redirect('eventlist', periodsought)
      else:
        return render(request, 'events/event_insert_update.html', {'form': form})
    else:                                                                                  # i.e. form is not valid, ask user to resubmit it
      return render(request, 'events/event_insert_update.html', {'form': form})


@login_required
def event_repeat(request, pk):
  activeuser                                  =  User.objects.get(id=request.user.id)
  activeperson                                =  Person.objects.get(username=activeuser.username)
  event                                     = get_object_or_404(Event, pk=pk)

  if request.method                           != 'POST':
    form = EventForm(instance=event)
    return render(request, 'events/event_insert_update.html', {'form': form})                   # ask user for event details
  else:
    form                                    = EventForm(request.POST)
    form_original                           = EventForm(request.POST, instance=event)
    if form_original.is_valid():
      event_original                          = form_original.save(commit=False)


    if form.is_valid():
      event                                   = form.save(commit=False)
      if event.e_date                         < timezone.localtime(timezone.now()).date():
        error_message                         = 'event date cannot be in the past, please enter a valid date'
        return render(request, 'events/insert_update.html', {'form': form, 'error_message': error_message})
                                              # events cannot be posted for dates in past
      else:
        periodsought                          = 'current'
      activeperson_status                     =  0
      if request.user.is_authenticated == True:
        activeuser                          =  User.objects.get(id=request.user.id)
        activeperson_status                 =  20
        try:
          activeperson                    = Person.objects.get(username=activeuser.username)
          activeperson_status             = activeperson.status
        except:
          pass
      if activeperson_status                   >=  40                         \
      or event_original.author                 ==  activeuser                 \
      or activeperson in event_original.hosts.all():
        event.author_name                     = activeuser.username
        event.author                          = activeperson
        updated_host                          = Person.objects.get(username=activeuser.username)        #(username = request.user)
        event.save()
        event.hosts.add(updated_host)
        event.save()
        form.save_m2m()
        return redirect('eventlist', periodsought)
      else:
        return render(request, 'events/event_insert_update.html', {'form': form})
    else:                                                                                  # i.e. form is not valid, ask user to resubmit it
      return render(request, 'events/event_insert_update.html', {'form': form})

@login_required
def notice_update(request):
  activeuser                                  =  User.objects.get(id=request.user.id)
  activeperson                                =  Person.objects.get(username=activeuser.username)
  #notice                                    = get_object_or_404(N, pk=pk)
  notice                                    = Notice.objects.get()
  if request.method                           == 'POST':
    form = NoticeForm(request.POST, instance=notice)
    if form.is_valid():
      notice                                   = form.save(commit=False)
      activeperson_status                     =  0
      if request.user.is_authenticated == True:
        activeuser                          =  User.objects.get(id=request.user.id)
        activeperson_status                 =  20
        try:
          activeperson                    = Person.objects.get(username=activeuser.username)
          activeperson_status             = activeperson.status
        except:
          pass
      if activeperson_status                   >=  40:
        notice.save()
        form.save_m2m()
        return redirect('eventlist', 'current')
      else:
        return render(request, 'events/notice_update.html', {'form': form})
    else:                                                                                  # i.e. form is not valid, ask user to resubmit it
      return render(request, 'events/notice_update.html', {'form': form})
  else:
    form = NoticeForm(instance=notice)
    return render(request, 'events/notice_update.html', {'form': form})                   # ask user for event details

@login_required
def notice_delete(request):
  notice                                    = Notice.objects.get()
  notice.notice = ""
  notice.save()
  return redirect('eventlist', 'current')
