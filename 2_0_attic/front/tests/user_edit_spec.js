var rp = require('request-promise');
var td_utils = require('./td-test-utils');

describe('User', function() {
    beforeEach(function() {        
        td_utils.beforeTdTestEx(true);        
    });

    it('edit user', function() {
        var EC = protractor.ExpectedConditions;
        var instance_ip = browser.params.test_instance_ip;
        new_user_name='poopyhead';
        changed_user_name='new_poop';
        changed_user_pass='new_poop_pass';
        td_utils.add_new_user_ex(new_user_name);
        browser.get('http://'+instance_ip+':8100/#/test/app');
        element(by.id('home_manage_user_button')).click();
        element(by.id('user_edit_user_'+new_user_name+'_link')).click();        
        element(by.model('user_info.username')).clear();
        element(by.model('user_info.username')).sendKeys(changed_user_name);
        element(by.model('user_info.password')).sendKeys(changed_user_pass);
        element(by.id('add_user_role_desk_checkbox')).click();
        element(by.id('add_user_role_admin_checkbox')).click();                
        el = element(by.id("add_user_add_button"));
        browser.executeScript("arguments[0].scrollIntoView(true)", el);
        element(by.id('add_user_add_button')).click();            
        td_utils.checkForError(false);
        element(by.id('GoHomeButton')).click();            
        element(by.id('home_manage_user_button')).click();
        element(by.id('user_edit_user_'+changed_user_name+'_link')).click();        
        expect(element(by.model('user_info.username')).getAttribute('value')).toBe('new_poop');
        expect(element(by.id('add_user_role_desk_checkbox')).$('div').$('input').isSelected()).toBe(true);
        expect(element(by.id('add_user_role_admin_checkbox')).$('div').$('input').isSelected()).toBe(false);
        td_utils.open_menu_ex();
        element(by.id('logout_link')).click();
        td_utils.login_through_webpage_ex(changed_user_name,changed_user_pass);
        td_utils.checkForError(false);
    },60000);
});
