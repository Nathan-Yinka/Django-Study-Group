from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RoomSerializer,MessageSerializer
from base.models import Room
from django.utils.timesince import timesince
from datetime import datetime

@api_view(["GET"])
def getRoutes(request):
    data = [
        "GET /api/",
        'GET /api/rooms',
        "GET /api/rooms/:id"
    ]
    return Response(data)

@api_view(["GET"])
def getRoom(request):
    room = Room.objects.all()
    rooms = RoomSerializer(room,many = True)
    return Response(rooms.data)

@api_view(["GET"])
def getRoomValue(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    
    for message in room_messages:
        created_time = message.created
        now = datetime.now(created_time.tzinfo)
        time_difference = now - created_time

        # Convert time_difference to a human-readable format "YYYY-MM-DD HH:mm:ss"
        created_timesince = (now - time_difference).strftime('%Y-%m-%d %H:%M:%S')

        message.created_timesince = created_timesince

        
    room_messages = MessageSerializer(room_messages, many=True)
    return Response(room_messages.data)
    
