var rp = require('request-promise');
var td_utils = require('./td-test-utils');
describe('User', function() {
    beforeEach(function() {
        this.ready_to_test = td_utils.beforeTdTest(true);        
    });
    it('add user', function(done) {
        var EC = protractor.ExpectedConditions;
        this.ready_to_test.then(function(data){
             td_utils.add_new_user('poopyhead').then(function(data){
                 td_utils.checkForError(false,done);
             });
         });
     });
    it('new user login', function(done) {        
        var EC = protractor.ExpectedConditions;
        this.ready_to_test.then(function(data){
            add_new_user_p = td_utils.add_new_user('poopyhead');
            ready_to_logout_p = add_new_user_p.then(function(data){
                return td_utils.open_menu();
            });
            logged_out_p = ready_to_logout_p.then(function(data){
                element(by.id('logout_link')).click();
                return browser.wait(EC.presenceOf($('#LoginAgainButton')), 5000);
            });
            logged_out_p.then(function(data){                
                return td_utils.login_through_webpage('poopyhead','poopyhead');
            });
            browser.sleep(3000).then(function(data){
                td_utils.checkForError(false,done);
            });            
        });
    });        
});
