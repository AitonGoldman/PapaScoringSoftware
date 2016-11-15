var rp = require('request-promise');
var td_utils = require('./td-test-utils');
describe('User', function() {
    beforeEach(function() {
        td_utils.beforeTdTestEx(true);        
    });
    it('add user', function() {
        new_user_name='poopyhead';
        var EC = protractor.ExpectedConditions;
        td_utils.add_new_user_ex(new_user_name,false);        
        td_utils.checkForError(false);
        element(by.id('AddAnotherUser')).click();
        //browser.wait(EC.presenceOf($('#user_edit_user_'+new_user_name+'_link')), 5000);
        expect(element(by.id('user_edit_user_'+new_user_name+'_link')).isPresent()).toBe(true);
    });
    
    it('new user login', function() {        
        var EC = protractor.ExpectedConditions;
        new_user_name='poopyhead2';
        td_utils.add_new_user(new_user_name,true);
        td_utils.open_menu_ex();
        element(by.id('logout_link')).click();
        td_utils.login_through_webpage_ex(new_user_name,new_user_name);
        td_utils.checkForError(false);
    });        
});
