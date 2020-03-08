from django.shortcuts               import render, get_object_or_404, redirect
from django.utils                   import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models     import User
from mysite.models                  import Sitesettings
from .models                        import Person
from .models                        import Branch
from .forms                         import UpdateMemberForm, UserOptionsForm, InsertMemberForm, InsertContactForm, PasswordForm, DisplaynameForm

    #status == 05      is a contact, not a member, does not have a login and can only be added to an event by a member
    #status == 10      can view event dates and titles. This is only used for user 'default', which is someone viewing the site without logging in
    #status == 15      also can view event details. This can be used for 'default' user on some sites. May also be used for some logged in users.
    #status == 20      also can book into and out of events
    #status == 30      also can put events on the programme and update/delete their own events
    #status == 35      also can add members
    #status == 38      branch.
    #status == 40      also can view more user details and update/delete any event
    #status == 50      also can change whether fullmember
    #status == 60      also can remove members and make any update

# functions which do not update the database
@login_required
def member_list(request):
  sitesettings                                    =  get_object_or_404(Sitesettings)
  if request.user.is_authenticated == True:
      activeuser                          = User.objects.get(id=request.user.id)
      activeperson                        = Person.objects.get(username=activeuser.username)
      activeperson.last_visited           = timezone.now()
      activeperson.save()
      logged_in                           = True
  else:
      activeperson                        = sitesettings
      logged_in                           = False
  persons                                 =  Person.objects.filter(status=20).order_by('display_name')
  return render(request, 'users/member_list.html', {'persons': persons, 'activeperson': activeperson, 'logged_in': logged_in })


@login_required
def member_detail(request, pk):
  activeuser                            =  User.objects.get(id=request.user.id)
  activeperson                          =  Person.objects.get(username=activeuser.username)
  person                                =  get_object_or_404(Person, pk=pk)     # get details of person to be updated/displayed/deleted
  return render(request, 'users/member_detail.html', {'person': person, 'activeperson': activeperson})

@login_required
def branch_list(request):
  sitesettings                                    =  get_object_or_404(Sitesettings)
  if request.user.is_authenticated == True:
      activeuser                          = User.objects.get(id=request.user.id)
      activeperson                        = Person.objects.get(username=activeuser.username)
      activeperson.last_visited           = timezone.now()
      activeperson.save()
      logged_in                           = True
  else:
      activeperson                        = sitesettings
      logged_in                           = False
  branches                                 =  Person.objects.filter(status=38).order_by('display_name')
  return render(request, 'users/branch_list.html', {'branches': branches, 'activeperson': activeperson, 'logged_in': logged_in })



# functions which update the database using parameters in the url, without using forms
# but do not require a pk as they refer to activeuser
@login_required
def unsubscribe(request, confirmed):
  if confirmed                 == 'no':
    return render(request, 'users/unsubscribe.html', {})
  else:
    activeuser                 =  User.objects.get(id=request.user.id)    # get details of activeuser
    activeperson               =  Person.objects.get(username=activeuser.username)
    activeuser.delete()
    activeperson.delete()
    unsubscribed               =  True
    return render(request, 'users/unsubscribe_confirmed.html', {'unsubscribed': unsubscribed})
    #return redirect('django.contrib.auth.views.logout')

# functions which update the database using parameters in the url, without using form
# and do require a pk as they refer to a user who is not, generally, the activeuser
@login_required
def member_delete(request, pk, confirmed):
  if confirmed                 == 'no':
    return render(request, 'users/member_delete.html', {'pk': pk})
  else:
    activeuser                 =  User.objects.get(id=request.user.id)    # get details of activeuser
    activeperson               =  Person.objects.get(username=activeuser.username)
    person                     =  get_object_or_404(Person, pk=pk)     # get details of person to be updated/displayed/deleted
    if activeperson.status     >= 60                              \
    or person.authorname       == activeperson.username:
      person.delete()
      try:
        User.objects.get(username=person.username).delete()
      except:
        pass
    return redirect('memberlist')

@login_required
def promote(request, pk):
  activeuser                 =  User.objects.get(id=request.user.id)    # get details of activeuser
  activeperson               =  Person.objects.get(username=activeuser.username)
  person                     =  get_object_or_404(Person, pk=pk)     # get details of person to be updated/displayed/deleted
  if activeperson.status                >= 50                              \
  and person.fullmember                 == False:
    person.fullmember                   =  True
    person.authorname                   =  ''
    person.save()                                                                   # update user record with extra details
    #form.save_m2m()
    return redirect('memberlist')

@login_required
def demote(request, pk):
  activeuser                 =  User.objects.get(id=request.user.id)    # get details of activeuser
  activeperson               =  Person.objects.get(username=activeuser.username)
  person                     =  get_object_or_404(Person, pk=pk)     # get details of person to be updated/displayed/deleted
  if activeperson.status                >= 50                              \
  and person.fullmember                 == True:
    person.fullmember                   =  False
    person.authorname                   =  ''
    person.save()                                                                   # update user record with extra details
    return redirect('memberlist')




# functions which update the database in two stages,  using forms
# but don't require a pk as they don't refer to an existing record
@login_required
def member_insert(request):
  activeuser                            =  User.objects.get(id=request.user.id)    # get details of activeuser
  activeperson                          =  Person.objects.get(username=activeuser.username)
  if request.method                     != "POST": # i.e. method == "GET":
    if activeperson.status              >= 38:
      form = InsertMemberForm()                                               # get a blank InsertPersonForm
      return render(request, 'users/person_insert_update.html', {'form': form})
    else:
      return redirect('eventlist')
  else:
    form                                    = InsertMemberForm(request.POST)                     # get a InsertPersonForm filled with details of new user
    if form.is_valid():
      person                                = form.save(commit=False)                 # extract details from user fo
      person.authorname                     = activeperson.username
      user = User.objects.create_user(person.username, 'a@a.com', person.password)  # create user record from form
      #user.first_name                       = person.display_name
      user.save()
      person.password                       = ''
      person.save()
      form.save_m2m()
      return redirect('memberlist')
    else:
      return render(request, 'users/person_insert_update.html', {'form': form})

@login_required
def contact_insert(request):
  activeuser                                =  User.objects.get(id=request.user.id)    # get details of activeuser
  activeperson                              =  Person.objects.get(username=activeuser.username)
  if request.method                         != "POST": # i.e. method == "GET":
    form = InsertContactForm()                                               # get a blank InsertPersonForm
    return render(request, 'users/contact_new.html', {'form': form})
  else:                                     # i.e method == 'POST'
    form                                    = InsertContactForm(request.POST)                     # get a InsertPersonForm filled with details of new user
    if form.is_valid():
      person                                = form.save(commit=False)                 # extract details from user for
      person.fullmember                     = False
      person.status                         =  5
      person.authorname                     = activeperson.username
      person.save()                                                                   # update user record with extra details
      form.save_m2m()
      return redirect('memberlist')
    else:                                                                        # i.e. form is not valid, ask activeuser to resubmit it
      return render(request, 'users/contact_new.html', {'form': form})




# functions which update the database in two stages,  using forms
# but do not require a pk as they refer to activeuser
@login_required
def password(request):
  if request.method                           != "POST": # i.e. method == "GET":
    form = PasswordForm()
    return render(request, 'users/password.html', {'form': form})
  else:                                       # i.e method == 'POST'
    form                                      = PasswordForm(request.POST)
    if form.is_valid():
      activeuser                              =  User.objects.get(id=request.user.id)    # get details of activeuser
      password                                = form.cleaned_data['password']
      activeuser.set_password(password)
      activeuser.save()
      return redirect('eventlist' 'current')
    else:                                                                        # i.e. form is not valid, ask activeuser to resubmit it
      return render(request, 'users/insert_update.html', {'form': form})

@login_required
def display_name(request):
  activeuser                 =  User.objects.get(id=request.user.id)    # get details of activeuser
  activeperson               =  Person.objects.get(username=activeuser.username)
  if request.method                           != "POST": # i.e. method == "GET":
    form = DisplaynameForm(initial = {'display_name': activeperson.display_name})
    return render(request, 'users/displayname.html', {'form': form})                # ask activeuser for details of new/updated user
  else:
    form                     = DisplaynameForm(request.POST)
    if form.is_valid():
      activeperson.display_name                 = form.cleaned_data['display_name']
      activeperson.save()
      activeuser.first_name                     = form.cleaned_data['display_name']
      activeuser.save()
      return redirect('memberlist')
    else:                                                                        # i.e. form is not valid, ask activeuser to resubmit it
      return render(request, 'users/insert_update.html', {'form': form})


@login_required
def user_colours(request, whence, type='get', color='black' ):
  activeuser                 =  User.objects.get(id=request.user.id)    # get details of activeuser
  activeperson               =  Person.objects.get(username=activeuser.username)
  if request.method          != "POST": # i.e. method == "GET":
    if type                  == 'get':
      form = UserOptionsForm(instance = activeperson)
      return render(request, 'users/usercolours.html', {'form': form, 'activeperson': activeperson, 'whence': whence})                # ask activeuser for details of new/updated user
    else:
      if activeperson.reversevideo           == False:
        if type                              == 'date':
          activeperson.datecolor             = color
        elif type                            == 'detail':
          activeperson.detailcolor           = color
        elif type                            == 'attendees':
          activeperson.attendeescolor        = color
        elif type                            == 'background':
          activeperson.backgroundcolor       = color
        elif type                            == 'reverse':
          activeperson.reversevideo          = True
        else:
          return redirect('usercolours', 'get', 'get', whence)
      elif activeperson.reversevideo         == True:
        if type                              == 'date':
          activeperson.datecolor_rev         = color
        elif type                            == 'detail':
          activeperson.detailcolor_rev       = color
        elif type                            == 'attendees':
          activeperson.attendeescolor_rev    = color
        elif type                            == 'background':
          activeperson.backgroundcolor_rev   = color
        elif type                            == 'forward':
          activeperson.reversevideo          = False
        else:
          return redirect('usercolours', 'get', 'get', whence)
      else:
        return redirect('usercolours', 'get', 'get', whence)

      activeperson.save()
      if type                          in ['reverse', 'forward']:
        return redirect('usercolours', 'get', 'get', whence)
      else:
        if whence == 'events':
          return redirect('eventlist', 'current')
        elif whence == 'users':
          return redirect('memberlist')

  else:
    form                     = UserOptionsForm(request.POST)
    if form.is_valid():
      activeperson.display_name                 = form.cleaned_data['display_name']
      activeperson.save()
      activeuser.first_name                     = form.cleaned_data['display_name']
      activeuser.save()
      return redirect('eventlist')
    else:                                                                        # i.e. form is not valid, ask activeuser to resubmit it
      return render(request, 'users/usercolours.html', {'form': form, 'whence': whence})

@login_required
def default_colours(request, whence, type='get', color='black' ):
  activeuser                 =  User.objects.get(id=request.user.id)    # get details of activeuser
  activeperson               =  Person.objects.get(username=activeuser.username)
  if request.method          != "POST": # i.e. method == "GET":
    if type                  == 'get':
      form = UserOptionsForm(instance = activeperson)
      return render(request, 'users/usercolours.html', {'form': form, 'activeperson': activeperson, 'whence': whence})                # ask activeuser for details of new/updated user
    else:
      if activeperson.reversevideo           == False:

        if type                              == 'date':
          activeperson.datecolor             = color
        elif type                            == 'detail':
          activeperson.detailcolor           = color
        elif type                            == 'attendees':
          activeperson.attendeescolor        = color
        elif type                            == 'background':
          activeperson.backgroundcolor       = color
        elif type                            == 'reverse':
          activeperson.reversevideo          = True
        else:
          return redirect('useroptions', 'get', 'get', whence)
      elif activeperson.reversevideo         == True:
        if type                              == 'date':
          activeperson.datecolor_rev         = color
        elif type                            == 'detail':
          activeperson.detailcolor_rev       = color
        elif type                            == 'attendees':
          activeperson.attendeescolor_rev    = color
        elif type                            == 'background':
          activeperson.backgroundcolor_rev   = color
        elif type                            == 'forward':
          activeperson.reversevideo          = False
        else:
          return redirect('useroptions', 'get', 'get', whence)
      else:
        return redirect('useroptions', 'get', 'get', whence)

      activeperson.save()
      if type                          in ['reverse', 'forward']:
        return redirect('usercolours', 'get', 'get', whence)
      else:
        if whence == 'events':
          return redirect('eventlist', 'current')
        elif whence == 'users':
          return redirect('memberlist')
  else:
    form                     = UserColoursForm(request.POST)
    if form.is_valid():
      activeperson.display_name                 = form.cleaned_data['display_name']
      activeperson.save()
      activeuser.first_name                     = form.cleaned_data['display_name']
      activeuser.save()
      return redirect('eventlist', 'current')
    else:                                                                        # i.e. form is not valid, ask activeuser to resubmit it
      return render(request, 'users/usercolours.html', {'form': form, 'whence': whence})

# functions which update the database in two stages,  using forms
# and do require a pk as they refer to a user who is not, generally, the activeuser
@login_required
def member_amend(request, pk):
  activeuser                            =  User.objects.get(id=request.user.id)    # get details of activeuser
  activeperson                          =  Person.objects.get(username=activeuser.username)
  person                                =  get_object_or_404(Person, pk=pk)     # get details of person to be updated/displayed/deleted
  user                                  =  User.objects.get(username=person.username)

  if request.method                     != "POST": # i.e. method == "GET":
    if activeperson.status              >= 60:
      form = UpdateMemberForm(instance=person)                                # get a UpdatePersonForm filled with details of Profile to be upd
    else:
      form = UpdateMemberBForm(instance=person)                                # get a UpdatePersonForm filled with details of Profile to be upd
    return render(request, 'users/person_insert_update.html', {'form': form})


#    form = UpdateMemberForm(instance=person)                                # get a UpdatePersonForm filled with details of Profile to be upd
#    return render(request, 'users/person_insert_update.html', {'form': form})                # ask activeuser for details of new/updated user
  else:                                 # i.e method == 'POST'
    if activeperson.status              >= 60:
      form                                = UpdateMemberForm(request.POST, instance=person)
    elif activeperson.status            >= 35:
      form                                = UpdateMemberBForm(request.POST, instance=person)
    else:
      return render(request, 'users/person_insert_update.html', {'form': form})
#    form                                = UpdateMemberForm(request.POST, instance=person)
#    if form.is_valid() and activeperson.status             >= 60:
    if form.is_valid():
      if activeperson.status             >= 60 or (activeperson.status             >= 35 and person.status < 35):
        person                            = form.save(commit=False)                 # extract details from user form
        user.first_name                   = person.display_name
        user.save()
        person.save()                                                                   # update user record with extra details
        form.save_m2m()
        return redirect('memberlist')
      else:                                                                        # i.e. form is not valid, ask activeuser to resubmit it
        return render(request, 'users/member_person_insert_update.html', {'form': form})
    else:                                                                        # i.e. form is not valid, ask activeuser to resubmit it
      return render(request, 'users/member_person_insert_update.html', {'form': form})