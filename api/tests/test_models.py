from django.test import TestCase
from api.models import Crash, Partic, Vhcl

class CrashTest(TestCase):
    """ Test for Crash model """

    def setUp(self):
        Crash.objects.create(crash_id=1547419,crash_yr_no=2013)

    def test_crash_year(self):
        crash_one = Crash.objects.get(crash_id=1547419)
        self.assertEqual(crash_one.crash_yr_no, 2013)
    
    #check if fixtures work
    def test_loaddata(self):
        crash_load = Crash.objects.get(crash_id=1096439)
        self.assertEqual(crash_load.crash_yr_no, 2004)