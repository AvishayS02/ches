from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from game.models import Game
from game.serializers import GameSerializer
from users.models import User
from rest_framework.permissions import IsAuthenticated

# View for starting a game
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_game(request):
    user = request.user
    opponent_id = request.data.get('opponent_id')

    try:
        opponent = User.objects.get(id=opponent_id)
    except User.DoesNotExist:
        return Response({'error': 'Opponent not found'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new game (both white and black players)
    game = Game.objects.create(white_player=user, black_player=opponent, result='Pending')

    return Response({'game_id': game.id, 'white_player': game.white_player.username, 'black_player': game.black_player.username}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_opponents(request):
    user = request.user
    users = User.objects.exclude(id=user.id)  # Exclude logged-in user
    opponent_list = [{'id': user.id, 'username': user.username} for user in users]
    return Response(opponent_list, status=status.HTTP_200_OK)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_score(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)

    result = request.data.get('result')  # The result could be "White", "Black", or "Draw"
    if result not in ['White', 'Black', 'Draw']:
        return Response({'error': 'Invalid result'}, status=status.HTTP_400_BAD_REQUEST)

    # Update game result
    game.result = result
    game.save()

    # Update player scores
    if result == 'White':
        game.white_player.score += 10  # Award 10 points for a win
        game.white_player.wins += 1
        game.black_player.score -= 10  # Deduct 10 points for a loss
        game.black_player.losses += 1
    elif result == 'Black':
        game.black_player.score += 10  # Award 10 points for a win
        game.black_player.wins += 1
        game.white_player.score -= 10  # Deduct 10 points for a loss
        game.white_player.losses += 1
    elif result == 'Draw':
        game.white_player.score += 5  # Award 5 points for a draw
        game.black_player.score += 5  # Award 5 points for a draw
        game.white_player.draws += 1
        game.black_player.draws += 1

    # Save updated score and record the results
    game.white_player.save()
    game.black_player.save()

    return Response({'msg': 'Game result and scores updated'}, status=status.HTTP_200_OK)

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Game

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def game_history(request):
    # Get all games where the current user is either the white or black player
    games_as_white = Game.objects.filter(white_player=request.user)
    games_as_black = Game.objects.filter(black_player=request.user)
    
    # Combine both querysets
    games = games_as_white | games_as_black
    
    # Create the game list to return
    game_list = [{
        "opponent": game.black_player.username if game.white_player == request.user else game.white_player.username,
        "result": game.result,
        "date": game.created_at,
        "color_played": "White" if game.white_player == request.user else "Black",
        "white_player": game.white_player.username,  # Add white player info
        "black_player": game.black_player.username,  # Add black player info
        "game_date": game.created_at.strftime("%d/%m/%Y")  # Formatted game date
    } for game in games]
    
    return Response({"games": game_list})