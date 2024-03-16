from rest_framework.serializers import ModelSerializer
from anketa.models import Anketa

class AnketaSerializer(ModelSerializer):
    class Meta:
        model = Anketa
        fields = '__all__'