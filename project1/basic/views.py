from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt
from basic.models import StudentNew ,Users
from django.contrib.auth.hashers import make_password,check_password

# Create your views here.
def sample(request):
    return HttpResponse('keeru')


def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            return JsonResponse({"status": "ok","db": "connected"})
    except Exception as e:
        return JsonResponse({"status": "error","db": str(e)})



@csrf_exempt
def addStudent(request):
    print(request.method)
    if request.method == "POST":
        data=json.loads(request.body)
        student=StudentNew.objects.create(
            name=data.get('name'),
            age=data.get("age"),
            email=data.get("email")
            )
        return JsonResponse({"status":"success", "id":student.id },status=200)
    elif request.method=="GET":
        print(request.method,"hello")
        result=list(StudentNew.objects.values())
        print(result)
        return JsonResponse({"status":"ok","data":result},status=200)
    elif request.method=="PUT":
        data=json.loads(request.body)
        ref_id=data.get("id") #getting id
        new_email=data.get("email") #getting email
        existing_student=StudentNew.objects.get(id=ref_id) #fetched the object as per the id
        existing_student.email=new_email #updating with new email
        existing_student.save()
        updated_data=StudentNew.objects.filter(id=ref_id).values().first()        
        return JsonResponse({"status":"data updated successfully","updated_data":updated_data},status=200)
    elif request.method=="DELETE":
        data=json.loads(request.body)
        ref_id=data.get("id") #getting id
        get_delting_data=StudentNew.objects.filter(id=ref_id).values().first()
        to_be_delete=StudentNew.objects.get(id=ref_id)
        to_be_delete.delete()
        return JsonResponse({"status":"success","message":"student record deleted successfully","deleted data":get_delting_data},status=200)
    return JsonResponse({"error":"use post method"},status=400)

@csrf_exempt
def signup(request):
    return JsonResponse({
        "status": "success",
        "message": "User signup valid and processed"
    })

def job1(request):
    return JsonResponse({"status": "success","message": "u have successfully applied to job1"},status=200)
def job2(request):
    return JsonResponse({"status": "success","message": "u have successfully applied to job2"},status=200)

@csrf_exempt
def signUp(request):
    if request.method == "POST":
       data=json.loads(request.body)
       print(data)
       user=Users.objects.create(
            username=data.get("username"),
            email=data.get("email"),
            password=make_password(data.get("password"))
            )
       return JsonResponse({"status":"success"},status=200)

@csrf_exempt
def login(request):
    if request.method=="POST":
        data=request.POST
        print(data)
        username=data.get('username')
        password=data.get("password")
        try:
            user=Users.objects.get(username=username)
            if check_password(password,user.password):
                return JsonResponse({"status":'sucessfully loggedin'},status=200)
            else:
                return JsonResponse({"status":'failure','message':'invalid password'},status=400)
        except Users.DoesNotExist:
            return JsonResponse({"status":'failure','message':'user not found'},status=400)
        

@csrf_exempt
def check(request):
    hashed="pbkdf2_sha256$870000$1ac6psEK4vFTlAVYQmojwz$qUWbrMsfSLQ/c1ZV1yBmqKX0rtdOoeiv8wm5h0hhGVY="
    ipdata=request.POST
    print(ipdata)
    # hashed=make_password(ipdata.get("ip"))
    x=check_password(ipdata.get("ip"),hashed)
    print(x)
    return JsonResponse({"status":"success","data":x},status=200)
    
    