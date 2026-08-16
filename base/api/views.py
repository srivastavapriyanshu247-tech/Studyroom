from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import Roomserializer


@api_view(['GET'])
def getroutes(request):
    routes=[
        'GET/api/room',
        'GET/api/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def getrooms(request):
    rooms=Room.objects.all()
    serializer=Roomserializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getroom(request,pk):
    room=Room.objects.get(id=pk)
    serializer=Roomserializer(room,many=False)
    return Response(serializer.data)
