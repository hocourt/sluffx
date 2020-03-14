#from django.utils                   import timezone
from django.contrib.auth.models     import User
from django.shortcuts               import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls                    import reverse_lazy
from .models                        import Site
from .models                        import Photo
#from .models                        import Note
from users.models                   import Person
from .forms                         import advertUpdateForm
from .forms                         import noteUpdateForm
from .forms                         import PhotoInsertForm
from .forms                         import PhotoUpdateForm
from .forms                         import EnquiryInsertForm
#from django.views.generic           import ListView
from django.views.generic           import CreateView
from django.views.generic           import UpdateView
#from django.views.generic           import DeleteView


def fromlogin(request):
      return redirect('eventlist', 'current')
      #return redirect('homepage')

def logout(request):
    logout(request)

@login_required
def advert_update(request):
    activeuser                                                          =     User.objects.get(id=request.user.id)
    activeperson                                                        =     Person.objects.get(username=activeuser.username)
    site                                                                =      get_object_or_404(Site)     

    if request.method                                                   != 	"POST": 
        form 				= 	                                            advertUpdateForm(instance=site)
        context				                                            =	{'form': form, 'site': site}
        return render				                                        (request, 'mysite/advert_update.html', context)
    else:                                 
        form                                                            = 	advertUpdateForm(request.POST, instance=site)
        if form.is_valid and activeperson.status >= 55:
            site                                                        =   form.save(commit=False)
            site.save()        
            return redirect                                                 ('eventlist' ,'current')
        else:                                                                        
            context                                                     =   {'form': form, 'site': site}
            return render                                                   (request, 'mysite/advert_update.html', context)

@login_required
def note_update(request):
    activeuser                                                                      =  User.objects.get(id=request.user.id)
    activeperson                                                                    =  Person.objects.get(username=activeuser.username)
    site                                                                            =  Site.objects.get()
    if request.method                                                               != 'POST':
        form                                                                        = noteUpdateForm(instance=site)
        context                                                                     =   {'form': form}
        return render                                                               (request, 'mysite/note_update.html', context)
    else:
        form                                                                        = noteForm(request.POST, instance=site)
        if form.is_valid():
            note                                                                    = form.save(commit=False)
            if request.user.is_authenticated and activeperson.status                >=  55:
                note.save()
                form.save_m2m()
                return redirect('eventlist', 'current')
            else:
                context                                                              =      {'form': form}
                return render                                                               (request, 'mysite/note_update.html', context)
        else:
            context                                                                 =   {'form': form}
            return render                                                               (request, 'mysite/note_update.html', context)

"""
@login_required
def note_delete(request):
    activeuser                                                                      =  User.objects.get(id=request.user.id)
    activeperson                                                                    =  Person.objects.get(username=activeuser.username)
    site                                                                            = Site.objects.get()
    if activeperson.status >=  55:
        site.note                                                            		= ""
        site.save()
    return redirect                                                                     ('eventlist', 'current')
"""

@login_required
def photo_list(request):
  photos                                     = Photo.objects.filter(is_live=True)
  return render                                 (request, 'mysite/photo_list.html', {'photos': photos})

@login_required
def photo_list_deleted(request):
  photos                                     = Photo.objects.filter(is_live=False)
  return render(request, 'mysite/photo_list_deleted.html', {'photos': photos})


class PhotoInsert(CreateView):
    model = Photo
    form_class = PhotoInsertForm
    template_name = 'mysite/photo_insert.html'
    success_url = reverse_lazy('photolist')



@login_required
def photo_update(request, pk):
    activeuser                                                                      =  User.objects.get(id=request.user.id)
    activeperson                                                                    =  Person.objects.get(username=activeuser.username)
    photo                                                                           = get_object_or_404(Photo, pk=pk)
    if request.method                                                               != 'POST':
        form                                                                        = PhotoUpdateForm(instance=photo)
        context                                                                     =   {'form': form}
        return render                                                               (request,'mysite/photo_update.html' , context)
    else:
        form                                                                        = PhotoUpdateForm(request.POST, instance=photo)
        if form.is_valid() and (activeperson.status >=  55 or activeperson.username == photo.authorname):
            photo                                                                   = form.save(commit=False)
            photo.save()
            form.save_m2m()
        return redirect('photolist')

@login_required
def photo_delete(request, pk):
    activeuser                                                                      =  User.objects.get(id=request.user.id)
    activeperson                                                                    =  Person.objects.get(username=activeuser.username)
    photo                                                                           = get_object_or_404(Photo, pk=pk)
    if activeperson.status >=  55:
        photo.is_live                                                               = False
        photo.save()
    return redirect('photolist')

@login_required
def photo_restore(request, pk):
    activeuser                                                                      =  User.objects.get(id=request.user.id)
    activeperson                                                                    =  Person.objects.get(username=activeuser.username)
    photo                                                                           = get_object_or_404(Photo, pk=pk)
    if activeperson.status >=  55:
        photo.is_live                                                               = True
        photo.save()
    return redirect('photolist')

@login_required
def photo_delete_perm(request, pk):
    activeuser                                                                      =  User.objects.get(id=request.user.id)
    activeperson                                                                    =  Person.objects.get(username=activeuser.username)
    photo                                                                           = get_object_or_404(Photo, pk=pk)
    if activeperson.status >=  55:
        photo.delete()
    return redirect('photolist')

@login_required
def enquiry_list(request):
    activeuser                                                                      =  User.objects.get(id=request.user.id)
    activeperson                                                                    =  Person.objects.get(username=activeuser.username)
    if activeperson.status >=  40:
        enquirys                                                                    =   Enquiry.objects.filter(is_live=True)
        return render                                                                   (request, 'mysite/enquiry_list.html', {'enquirys': enquirys})
    else:
        return redirect('eventlist')

def enquiry_insert(request):
    if request.method                                                               != 'POST':
        form                                                                        =   EnquiryInsertForm()
        context                                                                     =   {'form': form}
        return render                                                                   (request, 'mysite/enquiry_insert.html', context)
    else:
        form                                                                        =   EnquiryInsertForm(request.POST, instance=enquiry)
        if form.is_valid():
            enquiry                                                                 =   form.save(commit=False)
            enquiry.save()
            form.save_m2m()
            return redirect('eventlist', 'current')
        else:
            context                                                                 =   {'form': form}
            return render                                                               (request, 'mysite/enquiry_insert.html', context)

"""
            if request.user.is_authenticated and activeperson.status >=  60:
def contactus(request):
	pass
class PhotoUpdate(UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'mysite/photo_insert_update.html'
    success_url = reverse_lazy('photolist')

class PhotoDelete(DeleteView):
    model = Photo
    success_url = reverse_lazy('photolist')
class PhotoList(ListView):
    model = Photo
    template_name = 'photo_list.html'
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
