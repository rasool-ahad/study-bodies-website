from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]

    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serlizer = RoomSerializer(rooms, many = True)
    return Response(serlizer.data)


@api_view(['GET'])
def getRooms(request,id):
    room = Room.objects.get(id= id)
    serlizer = RoomSerializer(room)
    return Response(serlizer.data)