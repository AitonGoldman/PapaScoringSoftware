import pss_integration_test_base
from sqlalchemy_utils import drop_database
from lib.PssConfig import PssConfig
class AllDone(pss_integration_test_base.PssIntegrationTestBase):        
    def test_all_done(self):
        db_url = PssConfig().get_db_info().generate_db_url()                        
        drop_database(db_url)
        
                     
