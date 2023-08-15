from rest_framework.serializers import ModelSerializer
from base.models import Room,Message, User
from rest_framework import serializers

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "avatar","username",]
        
class MessageSerializer(ModelSerializer):
    room = RoomSerializer()
    user = UserSerializer()
    
    created_timesince = serializers.CharField(source='created', read_only=True)
    class Meta:
        model = Message
        fields = "__all__"
        