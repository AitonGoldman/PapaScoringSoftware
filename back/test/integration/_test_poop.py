import pss_integration_test_base
class AllDone(pss_integration_test_base.PssIntegrationTestBase):
    def setUp(self):
        super(AllDone,self).setUp()        
        
    def test_all_done(self):
        db_url = self.pss_config.get_db_info().generate_db_url()                
        print "db url is %s" % db_url
        drop_database(db_url)
        print "poop"
