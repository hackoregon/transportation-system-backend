from api.models import Crash, Partic, Vhcl
from rest_framework.decorators import api_view, detail_route
from api.serializers import CrashSerializer, ParticSerializer, VhclSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class CrashViewSet(viewsets.ModelViewSet):
    
    queryset = Crash.objects.all()
    serializer_class = CrashSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('crash_id','crash_hr_short_desc','urb_area_short_nm','fc_short_desc',
                     'hwy_compnt_short_desc','mlge_typ_short_desc', 'specl_jrsdct_short_desc',
                     'jrsdct_grp_long_desc','st_full_nm','isect_st_full_nm','rd_char_short_desc',
                     'isect_typ_short_desc','crash_typ_short_desc','collis_typ_short_desc',
                     'rd_cntl_med_desc','wthr_cond_short_desc','rd_surf_short_desc','lgt_cond_short_desc',
                     'traf_cntl_device_short_desc','invstg_agy_short_desc','crash_cause_1_short_desc',
                     'crash_cause_2_short_desc','crash_cause_3_short_desc','pop_rng_med_desc','rd_cntl_med_desc')

class ParticViewSet(viewsets.ModelViewSet):

    queryset = Partic.objects.all()
    serializer_class = ParticSerializer

class VhclViewSet(viewsets.ModelViewSet):

    queryset = Vhcl.objects.all()
    serializer_class = VhclSerializer
