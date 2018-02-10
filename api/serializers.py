from rest_framework import serializers
from api.models import Crash, Partic, Vhcl

class CrashSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Crash
        fields = '__all__'

class ParticSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Partic
        fields = '__all__'

class VhclSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vhcl
        fields = '__all__'