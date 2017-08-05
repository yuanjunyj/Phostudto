import keras
from keras.models import Model
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras import backend as K
from keras.applications.vgg16 import VGG16
import tensorflow
import cv2
from sklearn.neighbors import BallTree
import numpy
from PIL import ImageFile
from .models import ImageData
import threading
from PIL import Image


def List2Str(num_list):
    length = len(num_list)
    str_result = ""
    for i in range(length - 1):
        str_result += str(num_list[i])
        str_result += "_"
    str_result += str(num_list[length - 1])
    return str_result


def Str2List(str_origin):
    str_list = str_origin.split("_")
    return [float(x) for x in str_list]


if K.image_data_format() == 'channels_first':
    input_shape = (3, 224, 224)
else:
    input_shape = (224, 224, 3)
base_model = VGG16(include_top=False, weights=None, input_shape=input_shape)
feature_model = Sequential()
feature_model.add(Flatten(input_shape=base_model.output_shape[1:]))
feature_model.add(Dense(64, activation='relu'))
feature_model.add(Dropout(0.5))
feature_model = Model(inputs=base_model.input, outputs=feature_model(base_model.output))
feature_model.load_weights("media/BTData/vgg16_12.h5", by_name=True)
feature_model.summary()
feature_model.compile(loss='binary_crossentropy',
                      optimizer=keras.optimizers.SGD(lr=1e-4, momentum=0.9),
                      metrics=['accuracy'])
graph = tensorflow.get_default_graph()

thread_num = 0


def get_thread_num():
    global thread_num
    return thread_num


def calculate_pic(files, user):
    global graph
    global thread_num

    if len(files) == 0:
        return None

    lock = threading.Lock()
    lock.acquire()
    try:
        thread_num += 1
    finally:
        lock.release()
    pic_feature_224 = []
    print()
    print(thread_num)
    print()
    for file in files:
        try:
            img = Image.open("media/photos/" + str(user.id) + '/' + user.current_visiting_path + file.name)
        except IOError:
            pic_feature_224.append([[[0, 0, 0] for i in range(224)] for i in range(224)])
            pass
        else:
            img = img.convert("RGB")
            img = numpy.array([[y[::-1] for y in x] for x in numpy.array(img)])
            img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
            pic_feature_224.append(img)
    pic_feature_224_array = numpy.array(pic_feature_224)
    with graph.as_default():
        final_feature = feature_model.predict(pic_feature_224_array)
    for i in range(len(files)):
        str_temp = List2Str(final_feature[i])
        # print(str_temp)
        temp_obj = ImageData.objects.filter(image="photos/" + str(user.id) + '/'
                                                  + user.current_visiting_path + files[i].name)
        if len(temp_obj) != 0: 
            temp_obj = temp_obj[0]
            temp_obj.feature = str_temp
            temp_obj.save()
    lock.acquire()
    try:
        thread_num -= 1
    finally:
        lock.release()
    print()
    print(thread_num)
    print()


def search_image(file):
    global graph

    pic_feature_224 = []

    parser = ImageFile.Parser()
    for chunk in file.chunks():
        parser.feed(chunk)
    img_origin = parser.close()

    img_origin = img_origin.convert("RGB")
    img = numpy.array(img_origin)
    img = numpy.array([[y[::-1] for y in x] for x in img])
    img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
    pic_feature_224.append(img)

    pic_feature_224_array = numpy.array(pic_feature_224)
    with graph.as_default():
        final_feature = feature_model.predict(pic_feature_224_array)
    ImageData_list = [Str2List(x.feature) for x in list(ImageData.objects.all()) if x.feature is not None]
    if len(ImageData_list) == 0:
        return []
    else:
        tree = BallTree(ImageData_list, leaf_size=2, metric='euclidean')
        dist, ind = tree.query(final_feature[0], k=9)
        return [list(ImageData.objects.all())[i] for i in ind[0]]