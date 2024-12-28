from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import User, Train, Booking
from .serializers import UserSerializer, TrainSerializer, BookingSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

ADMIN_API_KEY = settings.ADMIN_API_KEY

def check_admin_api_key(request):
    api_key = request.headers.get('API_KEY')
    if api_key != ADMIN_API_KEY:
        return Response({'error': 'Unauthorized'}, status=403)
    return None

# Register
@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Generate tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Login
@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()

        if user and check_password(password, user.password):
            is_admin = user.is_admin
            tokens = get_tokens_for_user(user)
            return JsonResponse({
                "username": user.username,
                "is_admin": is_admin,
                "token": tokens['access'],
                "message": "Login successful"
            }, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)

#Add train
@api_view(['POST'])
def add_train(request):
    api_key_check = check_admin_api_key(request)
    if api_key_check:
        return api_key_check 

    if request.method == 'POST':
        train_data = request.data
        try:
            train = Train.objects.create(
                train_name=train_data['train_name'],
                source=train_data['source'],
                destination=train_data['destination'],
                total_seats=train_data['total_seats'],
                available_seats=train_data['total_seats'],
            )
            return Response({'message': 'Train added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Seat availability
@api_view(['GET'])
def get_seat_availability(request, source, destination):
    trains = Train.objects.filter(source=source, destination=destination)
    serializer = TrainSerializer(trains, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Book seat
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_seat(request, train_id):
    user = request.user
    train = Train.objects.get(id=train_id)
    
    if train.available_seats > 0:
        with transaction.atomic():
            train.available_seats -= 1
            train.save()
            booking = Booking.objects.create(user=user, train=train)
        
        return Response({'message': 'Booking successful'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'No available seats'}, status=status.HTTP_400_BAD_REQUEST)


# Booking details
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_booking_details(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if booking.user == request.user:
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)
