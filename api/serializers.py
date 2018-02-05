from rest_framework import serializers
from api.models import Crash, Partic, Vhcl


class CrashSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Crash
        fields = ('crash_id', 'crash_dt', 'cnty_id', 'crash_cause_1_short_desc')