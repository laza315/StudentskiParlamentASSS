from rest_framework.decorators import api_view
from rest_framework.response import Response
from anketa.models import Anketa
from .serializers import AnketaSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api/',
        'GET /api/ankete',
        'GET /api/results/:host_id'
    ]
    return Response(routes)

@api_view(['GET'])
def getLiveAnkete(request):
    live_ankete = Anketa.objects.filter(aktivnost=True).all()

    if not live_ankete:
        return Response({"message": "Нема активних Анкета"}, status=404)

    serializer = AnketaSerializer(live_ankete, many=True)
    return Response(serializer.data)
