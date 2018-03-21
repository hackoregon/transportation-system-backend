from django.test import TestCase
from api.models import Crash, Partic, Vhcl

class CrashTest(TestCase):
    """ Test for Crash model """

    fixtures = ['crash_dummy_data']

    def setUp(self):
        Crash.objects.create(crash_id=1547419,crash_yr_no=2013)

    def test_crash_year(self):
        crash_one = Crash.objects.get(crash_id=1547419)
        self.assertEqual(crash_one.crash_yr_no, 2013)
    
    #check if fixtures work
    def test_loaddata(self):
        crash_load = Crash.objects.get(crash_id=1096439)
        self.assertEqual(crash_load.crash_yr_no, 2004)

class ParticTest(TestCase):
    """ Test for Partic model """

    fixtures = ['partic_dummy_data']

    def setUp(self):
        Partic.objects.create(partic_id=121221,partic_vhcl_seq_no=1)

    def test_partic_vhcl_seq_no(self):
        partic_one = Partic.objects.get(partic_id=121221)
        self.assertEqual(partic_one.partic_vhcl_seq_no, 1)
    
    def test_loaddata(self):
        partic_load = Partic.objects.get(partic_id=2380870)
        self.assertEqual(partic_load.drvr_lic_stat_cd, 1)

class VhclTest(TestCase):
    """ Test for Vhcl model """

    fixtures = ['vhcl_dummy_data']

    def setUp(self):
        Vhcl.objects.create(vhcl_id=223411,vhcl_coded_seq_no=2)

    def test_vhcl_vhcl_seq_no(self):
        vhcl_one = Vhcl.objects.get(vhcl_id=223411)
        self.assertEqual(vhcl_one.vhcl_coded_seq_no, 2)
    
    def test_loaddata(self):
        vhcl_load = Vhcl.objects.get(vhcl_id=2078725)
        self.assertEqual(vhcl_load.vhcl_cause_1_short_desc, "NO CODE ")