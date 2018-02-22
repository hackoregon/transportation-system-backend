from django.test.runner import DiscoverRunner


class UnManagedModelTestRunner(DiscoverRunner):
    """
    This class sets 'Managed=True' for models during setup of a test, and then
    subsequently reverts the model setting back to 'Managed=False' once the test
    is complete.
    """
    def setup_test_environment(self, *args, **kwargs):
        from django.apps import apps
        get_models = apps.get_models
        self.unmanaged_models = [m for m in get_models() if not m._meta.managed]
        for m in self.unmanaged_models:
            m._meta.managed = True
        super(UnManagedModelTestRunner, self).setup_test_environment(*args, **kwargs)

    def teardown_test_environment(self, *args, **kwargs):
        super(UnManagedModelTestRunner, self).teardown_test_environment(*args, **kwargs)
        for m in self.unmanaged_models:
            m._meta.managed = False