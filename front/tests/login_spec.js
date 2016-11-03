var rp = require('request-promise');
var td_utils = require('./td-test-utils');
describe('Auth', function() {
    var isUserLoggedIn = function(expectation,user){
        var instance_ip = browser.params.test_instance_ip;

        cookie_promise = browser.manage().getCookie('session').then(function(data){
            return data;
        });
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
        
        return current_user_options_promise.then(function(data){                                    
            return rp(data)
                .then(function (result) {
                    if(result.data != null){                        
                        expect(result.data.username == user.username).toBe(true);                                                
                    } else {
                        expect(expectation).toEqual(false);                                                                                     }                                                        
                })
                .catch(function (err) {
                    // test_done();
                    // API call failed...
                });       
        });        
    };            
    beforeEach(function() {                
        this.ready_to_test = td_utils.beforeTdTest();
    });
    
    it('current user should be null when not logged in', function(done) {        
        this.ready_to_test.then(function(data){            
            isUserLoggedIn(false).then(function(data){
                done();
            });            
        });        
    });    
    
    it('login link should be available when logged out', function(done) {        
        this.ready_to_test.then(function(data){
            td_utils.open_menu().then(function(data){
                expect(element(by.id('logout_link')).isPresent()).toBe(false);        
                expect(element(by.id('login_link')).isDisplayed()).toBe(true);
            done();
            });
        });
    });
    
    it('should be able to login', function(done) {
        this.ready_to_test.then(function(data){
            var EC = protractor.ExpectedConditions;
            login_p = td_utils.login_through_webpage('test_admin','test_admin');
            logged_in_p = browser.wait(EC.visibilityOf($('.icon-label')), 25000);
            logged_in_p.then(function(data){
                expect(element(by.className('icon-label')).isDisplayed()).toEqual(true);
                //expect(element(by.id('error_present')).isPresent()).toBe(false);                                
                rest_logged_in_p = isUserLoggedIn(true, {username:'test_admin'});
                rest_logged_in_p.then(function(data){
                    td_utils.checkForError(false,done);
                });
                
            });
        });
    });

    it('should not be able to login with bad credentials', function(done) {
        this.ready_to_test.then(function(data){
            var EC = protractor.ExpectedConditions;
            login_p = td_utils.login_through_webpage('test_admin','test_admin2');
            logged_in_p = browser.wait(EC.visibilityOf($('.icon-label')), 25000);
            logged_in_p.then(function(data){
                expect(element(by.className('icon-label')).isDisplayed()).toEqual(true);
                //expect(element(by.id('error_present')).isPresent()).toBe(false);                                
                rest_logged_in_p = isUserLoggedIn(false, {username:'test_admin'});
                rest_logged_in_p.then(function(data){
                    td_utils.checkForError(true,done);
                });
                
            });
        });
    });

    
    it('should be able to logout', function(done) {        
        this.ready_to_test.then(function(data){
            var EC = protractor.ExpectedConditions;
            logged_in_p = td_utils.login_through_webpage('test_admin','test_admin').then(function(data){
                return browser.wait(EC.presenceOf($('.icon-label')), 5000);
            });            
            open_menu_p = logged_in_p.then(function(data){
                td_utils.reset_menu_count();
                return td_utils.open_menu();                
            });
            logged_out_p = open_menu_p.then(function(data){                
                element(by.id('logout_link')).click();
                return browser.wait(EC.presenceOf($('.icon-label')), 5000);
            });
            logged_out_p.then(function(data){
                expect(element(by.className('icon-label')).isDisplayed()).toEqual(true);
                expect(element(by.id('error_present')).isPresent()).toBe(false);                            
                isUserLoggedIn(false, {username:'test_admin'}).then(function(data){
                    td_utils.checkForError(false,done);                    
                });            
            });            
        });
    }); 
});    

