from api.models import Crash, Partic, Vhcl
from rest_framework.decorators import api_view, detail_route
from api.serializers import CrashSerializer, ParticSerializer, VhclSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet


class CrashViewSet(viewsets.ModelViewSet):
    """
    retrieve: Get a single Crash instance

    list: Get a list of all Crashes
    """
    queryset = Crash.objects.all()
    serializer_class = CrashSerializer
    filter_backends = (SearchFilter,DjangoFilterBackend,OrderingFilter,)
    search_fields = ('crash_id','crash_hr_short_desc','urb_area_short_nm','fc_short_desc',
                     'hwy_compnt_short_desc','mlge_typ_short_desc', 'specl_jrsdct_short_desc',
                     'jrsdct_grp_long_desc','st_full_nm','isect_st_full_nm','rd_char_short_desc',
                     'isect_typ_short_desc','crash_typ_short_desc','collis_typ_short_desc',
                     'rd_cntl_med_desc','wthr_cond_short_desc','rd_surf_short_desc','lgt_cond_short_desc',
                     'traf_cntl_device_short_desc','invstg_agy_short_desc','crash_cause_1_short_desc',
                     'crash_cause_2_short_desc','crash_cause_3_short_desc','pop_rng_med_desc','rd_cntl_med_desc')
    filter_fields = ('ser_no','cnty_id','alchl_invlv_flg','crash_day_no','crash_mo_no','crash_yr_no','crash_hr_no',
                    'schl_zone_ind','wrk_zone_ind','alchl_invlv_flg','drug_invlv_flg','crash_speed_invlv_flg',
                    'crash_hit_run_flg',)
    ordering_fields = '__all__'

class ParticViewSet(viewsets.ModelViewSet):
    """
    retrieve: Get a single Participant instance

    list: Get a list of all Participants
    """
    queryset = Partic.objects.all()
    serializer_class = ParticSerializer
    filter_backends = (SearchFilter,DjangoFilterBackend,OrderingFilter,)
    search_fields = ('partic_typ_short_desc','drvr_lic_stat_short_desc',
    'drvr_res_short_desc','inj_svrty_short_desc','sfty_equip_use_short_desc',
    'mvmnt_short_desc','partic_cmpss_dir_from_short_desc',
    'partic_cmpss_dir_to_short_desc','non_motrst_loc_short_desc','actn_short_desc',
    'partic_err_1_short_desc','partic_err_2_short_desc','partic_err_3_short_desc',
    'partic_cause_1_short_desc','partic_cause_2_short_desc','partic_cause_3_short_desc',
    'partic_evnt_1_short_desc','partic_evnt_2_short_desc','partic_evnt_3_short_desc')
    filter_fields = ('crash_id','vhcl_id','partic_dsply_seq_no','vhcl_coded_seq_no','partic_vhcl_seq_no',
    'partic_typ_cd','partic_hit_run_flg','pub_empl_flg','sex_cd','age_val','drvr_lic_stat_cd',
    'drvr_res_stat_cd','inj_svrty_cd','sfty_equip_use_cd','airbag_deploy_ind','mvmnt_cd',
    'cmpss_dir_from_cd','cmpss_dir_to_cd','non_motrst_loc_cd','actn_cd','partic_err_1_cd',
    'partic_err_2_cd','partic_err_3_cd','partic_cause_1_cd','partic_cause_2_cd','partic_cause_3_cd',
    'partic_evnt_1_cd','partic_evnt_2_cd','partic_evnt_3_cd','bac_val','alchl_use_rpt_ind',
    'drug_use_rpt_ind','strikg_partic_flg')
    ordering_fields = '__all__'

class VhclViewSet(viewsets.ModelViewSet):
    """
    This endpoint shows all vehicles.

    retrieve: Get a single Vehicle instance

    list: Get a list of all Vehicles
    """

    queryset = Vhcl.objects.all()
    serializer_class = VhclSerializer
    filter_backends = (SearchFilter,DjangoFilterBackend,OrderingFilter,)
    search_fields = ('vhcl_ownshp_short_desc','vhcl_use_short_desc',
    'vhcl_typ_short_desc','mvmnt_short_desc','vhcl_cmpss_dir_from_short_desc',
    'vhcl_cmpss_dir_to_short_desc','actn_short_desc','vhcl_cause_1_short_desc',
    'vhcl_cause_2_short_desc','vhcl_cause_3_short_desc','vhcl_evnt_1_short_desc',
    'vhcl_evnt_2_short_desc','vhcl_evnt_3_short_desc')
    filter_fields = ('vhcl_id','crash_id','vhcl_coded_seq_no','vhcl_ownshp_cd',
    'vhcl_use_cd','vhcl_typ_cd','emrgcy_vhcl_use_flg','trlr_qty','mvmnt_cd',
    'cmpss_dir_from_cd','cmpss_dir_to_cd','actn_cd','vhcl_cause_1_cd','vhcl_cause_2_cd',
    'vhcl_cause_3_cd','vhcl_evnt_1_cd','vhcl_evnt_2_cd','vhcl_evnt_3_cd',
    'vhcl_speed_flg','vhcl_hit_run_flg','vhcl_sfty_equip_used_qty',
    'vhcl_sfty_equip_unused_qty','vhcl_sfty_equip_use_unknwn_qty','vhcl_occup_cnt',
    'strikg_vhcl_flg')
    ordering_fields = '__all__'
