from django.shortcuts import render
import base64
import datetime
import os
import json
import numpy as np
import cv2
import joblib
import keras
from testapp.datasource import datasource

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from tensorflow.keras.models import model_from_json, load_model


# Create your views here.


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
    TIME_STAMP = 50

    root_path = os.getcwd();
    print(root_path)
    os.chdir("./openpose_source")
    print(os.getcwd())

    image_dir = root_path + "/openpose_source/examples/image/"
    frames_list = os.listdir(image_dir)
    l = len(frames_list)
    z = int(l / (TIME_STAMP - 1))
    y = int((l - z * (TIME_STAMP - 1)) / 2)

    selected_frame = [frames_list[y + j * z] for j in range(TIME_STAMP)]
    print(selected_frame)
    for image in frames_list:
        if image not in selected_frame:
            print(image)
            os.remove(image_dir + "/" + image)

    width, height, _ = cv2.imread(image_dir + "/" + selected_frame[0], cv2.IMREAD_UNCHANGED).shape
    print(width, height)

    # openpose_command = ".\\bin\OpenPoseDemo.exe --image_dir .\examples\image\ --write_json .\out\ 0 --display 0 --render_pose 0 --face --hand"
    # os.system(openpose_command)

    os.chdir(root_path)
    print(os.getcwd())

    feature_list = []
    directory_path = os.path.abspath(root_path + "/openpose_source/out/")
    for json_file in os.listdir(directory_path):
        with open(os.path.abspath(directory_path + "/" + json_file)) as json_file:
            file = json.load(json_file)

        people = file["people"][0]
        image_feature = []
        image_feature.extend(people["pose_keypoints_2d"][:8 * 3])
        image_feature.extend(people["pose_keypoints_2d"][15 * 3:19 * 3])
        image_feature.extend(people["face_keypoints_2d"])
        image_feature.extend(people["hand_left_keypoints_2d"])
        image_feature.extend(people["hand_right_keypoints_2d"])
        del image_feature[2::3]
        feature_list.append(image_feature)

    np_input = np.array(feature_list)
    print(np_input)
    np_input[np_input == 0] = np.nan

    for i in range(np_input.shape[1]):
        if i % 2 == 0:
            np_input[:, i] = np_input[:, i] / width
        else:
            np_input[:, i] = np_input[:, i] / height

    model_path = root_path + "/testapp/model/"
    normalization_model = joblib.load(model_path + "standard_total_normalization.pkl")
    norm_data = normalization_model.transform(np_input)
    norm_data[np.isnan(norm_data)] = -99

    print(norm_data)

    file = open(os.path.abspath(model_path + "SLT-model-005-67.json"), 'r')
    loaded_model_json = file.read()
    file.close()
    print(loaded_model_json)
    print(keras.__version__)
    model = model_from_json(loaded_model_json)
    model.load_weights(os.path.abspath(model_path + "SLT-model-005-67.h5"))

    # model = load_model(model_path + "SLT-model-011-57.h5")

    norm_data = np.delete(norm_data, slice(24, 164), 1)
    norm_data = norm_data.reshape((1, 50, 108))

    predict = model.predict(norm_data)
    print(predict)

    max_index = np.argmax(predict[0])
    message = datasource.dic_label[max_index]
    probability = predict[0][max_index]

    # 사용한 image 제거
    # frames_list = os.listdir(image_dir)
    # for image in frames_list:
    #     os.remove(image_dir + "/" + image)

    return HttpResponse(f'message : {message}, index : {max_index}, probability : {probability}')
