# 수어지교   
농인(청각 장애인)과 청인간의 원활한 소통에 도움을 주고자 청인의 목소리와 농인의 수어를 텍스트로 변환하는 서비스 입니다.

## 설치(Install)
1 프로젝트 Download
```git
git clone https://github.com/SHINMH/sign_translator_django.git
```
2 Openpose Download    
[Openpose Release](https://github.com/CMU-Perceptual-Computing-Lab/openpose/releases) 에서 CPU버전 다운 받는다.   
받은 폴더를 `openpose_source`로 변경 후 `sign_translator_django` 폴더 아래에 넣는다.

## 사용 방법
 ![사용설명](./testapp/static/assets/img/START/descripte.PNG)   
(1) 음성을 텍스트로 변환하기 위한 버튼   
(2) 수어영상을 촬영하기 위한 버튼   
(3) 음성과 수어 해석한 결과를 텍스트로 보여주는 영역   
(4) 수어가 해석된 결과를 보여주는 영역   
&nbsp; 정확도가 50% 미만인 경우 붉은 글씨로 표시된다.

## 사용 모듈
|모듈|모듈|
|:---:|:---:|
|![사진](./testapp/static/assets/img/START/openpose.jpg)|![사진](./testapp/static/assets/img/START/artyom.jpg)|
|![사진](./testapp/static/assets/img/START/tensorflow.png)|![사진](./testapp/static/assets/img/START/colab_logo.png)|
