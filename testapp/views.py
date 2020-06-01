from PIL import Image
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.http import HttpResponseRedirect, HttpResponse
# Create your views here.

import base64
import datetime


def index(request):
    return render(request, '../templates/index.html', {})



def communication(request):
    if request.method == 'POST':
        temp = request.POST.get('img', '')

        temp = temp[21:]
        imgdata = base64.b64decode(temp)

        basename = "image"
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S_%f")
        filename = "_".join([basename, suffix])

        filename = './media/'+filename+'.png'  # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
            f.write(imgdata)
        return HttpResponse('test')
    else:
        print(2)
        return render(request, '../templates/communication.html', {})

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