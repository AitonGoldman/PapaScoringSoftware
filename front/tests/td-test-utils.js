var rp = require('request-promise');
var menu_count = 0;

var open_menu = function(){
     if(menu_count == 0){
        menu_count = 1;
    } else {
        menu_count = 0;
    }    
    ion_navicon_promise = element.all(by.className('ion-navicon'));    
    menu_click_promise = ion_navicon_promise.then(function(super_local_data){                        
        super_local_data[menu_count].click();        
    });    
    return browser.sleep(1000);
};

exports.open_menu = open_menu;

var reset_menu_count = function(){
    menu_count = 0;
}

exports.reset_menu_count=reset_menu_count;

var login_through_webpage = function(username,password){
    var EC = protractor.ExpectedConditions;
    browser.wait(open_menu());
        //FIXME : need to change login_link to more descriptive name
    //login_link_present_promise = element(by.id('login_link')).isDisplayed();
    login_link_present_promise = browser.wait(EC.presenceOf($('#login_link')), 5000);
    login_link_click_promise = login_link_present_promise.then(function(data){        
        element.all(by.id('login_link')).then(function(login_link_data){            
            element(by.id('login_link')).click();
        });
        
    });
    return login_link_click_promise.then(function(data){
        element(by.model('user.username')).sendKeys(username);
        element(by.model('user.password')).sendKeys(password);
        element.all(by.id('LoginButton')).then(function(local_data){
            local_data[0].click();
        });
    });
};

exports.login_through_webpage = login_through_webpage;

var beforeTdTest = function(login,username,password){
    
    reset_menu_count();
    if(username==undefined){
        username='test_admin';
        password='test_admin';
    }
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
    
    var wipe_db_p = rp(options);
    
    var del_cookies_p = wipe_db_p.then(function(data){
        
        return browser.manage().deleteAllCookies();            
    });
    
    var get_page_p = del_cookies_p.then(function(data){
        
        browser.get('http://'+instance_ip+':8100/#/test/app');
        return browser.sleep(3000);
    });

    if(login==undefined){
        
        return get_page_p;
    }
    
    logged_in_p = get_page_p.then(function(data){
        return login_through_webpage('test_admin','test_admin');
    });
    logged_in_screen_p = logged_in_p.then(function(data){
        var EC = protractor.ExpectedConditions;
        // Waits for the element with id 'abc' to be present on the dom.
        return browser.wait(EC.presenceOf($('#HomeButton')), 5000);
    });
    return logged_in_screen_p.then(function(data){
        $('#HomeButton').click();
        return browser.sleep(1000);            
    });        
}

exports.beforeTdTest = beforeTdTest;

var checkForError = function(expectError, done){
    var EC = protractor.ExpectedConditions;
    if(done==undefined){
        done=function(){};
    }
    browser.wait(EC.stalenessOf($('#error_present')), 5000).then(function(data){
        if(expectError == false){
            done();
        } else {
            console.log("WAS expecting error -- "+err);
            expect(false).toBe(true);
            done();
        }                    
    },function(err){
        if(expectError == true){
            done();
        } else {
            console.log("was NOT expecting error -- "+err);
            expect(false).toBe(true);
            done();
        }                    
    });

}

exports.checkForError = checkForError;

var add_new_user = function(new_user_name){        
        $('#home_manage_user_button').click();
        var EC = protractor.ExpectedConditions;
            // Waits for the element with id 'abc' to be present on the dom.
            manage_users_p =  browser.wait(EC.presenceOf($('#manage_users_add_user_button')), 5000);
            manage_users_p.then(function(data){
                $('#manage_users_add_user_button').click();
            });
            manage_users_p =  browser.wait(EC.presenceOf($('#add_user_user_info_title')), 5000);
            manage_users_p.then(function(data){
                element(by.model('user_info.username')).sendKeys(new_user_name);
                element(by.model('user_info.password')).sendKeys(new_user_name);
                element(by.id('add_user_role_admin_checkbox')).click();
                element.all(by.id('add_user_add_button')).then(function(data){
                    data[0].click();
                });
                return browser.wait(EC.presenceOf($('#AddAnotherUser')), 5000);    
            });
            
            return manage_users_p.then(function(data){
                $('#AddAnotherUser').click();
                return browser.wait(EC.presenceOf($('#user_edit_user_'+new_user_name+'_link')), 5000);                    
            });
    };

exports.add_new_user = add_new_user;
