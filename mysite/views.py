#from django.utils                   import timezone
from django.contrib.auth.models     import User
from django.shortcuts               import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls                    import reverse_lazy
from .models                        import Sitesettings
from .models                        import Photo
from .models                        import Note
from users.models                   import Person
from .forms                         import SiteadminForm
from .forms                         import PhotoForm
from .forms                         import PhotoUpdateForm
from .forms                         import NoteForm
#from django.views.generic           import ListView
from django.views.generic           import CreateView
from django.views.generic           import UpdateView
#from django.views.generic           import DeleteView

@login_required
def siteadmin_detail(request):
  #activeuser                            =  User.objects.get(id=request.user.id)    # get details of activeuser
  sitesettings                          =  get_object_or_404(Sitesettings)     # get details of person to be updated/displayed/deleted

  if request.method                     != "POST": # i.e. method == "GET":
    form = SiteadminForm(instance=sitesettings)                                # get a UpdatePersonForm filled with details of Profile to be upd
    return render(request, 'mysite/siteadmin.html', {'form': form, 'sitesettings': sitesettings})                # ask activeuser for details of new/updated user
  else:                                 # i.e method == 'POST'
    form                                = SiteadminForm(request.POST, instance=sitesettings)
    if form.is_valid:
#    and activeperson.status             >= 60:
      sitesettings                            = form.save(commit=False)
      sitesettings.save()
      return redirect('eventlist' ,'current')
    else:                                                                        # i.e. form is not valid, ask activeuser to resubmit it
      return render(request, 'mysite/siteadmin.html', {'form': form, 'sitesettings': sitesettings})

def fromlogin(request):
      return redirect('eventlist', 'current')
      #return redirect('homepage')

def logout(request):
    logout(request)

@login_required
def photo_list(request):
  photos                                     = Photo.objects.filter(is_live=True)
  return render(request, 'mysite/photo_list.html', {'photos': photos})

@login_required
def photo_list_deleted(request):
  photos                                     = Photo.objects.filter(is_live=False)
  return render(request, 'mysite/photo_list_deleted.html', {'photos': photos})

"""
class PhotoList(ListView):
    model = Photo
    template_name = 'photo_list.html'
"""

class PhotoInsert(CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'mysite/photo_insert_update.html'
    success_url = reverse_lazy('photolist')

"""
class PhotoUpdate(UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'mysite/photo_insert_update.html'
    success_url = reverse_lazy('photolist')

class PhotoDelete(DeleteView):
    model = Photo
    success_url = reverse_lazy('photolist')
"""


@login_required
def photo_update(request, pk):
    activeuser                                                                      =  User.objects.get(id=request.user.id)
    activeperson                                                                    =  Person.objects.get(username=activeuser.username)
    photo                                                                           = get_object_or_404(Photo, pk=pk)
    if request.method                                                               != 'POST':
        form                                                                        = PhotoUpdateForm(instance=photo)
        context                                                                     =   {'form': form}
        return render                                                               (request,'mysite/photo_insert_update.html' , context)
    else:
        form                                                                        = PhotoUpdateForm(request.POST, instance=photo)
        if form.is_valid():
            note                                                                    = form.save(commit=False)
            if request.user.is_authenticated and activeperson.status >=  60:
                note.save()
                form.save_m2m()
                return redirect('photolist')
            else:
                context                                                              =      {'form': form}
                return render                                                               (request, 'mysite/photo_insert_update.html', context)
        else:
            context                                                                 =   {'form': form}
            return render                                                               (request,'mysite/photo_insert_update.html' , context)

@login_required
def photo_delete(request, pk):
    activeuser                                                                      =  User.objects.get(id=request.user.id)
    activeperson                                                                    =  Person.objects.get(username=activeuser.username)
    photo                                                                           = get_object_or_404(Photo, pk=pk)
    if request.user.is_authenticated and activeperson.status >=  60:
        photo.is_live                                                               = False
        photo.save()
    return redirect('photolist')

@login_required
def photo_restore(request, pk):
    activeuser                                                                      =  User.objects.get(id=request.user.id)
    activeperson                                                                    =  Person.objects.get(username=activeuser.username)
    photo                                                                           = get_object_or_404(Photo, pk=pk)
    if request.user.is_authenticated and activeperson.status >=  60:
        photo.is_live                                                               = True
        photo.save()
    return redirect('photolist')

@login_required
def photo_delete_perm(request, pk):
    activeuser                                                                      =  User.objects.get(id=request.user.id)
    activeperson                                                                    =  Person.objects.get(username=activeuser.username)
    photo                                                                           = get_object_or_404(Photo, pk=pk)
    if request.user.is_authenticated and activeperson.status >=  60:
        photo.delete()
    return redirect('photolist')

@login_required
def note_update(request):
    activeuser                                                                      =  User.objects.get(id=request.user.id)
    activeperson                                                                    =  Person.objects.get(username=activeuser.username)
    note                                                                            =  Note.objects.get()
    if request.method                                                               != 'POST':
        form                                                                        = NoteForm(instance=note)
        context                                                                     =   {'form': form}
        return render                                                               (request, 'mysite/note_update.html', context)
    else:
        form                                                                        = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note                                                                    = form.save(commit=False)
            if request.user.is_authenticated and activeperson.status                >=  60:
                note.save()
                form.save_m2m()
                return redirect('eventlist', 'current')
            else:
                context                                                              =      {'form': form}
                return render                                                               (request, 'mysite/note_update.html', context)
        else:
            context                                                                 =   {'form': form}
            return render                                                               (request, 'mysite/note_update.html', context)


@login_required
def note_delete(request):
    activeuser                                                                      =  User.objects.get(id=request.user.id)
    activeperson                                                                    =  Person.objects.get(username=activeuser.username)
    note                                                                            = Note.objects.get()
    if request.user.is_authenticated and activeperson.status >=  60:
        note.note_content                                                           = ""
        note.save()
    return redirect('eventlist', 'current')


"""
#@login_required
#def advert_display(request):
#  activeuser                              =  User.objects.get(id=request.user.id)
#  activeperson                            =  Person.objects.get(username=activeuser.username)
##  return render(request, 'sitesettings/advert_display.html', { 'activeperson': activeperson, 'IS_CLUB': IS_CLUB})
#
## functions which update the database in two stages,  using forms
# but don't require a pk as they don't refer to an existing record
#@login_required
#def advert_insert(request):
#  activeuser                            =  User.objects.get(id=request.user.id)    # get details of activeuser
#  activeperson                          =  Person.objects.get(username=activeuser.username)
#
#  if request.method                     != "POST": # i.e. method == "GET":
#    if activeperson.status             >= 60:
#      form = InsertAdvertForm()                                               # get a blank InsertPersonForm
#      return render(request, 'sitesettings/advert_new.html', {'form': form})
#    else:
#      return redirect('events.views.event_list')
#  else:                                 # i.e method == 'POST'
#    form                                = InsertAdvertForm(request.POST)                     # get a InsertPersonForm filled with details of new user
#    if form.is_valid()\
#    and activeperson.status             >= 60:
#      advert                                = form.save(commit=False)                 # extract details from user for
#      advert.save()
#      return redirect('events.views.event_list')
#    else:
#      return render(request, 'users/insert_update.html', {'form': form})
#

"""
