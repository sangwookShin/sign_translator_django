import base64
import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render

from testapp.models import TranslateSLN


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

        filename = './openpose_source/examples/image/' + filename + '.jpg'
        with open(filename, 'wb') as f:
            f.write(imgdata)
        return HttpResponse('test')
    else:
        print(2)
        return render(request, '../templates/communication.html', {})


def RoomSetting(request):
    return render(request, '../templates/RoomSetting.html', {})


def sln_translate(request):
    model = TranslateSLN()
    return HttpResponse(
        json.dumps(model.translate_sln(), ensure_ascii=False),
        status=202,
        content_type="application/json",
        charset="utf-8"
    )
