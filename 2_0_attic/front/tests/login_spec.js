var rp = require('request-promise');
var td_utils = require('./td-test-utils');
describe('Auth', function() {
    var isUserLoggedIn = function(expectation,user){
        var instance_ip = browser.params.test_instance_ip;

        cookie_promise = browser.manage().getCookie('session');
        current_user_options_promise = cookie_promise.then(function(cookie_data){
            if(cookie_data != null){
                cookie_data_string = cookie_data.value;
            } else {
                cookie_data_string = '';
            }
            options = {
                uri: "http://"+instance_ip+":8000/test/auth/current_user",
                headers: {
                    'Cookie': 'session='+cookie_data_string
                },
                json: true // Automatically parses the JSON string in the response
            };
            return options;
        });
        
        rp_promise = current_user_options_promise.then(function(data){                                    
            return rp(data)
                .then(function (result) {
                    if(result.data != null){
                        expect(result.data.username == user.username).toBe(true);
                    } else {
                        expect(expectation).toEqual(false);
                    }                                                        
                })
                .catch(function (err) {
                    // test_done();
                    // API call failed...
                });       
        });
        browser.wait(rp_promise,10000);
    };
    
    beforeEach(function() {                
        td_utils.beforeTdTestEx();
    });
    
    it('current user should be null when not logged in', function() {        
        isUserLoggedIn(false);        
    });    
    
    it('login link should be available when logged out', function() {        
        td_utils.open_menu_ex();
        expect(element(by.id('logout_link')).isPresent()).toBe(false);        
        expect(element(by.id('login_link')).isDisplayed()).toBe(true);        
    });
    
    it('should be able to login', function() {
        var EC = protractor.ExpectedConditions;
        td_utils.login_through_webpage_ex('test_admin','test_admin');                
        td_utils.checkForError(false);
        expect(element(by.className('icon-label')).isDisplayed()).toEqual(true);
        isUserLoggedIn(true, {username:'test_admin'});        
    });

    it('should not be able to login with bad credentials', function() {
        var EC = protractor.ExpectedConditions;
        td_utils.login_through_webpage_ex('test_admin','test_admin2');                
        td_utils.checkForError(true);        
        isUserLoggedIn(false, {username:'test_admin'});        
    });

    
    it('should be able to logout', function() {        
        var EC = protractor.ExpectedConditions;
        td_utils.login_through_webpage_ex('test_admin','test_admin');
        browser.wait(EC.presenceOf($('.icon-label')), 5000);
        td_utils.open_menu_ex();
        element(by.id('logout_link')).click();
        browser.wait(EC.presenceOf($('.icon-label')), 5000);        
        expect(element(by.className('icon-label')).isDisplayed()).toEqual(true);
        td_utils.checkForError(false);
        isUserLoggedIn(false, {username:'test_admin'});        
    });
    
});    

