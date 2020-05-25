from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.http import HttpResponseRedirect
# Create your views here.

def index(request):
    return render(request, '../templates/index.html', {})

def communication(request):
    return render(request, '../templates/communication.html', {})

def RoomSetting(request):
    return render(request, '../templates/RoomSetting.html', {})

# def mainView(request):
#     if request.method == 'POST' and request.FILES['myfile']:
#         myfile = request.FILES['myfile']
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)
#         uploaded_file_url = fs.url(filename)
#
#
#     else :
#         return render(request, 'index.html')

