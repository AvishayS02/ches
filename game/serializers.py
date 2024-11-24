from rest_framework import serializers
from game.models import Game
from users.models import User

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
        white_player = validated_data['white_player']
        black_player = validated_data.get('black_player', None)  # Make black_player optional
        
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
        """
        representation = super().to_representation(instance)
        # Adjust the serialization of white_player and black_player to return user IDs
        representation['white_player'] = UserSerializer(instance.white_player).data
        if instance.black_player:
            representation['black_player'] = UserSerializer(instance.black_player).data
        return representation
