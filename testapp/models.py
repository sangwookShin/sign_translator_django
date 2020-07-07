import json
import os
import subprocess

import cv2
import numpy as np
from tensorflow_core.python.keras.models import model_from_json
from testapp.datasource import datasource
import joblib

TIME_STAMP = 50
ROOT_PATH = os.getcwd()


class TranslateSLN:

    def __init__(self):
        self.l = None
        self.z = None
        self.y = None

    def translate_sln(self):
        image_path = os.path.abspath(ROOT_PATH + "/openpose_source/examples/image/")
        frame_list = os.listdir(image_path)
        self._calculate_baseline(frame_list)

        # TIME_STAMP만큼 FRAME 추출
        selected_frame = [frame_list[self.y + j * self.z] for j in range(TIME_STAMP)]

        # 선택된 FRMAME을 제외하고 나머지 FRAME제거
        for frame in frame_list:
            if frame not in selected_frame:
                os.remove(image_path + "/" + frame)

        # frame의 width와 height계산
        width, height, _ = cv2.imread(image_path + "/" + selected_frame[0], cv2.IMREAD_UNCHANGED).shape

        # self._run_openpose()

        # feature 추출
        json_file_path = os.path.abspath(ROOT_PATH + "/openpose_source/out/")
        np_feature = self._get_feature_of_images(json_file_path, width, height)

        # without face key point
        # np_feature = np.delete(np_feature, slice(24, 164), 1)

        # normalization
        np_feature = self._normalization(np_feature)
        scaler = joblib.load(os.path.abspath(ROOT_PATH + "/testapp/model/standard_norm_model.pkl"))
        np_feature = scaler.transform(np_feature)

        # load GRU model
        model_path = os.path.abspath(ROOT_PATH + "/testapp/model/")
        with open(os.path.abspath(model_path + "/SLT-model-001.json"), 'r') as json_file:
            loaded_model_json = json_file.read()

        model = model_from_json(loaded_model_json)
        model.load_weights(os.path.abspath(model_path + "/SLT-model-001.h5"))

        predict = model.predict(np_feature.reshape((1, 50, 248)))
        max_index = np.argmax(predict[0])

        self._clear_directory(image_path, json_file_path)

        return {
            'message': datasource.dic_label[max_index],
            'probability': str(predict[0][max_index])
        }

    @staticmethod
    def _clear_directory(image_path, json_path):
        frame_list = os.listdir(image_path)
        json_file_list = os.listdir(json_path)

        for frame, json_file in zip(frame_list, json_file_list):
            os.remove(image_path + "/" + frame)
            os.remove(json_path + "/" + json_file)

        print("Success clearing directory")

    @staticmethod
    def _get_feature_of_images(json_file_path, width, height):
        result = []

        for file in os.listdir(json_file_path):
            with open(os.path.abspath(json_file_path + "/" + file)) as json_file:
                json_feature = json.load(json_file)

            image_feature = []
            feature = json_feature["people"][0]
            # body key points
            image_feature.extend(feature["pose_keypoints_2d"][:8 * 3])
            image_feature.extend(feature['pose_keypoints_2d'][15*3:19*3])

            # face, both hand key points
            image_feature.extend(feature['face_keypoints_2d'])
            image_feature.extend(feature['hand_left_keypoints_2d'])
            image_feature.extend(feature['hand_right_keypoints_2d'])

            # delete channel value
            del image_feature[2::3]

            result.append(image_feature)

        # normalization
        result = np.array(result)
        for i in range(result.shape[1]):
            if i % 2 is 0:
                result[:, i] = result[:, i] / width
            else:
                result[:, i] = result[:, i] / height

        return result

    @staticmethod
    def _run_openpose():
        os.chdir("./openpose_source")
        openpose_command = [".\\bin\OpenPoseDemo.exe", "--image_dir", ".\examples\image\\", "--write_json", ".\out\\",
                            "0", "--display", "0", "--render_pose", "0", "--face", "--hand"]
        proc = subprocess.Popen(openpose_command)

        proc.wait()

        os.chdir(ROOT_PATH)
        print("Finish Openpose!!!")

    def _calculate_baseline(self, frame_list):
        self.l = len(frame_list)
        self.z = int(self.l / (TIME_STAMP - 1))
        self.y = int((self.l - self.z * (TIME_STAMP - 1)) / 2)

    @staticmethod
    def _position_correction(row):
        standard_x, standard_y = row[[2, 3]]
        result = []

        for i in range(len(row)):
            if i % 2 == 0:
                result.append(row[i] - standard_x)
            else:
                result.append(row[i] - standard_y)

        return result

    def _normalization(self, data):
        result = []

        for row in data:
            result.append(self._position_correction(row))

        return np.array(result)
