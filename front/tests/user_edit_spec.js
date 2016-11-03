var rp = require('request-promise');
var td_utils = require('./td-test-utils');
describe('User', function() {
    beforeEach(function() {
        jasmine.DEFAULT_TIMEOUT_INTERVAL=35000;
        this.ready_to_test = td_utils.beforeTdTest(true);        
    });

    it('edit user roles', function(done) {
        var EC = protractor.ExpectedConditions;
        this.ready_to_test.then(function(data){
            add_new_user_p = td_utils.add_new_user('poopyhead');
            user_added_p = add_new_user_p.then(function(data){
                var instance_ip = browser.params.test_instance_ip;         
                browser.get('http://'+instance_ip+':8100/#/test/app');
                return browser.sleep(3000);
            });
            ready_to_edit_p = user_added_p.then(function(data){
                $('#home_manage_user_button').click();
                return browser.wait(EC.presenceOf($('#user_edit_user_poopyhead_link')), 5000);                
            });
            ready_to_edit_p.then(function(data){
                $('#user_edit_user_poopyhead_link').click();
                return browser.wait(EC.presenceOf($('#add_user_user_info_title')), 5000);
            });
            editing_p = ready_to_edit_p.then(function(data){
                element(by.model('user_info.username')).clear();
                element(by.model('user_info.username')).sendKeys('new_poop');
                element(by.model('user_info.password')).sendKeys('new_poop_pass');
                element(by.id('add_user_role_desk_checkbox')).click();
                element(by.id('add_user_role_admin_checkbox')).click();                
                element.all(by.id('add_user_add_button')).then(function(data){
                    data[0].click();
                });
                return browser.wait(EC.presenceOf($('#GoHomeButton')), 5000);    
            });
            home_loaded_again_p = editing_p.then(function(data){
                var instance_ip = browser.params.test_instance_ip;         
                browser.get('http://'+instance_ip+':8100/#/test/app');
                return browser.sleep(3000);
            });

            ready_to_edit_again_p = home_loaded_again_p.then(function(data){
                $('#home_manage_user_button').click();
                return browser.wait(EC.presenceOf($('#user_edit_user_new_poop_link')), 5000);                
            });
            editing_p = ready_to_edit_again_p.then(function(data){
                $('#user_edit_user_new_poop_link').click();
                return browser.wait(EC.presenceOf($('#add_user_user_info_title')), 5000);
            });
            done_editing_p = editing_p.then(function(data){
                expect(element(by.model('user_info.username')).getAttribute('value')).toBe('new_poop');
                expect(element(by.id('add_user_role_desk_checkbox')).$('div').$('input').isSelected()).toBe(true);
                expect(element(by.id('add_user_role_admin_checkbox')).$('div').$('input').isSelected()).toBe(false);
                //expect()
            });
            ready_to_logout_p = done_editing_p.then(function(data){
                td_utils.reset_menu_count();
                return td_utils.open_menu();
            });
            logged_out_p = ready_to_logout_p.then(function(data){
                element(by.id('logout_link')).click();
                return browser.wait(EC.presenceOf($('#LoginAgainButton')), 5000);
            });
            logged_out_p.then(function(data){                
                return td_utils.login_through_webpage('new_poop','new_poop_pass');
            });
            browser.sleep(3000).then(function(data){
                td_utils.checkForError(false,done);
            });            
            
            
        });
    });
});
