from django.http import HttpResponseRedirect
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .serislizers import *
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework import viewsets, status
from .models import User
from rest_framework import serializers
from django.shortcuts import render
from django.contrib.auth.hashers import check_password, make_password
from django.core import serializers
from django.http import HttpResponse
from rest_framework.generics import UpdateAPIView
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView
from rest_framework.decorators import api_view
from .models import *
from django.core.mail import send_mail
from django.conf import settings
import reportlab
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas



class RegisterView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        users = User.objects.all()
        if len(data['password']) < 8:
            return JsonResponse({"Error": "Password is too short"}, status=400)
        if "@" not in data['email']:
            return JsonResponse({"Error": "Email must contain '@'"}, status=400)
        for var in users:
            if var.email == data['email']:
                return JsonResponse({"Error": "User already exists"}, status=401)
        data['password'] = make_password(data['password'], salt=None, hasher="default")
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"Info": "OK"}, status=200)
        return JsonResponse({"Error": "Error while registering new user!"}, status=402)


class LoginView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        users = User.objects.all()
        if len(data['password']) < 8:
            return JsonResponse({"Error": "Password is too short"}, status=400)
        if "@" not in data['email']:
            return JsonResponse({"Error": "Email must contain '@'"}, status=400)
        for var in users:
            if var.email == data['email']:
                if checkpassword(data, User.objects.all()):
                    return JsonResponse({"ID": var.pk, "Is_Admin": var.is_admin}, status=200)
        return JsonResponse({"Error": "Incorrect password or email!"}, status=400)


class AddCarView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        cars = Car.objects.all()
        if len(data['VIN']) != 17:
            return JsonResponse({"Error": "VIN must consist of 17 characters!"})
        if "Q" in data['VIN'] or "I" in data['VIN'] or "O" in data['VIN']:
            return JsonResponse({"Error": "VIN number can't include I and O and Q characters!"})
        for var in cars:
            if var.VIN == data['VIN'].upper():
                return JsonResponse({"Error": "Car with this VIN number already exists"}, status=400)
        data['VIN'] = data['VIN'].upper()
        serializer = CarSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"Info": "Car added successfully!"}, status=200)
        return JsonResponse({"Error": "Car not added!"}, status=401)

class UserViewPK(APIView):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(instance=user)
        if serializer.data is not None:
            return JsonResponse(serializer.data, status=200)
        return JsonResponse({"Error": "error"}, status=400)


class UserListView(APIView):
    def get(self, request):
                return JsonResponse(
                    {"users": list(User.objects.filter(is_admin=False).values())},
                    safe=False, status=200)


class CarViewPK(APIView):
    def get(self, request, pk):
        car = Car.objects.get(pk=pk)
        serializer = CarSerializer(instance=car)
        if serializer.data is not None:
            return JsonResponse(serializer.data, status=200)
        return JsonResponse({"Error": "error"}, status=400)

    def patch(self, request, pk):
        data = JSONParser().parse(request)
        car = Car.objects.get(pk=pk)
        serializer = CarSerializer(car, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"Info": "Edit ok!"}, status=200)
        return JsonResponse(serializer.errors, status=400)


class CarListView(APIView):
    def get(self, request, pk):
        return JsonResponse({"cars": list(Car.objects.filter(userID=pk).values())}, safe=False, status=200)


class ServiceViewPK(APIView):
    def get(self, request, pk):
        service = Service.objects.get(pk=pk)
        serializer = ServiceSerializer(instance=service)
        if serializer.data is not None:
            return JsonResponse(serializer.data, status=200)
        return JsonResponse({"Error": "error"}, status=400)

    def patch(self, request, pk):
        data = JSONParser().parse(request)
        service = Service.objects.get(pk=pk)
        serializer = ServiceSerializer(service, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"Info": "OK"}, status=200)
        return JsonResponse({"Error:": serializer.errors}, status=400)


class ServiceListView(APIView):
    def get(self, request, pk):
        return JsonResponse({"services": list(Service.objects.filter(userID=pk, is_finished=True).values())}, safe=False, status=200)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = ServiceSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"Info": "Ok"}, status=200)
        return JsonResponse(serializer.errors, status=400)

class ServiceListViewPresent(APIView):
    def get(self, request, pk):
        return JsonResponse({"services": list(Service.objects.filter(userID=pk, is_accepted=True, is_finished=False).values())}, safe=False, status=200)


def checkpassword(data, user):
    users = User.objects.all()
    for var in users:
        if var.email == data['email']:
            if check_password(data['password'], var.password):
                return True
            return False


class Addpart(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = Invoiceserializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"Info": "OK"}, status=200)
        return JsonResponse(serializer.errors, status=400)


class Getparts(APIView):
    def get(self, request, pk):
        return JsonResponse({"jobs": list(Invoice.objects.filter(serviceID=pk).values())}, safe=False, status=200)


class AdminServiceReservation(APIView):
    def get(self, request):
        return JsonResponse({"services": list(Service.objects.filter(is_accepted=False).values())}, safe=False, status=200)


class AdminServiceInProgress(APIView):
    def get(self, request):
        return JsonResponse({"services": list(Service.objects.filter(is_accepted=True, is_finished=False).values())}, safe=False, status=200)


class AdminServiceFinishedView(APIView):
    def get(self, request):
        return JsonResponse({"services": list(Service.objects.filter(is_finished=True).values())}, safe=False, status=200)


class AdminServiceAllView(APIView):
    def get(self, request, pk):
        return JsonResponse({"services": list(Service.objects.filter().values())}, safe=False, status=200)


class Email(APIView):
    def post(self, request, pk):
        service = Service.objects.get(pk=pk)
        car = Car.objects.get(pk=service.carID)
        user = User.objects.get(pk=service.userID)
        prize = str(service.total_prize)
        subject = 'Autoservice G&G- Informcja o Aucie'
        message = "Dzień dobry, chcielibyśmy poinformować że auto o nr VIN " + car.VIN + " jest dostępne do odbioru w " \
                    "warsztacie. Kwota jaką należy przygotować wynosi " + prize +" zł. \n Pozdrawiamy, autoservice G&G "
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail(subject, message, email_from, recipient_list)
        return JsonResponse({"Info": "email send!"}, status=200)


class EmailAccept(APIView):
    def patch(self, request, pk):
        data = JSONParser().parse(request)
        service = Service.objects.get(pk=pk)
        car = Car.objects.get(pk=service.carID)
        user = User.objects.get(pk=service.userID)
        subject = 'Autoservice G&G- Akceptacja Rezerwacji'
        message = "Dzień dobry, chcielibyśmy poinformować że rezerwacja serwisu auta o nr VIN " + car.VIN + "została " \
                    "zaakceptowana. Prosimy o teminowe stawienie się na wizytę.\n Pozdrawiamy, autoservice G&G "
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail(subject, message, email_from, recipient_list)
        serializer = ServiceSerializer(service, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if not serializer.is_valid():
                return JsonResponse({"Error": serializer.errors}, status=400)
        return JsonResponse({"Info": "OK"}, status=200)




