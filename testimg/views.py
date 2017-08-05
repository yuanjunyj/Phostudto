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
import shutil
from .tools import calculate_pic, get_thread_num, search_image
import threading


# Create your views here.

def index(request):
    pics_latest = ImageData.objects.order_by('-created_at')[:9]
    pics_mostliked_all = ImageData.objects.order_by('-likes')[:]
    pics_mostliked = []
    count_picture = 0
    for pic in pics_mostliked_all:
        if pic not in pics_latest:
            pics_mostliked.append(pic)
            count_picture += 1
            if count_picture >= 9:
                break
    pics_is_liked_latest = []
    pics_is_liked_mostliked = []
    user = auth.get_user(request)
 
    if user.is_authenticated():
        like_list = list(map(int,decode_str(user.like_list)))
        favor_list = list(map(int,decode_str(user.favor_list)))
        for i in range(0, len(pics_latest)):
            pics_labels = decode_str(pics_latest[i].img_labels)
            for j in range(0, 3-len(pics_labels)):
                pics_labels.append('')
            if pics_latest[i].id in like_list and pics_latest[i].id in favor_list:
                pics_is_liked_latest.append((pics_latest[i], 1, 1, i % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
            elif pics_latest[i].id in like_list and pics_latest[i].id not in favor_list:
                pics_is_liked_latest.append((pics_latest[i], 1, 0, i % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
            elif pics_latest[i].id not in like_list and pics_latest[i].id in favor_list:
                pics_is_liked_latest.append((pics_latest[i], 0, 1, i % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
            else:
                pics_is_liked_latest.append((pics_latest[i], 0, 0, i % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
   
        for i in range(0, len(pics_mostliked)):
            pics_labels = decode_str(pics_mostliked[i].img_labels)
            for j in range(0, 3-len(pics_labels)):
                pics_labels.append('')
            if pics_mostliked[i].id in like_list and pics_mostliked[i].id in favor_list:
                pics_is_liked_mostliked.append((pics_mostliked[i], 1, 1, i % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
            elif pics_mostliked[i].id in like_list and pics_mostliked[i].id not in favor_list:
                pics_is_liked_mostliked.append((pics_mostliked[i], 1, 0, i % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
            elif pics_mostliked[i].id not in like_list and pics_mostliked[i].id in favor_list:
                pics_is_liked_mostliked.append((pics_mostliked[i], 0, 1, i % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
            else:
                pics_is_liked_mostliked.append((pics_mostliked[i], 0, 0, i % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
        labels_str = user.labels
        labels = decode_str(user.labels) 

        return render(request, 'index.html', {'pics_latest': pics_is_liked_latest, 'pics_mostliked': pics_is_liked_mostliked, 'labels':labels})
    else:
        for i in range(0, len(pics_latest)):
            pics_labels = decode_str(pics_latest[i].img_labels)
            for j in range(0, 3-len(pics_labels)):
                pics_labels.append('')
            pics_is_liked_latest.append((pics_latest[i], -1, 0, i % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
        for i in range(0, len(pics_mostliked)):
            pics_labels = decode_str(pics_mostliked[i].img_labels)
            for j in range(0, 3-len(pics_labels)):
                pics_labels.append('')
            pics_is_liked_mostliked.append((pics_mostliked[i], -1, 0, i % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
        labels = []
        return render(request, 'index.html', {'pics_latest': pics_is_liked_latest, 'pics_mostliked': pics_is_liked_mostliked, 'labels':labels}) 


def uploadPhoto(request):
    if request.method == "POST":
        files = request.FILES.getlist('myfiles')

        for file in files:
            # write in database
            imageData = ImageData()
            user = auth.get_user(request)
            imageData.username = user
            imageData.image.save(str(user.id) + '/' + user.current_visiting_path + file.name, file)
            imageData.path = user.current_visiting_path
            imageData.filename = imageData.image.name.split('/')[-1]
            imageData.save()

        t = threading.Thread(target=calculate_pic, args=(files, auth.get_user(request)))
        t.start()
    if files != []:
        messages.info(request, 'Photos uploaded successfully')  
    return redirect('profile')

def deletePhoto(request):
    if request.method == "POST":
        rms = request.POST.getlist('deleteList')
        for rm in rms:
            os.remove( os.path.join('./media/', rm).replace('\\','/') )
            ImageData.objects.get(image=rm).delete()
        messages.info(request, 'Photos removed successfully')
    return redirect('profile')

def searchPhotoQuery(request):
    return render(request, 'searchPhoto.html')

def searchPhoto(request):
    pics = []
    if request.method == "POST":
        files = request.FILES.getlist('myfiles')
        if len(files) == 0:
            messages.info(request, '请选择图片')
        else:
            pics = search_image(files[0])
    user = auth.get_user(request)
    pics_is_liked = []
    user = auth.get_user(request)
    like_list = list(map(int,decode_str(user.like_list)))
    favor_list = list(map(int,decode_str(user.favor_list)))
    for i in range(0, len(pics)):
        pics_labels = decode_str(pics[i].img_labels)
        for j in range(0, 3-len(pics_labels)):
            pics_labels.append('')
        if pics[i].id in like_list and pics[i].id in favor_list:
            pics_is_liked.append((pics[i], 1, 1, i % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
        elif pics[i].id in like_list and pics[i].id not in favor_list:
            pics_is_liked.append((pics[i], 1, 0, i % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
        elif pics[i].id not in like_list and pics[i].id in favor_list:
            pics_is_liked.append((pics[i], 0, 1, i % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
        else:
            pics_is_liked.append((pics[i], 0, 0, i % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
    labels_str = user.labels
    labels = decode_str(user.labels)
    return render(request, 'result.html', {'pics': pics_is_liked})

def profile(request):
    user = auth.get_user(request)
    if user.is_authenticated():
        pics = ImageData.objects.filter(username = user, path = user.current_visiting_path)
        pics_is_liked = []
        like_list = list(map(int,decode_str(user.like_list)))
        favor_list = list(map(int,decode_str(user.favor_list)))
        for i in range(0, len(pics)):
            pics_labels = decode_str(pics[i].img_labels)
            for j in range(0, 3-len(pics_labels)):
                pics_labels.append('')
            if pics[i].id in like_list and pics[i].id in favor_list:
                pics_is_liked.append((pics[i], 1, 1, i % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
            elif pics[i].id in like_list and pics[i].id not in favor_list:
                pics_is_liked.append((pics[i], 1, 0, i % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
            elif pics[i].id not in like_list and pics[i].id in favor_list:
                pics_is_liked.append((pics[i], 0, 1, i % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
            else:
                pics_is_liked.append((pics[i], 0, 0, i % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
        labels_str = user.labels
        labels = decode_str(user.labels)
        menutree = dirlist(os.path.abspath(os.curdir).replace('\\', '/') + '/media/photos/' + str(user.id) + '/')
        path = ('root/' + user.current_visiting_path).split('/')[:-1]
        return render(request, 'profile.html', {'pics': pics_is_liked, 'labels':labels, 'menutree': menutree, 'path': path})
    else:
        return redirect('login')

def operatedir(request):
    user = auth.get_user(request)
    dirname = request.POST.get("dirname")
    i = 0
    while i < len(dirname) and dirname[i] == ' ':
        i += 1
    j = len(dirname)
    while j > 0 and dirname[j - 1] == ' ':
        j -= 1
    dirname = dirname[i:j]
    if dirname == '':
        return redirect('profile')
    if '/' in dirname or '\\' in dirname or '?' in dirname or ':' in dirname or '.' in dirname or \
       '|' in dirname or '*' in dirname or '"' in dirname or '<' in dirname or '>' in dirname:
        messages.info(request, 'Invalid: no /,\\,?,:,|,*,",<,>,. should be used in your folder name')
        return redirect('profile')
    if 'makedir' in request.POST.keys():
        #makedir
        path = os.path.abspath(os.curdir).replace('\\', '/') + '/media/photos/' + str(user.id) + '/' + user.current_visiting_path + dirname
        if not os.path.exists(path):
            os.mkdir(path)
            messages.info(request, "Folder " + dirname + " successully created")
            return redirect('profile')
        else:
            messages.info(request, "Folder " + dirname + " already exists")
            return redirect('profile')
    else:
        #deldir
        path = os.path.abspath(os.curdir).replace('\\', '/') + '/media/photos/' + str(user.id) + '/' + user.current_visiting_path + dirname
        if not os.path.exists(path):
            messages.info(request, "Folder " + dirname + " not exists in the current path")
            return redirect('profile')
        rmpath = 'photos/' + str(user.id) + '/' + user.current_visiting_path + request.POST.get("dirname")
        rms = ImageData.objects.filter(username = user, image__contains = rmpath)
        for rm in rms:
            os.remove( os.path.join('./media/', rm.image.name).replace('\\','/') )
            rm.delete()
        shutil.rmtree(path)
        messages.info(request, "Folder " + dirname + " successully removed")
        return redirect('profile')

def enterdir(request):
    user = auth.get_user(request)
    user.current_visiting_path = request.GET.get("path")
    if user.current_visiting_path == ' ':
        user.current_visiting_path = ''
    user.save()
    return redirect('profile')

def imageProcess(request):
    return HttpResponse('../' + choose_model(request.GET.get('mode'), request.GET.get('path')[1:]))

def saveNewPhoto(request):
    path = request.GET.get('path')[9:] #slice ../media/
    # write in database
    user = auth.get_user(request);
    imageData = ImageData()
    imageData.username = auth.get_user(request)
    imageData.image = path
    imageData.path = user.current_visiting_path
    imageData.filename = path.split('/')[-1]
    imageData.save()
    return HttpResponse("Succesfully Saved to my album")

def deleteTempImg(request):
    path = request.GET.get('path')[3:] #slice ../
    if path != "":
        os.remove(path)
    return HttpResponse("")

def likeOrWithdrew(request):
    picId = request.GET.get('picId')  #type(picId) == string  直接用string操作
    pic = ImageData.objects.get(id=picId)
    user = auth.get_user(request)
    likes = pic.likes
    if not user.is_authenticated():
        return HttpResponse(-likes)
    like_list = decode_str(user.like_list)
    likes = pic.likes

    if picId in like_list:
        likes -= 1
        pic.likes = likes
        pic.save()
        like_list.remove(picId)
        user.like_list = encode_str(like_list)
        user.save()
        return HttpResponse(-likes)
    else:
        likes += 1
        pic.likes = likes
        pic.save()
        like_list.append(picId)
        user.like_list = encode_str(like_list)
        user.save()
        return HttpResponse(likes)

def chooseLabels(request):
    imgPath = request.GET.get('path')[7:]
    pic = ImageData.objects.get(image=imgPath)
    user = auth.get_user(request)
    label_to_manage = request.GET.get('label')
    labels_list = decode_str(pic.img_labels)
    if label_to_manage in labels_list:
        labels_list.remove(label_to_manage)
        pic.img_labels = encode_str(labels_list)
    else:
        labels_list.append(label_to_manage)
        pic.img_labels = encode_str(labels_list)
    pic.save()
    return HttpResponse(1)

def getPicLabels(request):
    imgPath = request.GET.get('path')[7:]
    pic = ImageData.objects.get(image=imgPath)
    return HttpResponse(pic.img_labels)

def labelsmanage(request):
    user = auth.get_user(request)
    request_names = request.POST.keys()
    if user.is_authenticated():
        labels = decode_str(user.labels)
        if 'createbutton' in request_names:
            newlabel = request.POST.get("newlabel")
            if ',' in newlabel:
                messages.info(request, '"," should not be included in your labels')
                return render(request, 'labelsmanage.html', {'labels':labels})
            if newlabel != '' and newlabel not in labels:
                labels.append(newlabel)
                user.labels = encode_str(labels)
                user.save()
            return render(request, 'labelsmanage.html', {'labels':labels})
        else:
            #if label is to be deleted
            for label in labels:
                if label in request_names:
                    labels.remove(label)
                    #remove label from every pic that has this label
                    all_pictures = ImageData.objects.all()
                    for pic in all_pictures:
                        if pic.username == user:
                            pic_labels = decode_str(pic.img_labels)
                            if label in pic_labels:
                                pic_labels.remove(label)
                                pic.img_labels = encode_str(pic_labels)
                                pic.save()
                    user.labels = encode_str(labels)
                    user.save()
                    return render(request, 'labelsmanage.html', {'labels':labels})
            #else nothing    
            labels = decode_str(user.labels)
            render(request, 'labelsmanage.html', {'labels':labels})
    else:
        labels = []
    return render(request, 'labelsmanage.html', {'labels':labels})    

def searchAlbum(request):
    user = auth.get_user(request)
    key = request.POST.get("searchKey")
    pics = ImageData.objects.filter(image__contains = key)
    pics_is_liked = []
    user = auth.get_user(request)
    like_list = list(map(int,decode_str(user.like_list)))
    favor_list = list(map(int,decode_str(user.favor_list)))
    for i in range(0, len(pics)):
        pics_labels = decode_str(pics[i].img_labels)
        for j in range(0, 3-len(pics_labels)):
            pics_labels.append('')
        if pics[i].id in like_list and pics[i].id in favor_list:
            pics_is_liked.append((pics[i], 1, 1, i % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
        elif pics[i].id in like_list and pics[i].id not in favor_list:
            pics_is_liked.append((pics[i], 1, 0, i % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
        elif pics[i].id not in like_list and pics[i].id in favor_list:
            pics_is_liked.append((pics[i], 0, 1, i % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
        else:
            pics_is_liked.append((pics[i], 0, 0, i % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
    labels_str = user.labels
    labels = decode_str(user.labels) 
    return render(request, 'result.html', {'pics':pics_is_liked, 'labels':labels})

def favor(request):
    user = auth.get_user(request)
    if user.is_authenticated():
        like_list = list(map(int,decode_str(user.like_list)))
        favor_list = list(map(int,decode_str(user.favor_list)))
        pics = ImageData.objects.all()
        pics_is_liked = []
        count = 0
        for i in range(0, len(pics)):
            pics_labels = decode_str(pics[i].img_labels)
            for j in range(0, 3-len(pics_labels)):
                pics_labels.append('')
            if pics[i].id in like_list and pics[i].id in favor_list:
                pics_is_liked.append((pics[i], 1, 1, count % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
                count += 1
            elif pics[i].id not in like_list and pics[i].id in favor_list:
                pics_is_liked.append((pics[i], 0, 1, count % 3, pics_labels[0], pics_labels[1], pics_labels[2]))
                count += 1

        labels_str = user.labels
        labels = decode_str(user.labels) 
        return render(request, 'favor.html', {'pics': pics_is_liked, 'labels':labels})
    else:
        return redirect('login')

def addFavor(request):
    picId = request.GET.get('picId')  #type(picId) == string  直接用string操作
    pic = ImageData.objects.get(id=picId)
    user = auth.get_user(request)
    if not user.is_authenticated():
        return HttpResponse(0)
    
    favor_list = decode_str(user.favor_list)
    if picId in favor_list:
        favor_list.remove(picId)
        user.favor_list = encode_str(favor_list)
        user.save()
        return HttpResponse(0)
    else:
        favor_list.append(picId)
        user.favor_list = encode_str(favor_list)
        user.save()
        return HttpResponse(1)

def help(request):
    return render(request, "help.html")