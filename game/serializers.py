from rest_framework import serializers
from game.models import Game
from users.models import User
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # You can add more fields if needed

class GameSerializer(serializers.ModelSerializer):
    white_player = UserSerializer()  
    black_player = UserSerializer(required=False, allow_null=True)  
    
    class Meta:
        model = Game
        fields = ['id', 'white_player', 'black_player', 'moves', 'result', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Extract white player and black player from validated data
        white_player_data = validated_data['white_player']
        black_player_data = validated_data.get('black_player', None)  # Make black_player optional

        # Get the actual User instances
        white_player = User.objects.get(id=white_player_data['id'])
        black_player = None
        if black_player_data:
            black_player = User.objects.get(id=black_player_data['id'])

        # Create a new Game object
        game = Game.objects.create(
            white_player=white_player,
            black_player=black_player,
            result='Pending'  # Default result is 'Pending'
        )
        return game

    def to_representation(self, instance):
        """
        This will modify the representation of the game instance to include the user details
        in the proper format (i.e., returning the `id`, `username`, `email` of the user).
        Also, we'll leave the `created_at` and `updated_at` dates in ISO 8601 format.
        """
        representation = super().to_representation(instance)

        # Use ISO 8601 format for created_at and updated_at (no manual formatting needed)
        representation['created_at'] = instance.created_at.isoformat()
        representation['updated_at'] = instance.updated_at.isoformat()

        # Adjust the serialization of white_player and black_player to return user details
        representation['white_player'] = UserSerializer(instance.white_player).data
        if instance.black_player:
            representation['black_player'] = UserSerializer(instance.black_player).data

        return representation
