from rest_framework import serializers
from game.models import Game
from users.models import User
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # You can add more fields if needed

class GameSerializer(serializers.ModelSerializer):
    white_player = UserSerializer()  # Nest the User serializer to get full user data
    black_player = UserSerializer(required=False, allow_null=True)  # Optional black player
    
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
        Also, we'll format the `created_at` and `updated_at` dates for better readability.
        """
        representation = super().to_representation(instance)

        # Format the `created_at` and `updated_at` fields as strings
        representation['created_at'] = instance.created_at.strftime('%Y-%m-%d %H:%M:%S')
        representation['updated_at'] = instance.updated_at.strftime('%Y-%m-%d %H:%M:%S')

        # Adjust the serialization of white_player and black_player to return user details
        representation['white_player'] = UserSerializer(instance.white_player).data
        if instance.black_player:
            representation['black_player'] = UserSerializer(instance.black_player).data

        return representation