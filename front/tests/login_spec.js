var rp = require('request-promise');

describe('Auth', function() {
    var open_menu = function(){
        ion_navicon_promise = element.all(by.className('ion-navicon'));
        menu_click_promise = ion_navicon_promise.then(function(super_local_data){
            super_local_data[1].click();
        });
        return browser.sleep(3000);
    };
    
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
                        expect(expectation).toEqual(false);                                                                        
                    }                                                        
                })
                .catch(function (err) {
                    // test_done();
                    // API call failed...
                });       
        });        
    };
    
    var login_through_webpage = function(){
        browser.wait(open_menu());
        login_link_present_promise = element(by.id('login_link')).isDisplayed();
        login_link_click_promise = login_link_present_promise.then(function(data){
            element(by.id('login_link')).click();
        });
        return login_link_click_promise.then(function(data){
            element(by.model('user.username')).sendKeys('test_admin');
            element(by.model('user.password')).sendKeys('test_admin');
            element.all(by.linkText('Login')).then(function(data){
                 data[0].click();
            });
        });
    };
        
    beforeEach(function() {        
        if (browser.params.test_instance_ip == undefined){
            throw Error('params.test_instance_ip not defined');
        }
        var instance_ip = browser.params.test_instance_ip;         
        this.get_promise = browser.manage().deleteAllCookies();        
        options = {
            uri: "http://"+instance_ip+":8000/meta_admin/test_db",
            method: 'POST',
            json: true // Automatically parses the JSON string in the response
        };
        browser.wait(rp(options));
        browser.wait(this.get_promise);
        browser.get('http://'+instance_ip+':8100/#/test/app');
    });
    
    it('current user should be null when not logged in', function(done) {        
        this.get_promise.then(function(data){
            browser.wait(isUserLoggedIn(false));
            done();
        });        
    });    
    
    it('login link should be available when logged out', function(done) {        
        this.get_promise.then(function(data){
            expect(element(by.id('logout_link')).isPresent()).toBe(false);        
            expect(element(by.id('login_link')).isDisplayed()).toBe(true);
            done();
        });
    });
    
    it('should be able to login', function(done) {
        this.get_promise.then(function(data){
            login_through_webpage();
            var EC = protractor.ExpectedConditions;              
            browser.wait(EC.visibilityOf($('.icon-label')), 25000);
            expect(element(by.className('icon-label')).isDisplayed()).toEqual(true);
            expect(element(by.id('error_present')).isPresent()).toBe(false);                
            browser.wait(isUserLoggedIn(true, {username:'test_admin'}));
            done();
        });
    });
    
    it('should be able to logout', function(done) {        
        this.get_promise.then(function(data){
            login_through_webpage();
            var EC = protractor.ExpectedConditions;
            browser.wait(EC.presenceOf($('.icon-label')), 5000);
            expect(element(by.className('icon-label')).isDisplayed()).toEqual(true);
            browser.wait(open_menu());
            expect(element(by.id('logout_link')).isPresent()).toBe(true);     
            element(by.id('logout_link')).click();
            browser.wait(EC.presenceOf($('.icon-label')), 5000);
            expect(element(by.className('icon-label')).isDisplayed()).toEqual(true);
            expect(element(by.id('error_present')).isPresent()).toBe(false);                            
            browser.wait(isUserLoggedIn(false, {username:'test_admin'}));
            done();
        });
    }); 
});    

