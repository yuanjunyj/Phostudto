from django.contrib import auth
from django.shortcuts import render, render_to_response, redirect
from django import forms
from django.http import HttpResponse
from django.contrib import messages
from testimg.models import *
from .models import ImageData
from .imageProcessing import choose_model
from .str_to_list import *
from .dirlist import *
import os

from .tools import calculate_pic, get_thread_num, search_image
import threading

# Create your views here.

def display(request):
    pics = ImageData.objects.order_by('-created_at')[:5]
    print(pics)
    user = auth.get_user(request)
    pics_is_liked = []
    if user.is_authenticated():
        like_list = decode_str(user.like_list)
        for i in range(0, len(pics)):
            if pics[i].id in like_list:
                pics_is_liked.append((pics[i], 1))
            else:
                pics_is_liked.append((pics[i], 0))
        #user = auth.get_user(request)
        labels_str = user.labels
        labels = decode_str(user.labels)        

    else:
        for i in range(0, len(pics)):
            pics_is_liked.append((pics[i], -1))
        labels =[]

    return render(request, 'display.html', {'pics': pics_is_liked, 'labels': labels})

def uploadPhoto(request):
    if request.method == "POST":
        files = request.FILES.getlist('myfiles')

        for file in files:
            # write in database
            imageData = ImageData()
            user = auth.get_user(request)
            imageData.username = user
            imageData.path = user.current_visiting_path
            imageData.image.save(str(user.id) + '/' + user.current_visiting_path + file.name, file)
            imageData.save()

        t = threading.Thread(target=calculate_pic, args=(files, auth.get_user(request)))
        t.start()
        #messages.info(request, '图片上传成功~')  
    return redirect('profile')

def SearchPhoto(request):
    pics = []
    if request.method == "POST":
        files = request.FILES.getlist('myfiles')
        if len(files) == 0:
            messages.info(request, '请选择图片')
        else:
            pics = search_image(files[0])
    # print(pics)
    user = auth.get_user(request)
    pics_is_liked = []
    if user.is_authenticated():
        like_list = decode_str(user.like_list)
        for i in range(0, len(pics)):
            if pics[i].id in like_list:
                pics_is_liked.append((pics[i], 1))
            else:
                pics_is_liked.append((pics[i], 0))
        labels = decode_str(user.labels)
    else:
        for i in range(0, len(pics)):
            pics_is_liked.append((pics[i], -1))
        labels =[]
    return render(request, 'searchPhoto.html', {'pics': pics_is_liked, 'labels': labels})

def deletePhoto(request):
    if request.method == "POST":
        rms = request.POST.getlist('deleteList')
        print(rms)
        for rm in rms:
            os.remove( os.path.join('./media/', rm).replace('\\','/') )
            ImageData.objects.get(image=rm).delete()
        #messages.info(request, '图片删除成功~')
    return redirect('profile')

def filterPhoto(request):
    return render(request, 'profile.html')

def profile(request):
    user = auth.get_user(request)
    pics = ImageData.objects.filter(username = user, path = user.current_visiting_path)
    pics_is_liked = []
    like_list = decode_str(user.like_list)
    for i in range(0, len(pics)):
        if pics[i].id in like_list:
            pics_is_liked.append((pics[i], 1))
        else:
            pics_is_liked.append((pics[i], 0))
    labels_str = user.labels
    labels = decode_str(user.labels) 
    return render(request, 'profile.html', {'pics': pics_is_liked, 'labels':labels})

def makedir(request):
    user = auth.get_user(request);
    path = os.path.abspath(os.curdir).replace('\\', '/') + '/media/photos/' + str(user.id) + '/' + user.current_visiting_path + request.POST.get("dirname")
    os.mkdir(path)
    return redirect('profile')



def imageProcess(request):
    return HttpResponse('../' + choose_model(request.GET.get('mode'), request.GET.get('path')[1:]))

def saveNewPhoto(request):
    path = request.GET.get('path')[9:] #slice ../media/
    # write in database
    user = auth.get_user();
    imageData = ImageData()
    imageData.username = auth.get_user(request)
    imageData.image = path
    imageData.path = user.current_visiting_path
    imageData.save()
    return HttpResponse(user.current_visiting_path)

def deleteTempImg(request):
    path = request.GET.get('path')[3:] #slice ../
    if path != "":
        os.remove(path)
    return HttpResponse("")

def likeOrWithdrew(request):
    picId = request.GET.get('picId')  #type(picId) == string  直接用string操作
    pic = ImageData.objects.get(id=picId)
    user = auth.get_user(request)
    like_list = decode_str(user.like_list)
    likes = pic.likes

    if picId in like_list:
        likes -= 1
        pic.likes = likes
        pic.save()
        like_list.remove(picId)
        user.like_list = encode_str(like_list)
        user.save()
        return HttpResponse(0)
    else:
        likes += 1
        pic.likes = likes
        pic.save()
        like_list.append(picId)
        user.like_list = encode_str(like_list)
        user.save()
        return HttpResponse(1)

def chooseLabels(request):
    imgPath = request.GET.get('path')[7:]
    pic = ImageData.objects.get(image=imgPath)
    user = auth.get_user(request)
    labels = []
    labels.append(request.GET.get('label0'))
    labels.append(request.GET.get('label1'))
    labels.append(request.GET.get('label2'))
    labels_str = encode_str(labels)
    pic.img_labels = labels_str
    pic.save()
    labels_of_user = decode_str(user.labels)
    for label in labels:
        if label != '' and label not in labels_of_user:
            labels_of_user.append(label)
    user.labels = encode_str(labels_of_user)
    user.save()
    return HttpResponse(1)

def getPicLabels(request):
    imgPath = request.GET.get('path')[7:]
    pic = ImageData.objects.get(image=imgPath)
    return HttpResponse(pic.img_labels)



def register(request):
    user = auth.get_user(request)
    menutree = dirlist(os.path.abspath(os.curdir).replace('\\', '/') + '/media/photos/' + str(user.id) + '/' + user.current_visiting_path)
    print(menutree)
    return render(request, 'register.html', {'menutree': menutree})