import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from users.serializers import UserSerializer, LoginSerializer
from django.contrib.auth import authenticate 
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import redirect, render

logger = logging.getLogger(__name__)
# Login view
@api_view(['POST'])
@permission_classes([AllowAny])
def get_login(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Authenticate user
        user = authenticate(request , username=username, password=password)

        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Return the tokens in the response (no redirect)
            return Response({
                'access': access_token,
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@login_required   
def home(request):
    return render(request, 'index.html')

@api_view(['POST'])
@permission_classes([AllowAny])
def get_register(request):
    # Deserialize the request data using the UserSerializer
    serializer = UserSerializer(data=request.data)

    # Validate the incoming data
    if serializer.is_valid():
        # Save the new user to the database
        serializer.save()

        # Return a success response
        return Response({'detail': 'Registration successful'}, status=status.HTTP_201_CREATED)

    # If the data is invalid, return an error response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Only authenticated users can access their profile
def get_profile(request):
    user = request.user  # Get the logged-in user
    logger.info(f"Authenticated user: {user.username}")  # Log authenticated user
    # Format the `date_joined` as YYYY-MM-DD
    joined_date = user.date_joined.strftime('%Y-%m-%d')
    user_data = {
        'username': user.username,
        'email': user.email,
        'score': user.score,
        'wins': user.wins,
        'losses': user.losses,
        'draws': user.draws,
        'joined_date': user.date_joined,
    }
    return Response(user_data)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_leaderboard(request):
    # Get users sorted by their Elo rating or score
    users = User.objects.all().order_by('-score')[:4]  # Adjust the number (e.g., top 10)
    
    # Prepare the response data
    leaderboard_data = [{
        'username': user.username,
        'score': user.score,
        'email': user.email,
    } for user in users]
    
    return Response({'leaderboard': leaderboard_data})
    
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer    
    
    
