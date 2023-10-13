from django.http import FileResponse
from django.http import HttpResponse
from django.shortcuts import render
from pytube import YouTube
from os.path import exists
import time
import os
import re
from django.http import JsonResponse
from django.core.mail import BadHeaderError, EmailMessage
from django.shortcuts import render, redirect
from django.http import HttpResponse


# Create your views here.
def home(request):
    return render(request,'index.html')


def clearolderfiles(path):
    deletepath = "media\\"+path    
    if exists(deletepath):          
        for folder in os.listdir(deletepath):                                
            modifiedtime=os.path.getmtime(os.path.abspath(deletepath+"\\"+folder))          
            if time.time()-modifiedtime > 300:
                for file in os.listdir(deletepath+"\\"+folder):
                    os.remove(os.path.abspath(deletepath+"\\"+folder+"\\"+file))
                os.rmdir(os.path.abspath(deletepath+"\\"+folder))  
                

def downloadmp4(request):
    clearolderfiles("videofiles")
    my_new_path ="media\\videofiles\\"+re.sub('[^a-zA-Z0-9 \n\.]', '', request.POST["addressmp4"])
    if exists(my_new_path):          
        for file in os.listdir(my_new_path):
            if file.endswith(".mp4"):
                    audiofile = open(my_new_path+"\\"+file, "rb").read() 
                    response = HttpResponse(audiofile, content_type='application/vnd.mp4')
                    response['Content-Disposition'] = 'attachment; filename=' + file
    else:
        yt = YouTube(str(request.POST["addressmp4"]))
        video = yt.streams.get_highest_resolution()
        # download the file        
        out_file = video.download(output_path=my_new_path)
        for file in os.listdir(my_new_path):
            if file.endswith(".mp4"):
                    audiofile = open(my_new_path+"\\"+file, "rb").read() 
                    response = HttpResponse(audiofile, content_type='application/vnd.mp4')
                    response['Content-Disposition'] = 'attachment; filename=' + file
    return response

