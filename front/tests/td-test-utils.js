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

var open_menu_ex = function(){
    element.all(by.id('ion-navicon-id')).then(function(data){
        data[0].isDisplayed().then(function(local_data){
            if(local_data==true){
                data[0].click();
            }
            
        });
        data[1].isDisplayed().then(function(local_data_2){
            if(local_data_2==true){
                data[1].click();
            }
        });
    });
    browser.sleep(1000);
};


exports.open_menu = open_menu;
exports.open_menu_ex = open_menu_ex;

var reset_menu_count = function(){
    menu_count = 0;
}

exports.reset_menu_count=reset_menu_count;

var login_through_webpage = function(username,password){
    var EC = protractor.ExpectedConditions;
    browser.wait(open_menu_ex());
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

var login_through_webpage_ex = function(username,password){
    var EC = protractor.ExpectedConditions;
    open_menu_ex();
    browser.wait(EC.presenceOf($('#login_link')), 5000);
    element(by.id('login_link')).click();
    element(by.model('user.username')).sendKeys(username);
    element(by.model('user.password')).sendKeys(password);
    element(by.id('LoginButton')).click();
};

exports.login_through_webpage_ex = login_through_webpage_ex;


var beforeTdTest = function(login,username,password){
    //FIXME : need to handle type_of_db_init MUCH better
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
        uri: "http://"+instance_ip+":8000/meta_admin/test_db"+type_of_db_init,
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

var beforeTdTestEx = function(login,username,password,type_of_db_init){
    var EC = protractor.ExpectedConditions;
    if(username==undefined){
        username='test_admin';
        password='test_admin';
    }
    if (browser.params.test_instance_ip == undefined){        
        throw Error('params.test_instance_ip not defined');
    }
    var instance_ip = browser.params.test_instance_ip;         
    this.get_promise = browser.manage().deleteAllCookies();
    if(type_of_db_init == undefined){
        type_of_db_init = "";
    }
    options = {
        uri: "http://"+instance_ip+":8000/meta_admin/test_db"+type_of_db_init,
        method: 'POST',
        json: true // Automatically parses the JSON string in the response
    };
    var wipe_db_p = rp(options);
    browser.wait(wipe_db_p,10000);
    browser.manage().deleteAllCookies();
    browser.get('http://'+instance_ip+':8100/#/test/app');

    if(login==undefined){        
        return;
    }
    login_through_webpage_ex('test_admin','test_admin');
    browser.wait(EC.presenceOf($('#HomeButton')), 5000);
    element(by.id('HomeButton')).click();
    browser.sleep(1000);
};

exports.beforeTdTestEx = beforeTdTestEx;


var checkForError = function(expectError){
    var EC = protractor.ExpectedConditions;
    browser.wait(EC.presenceOf($('#error_present')), 5000).then(function(data){        
        if(expectError == false){
            console.log("was NOT expecting error -- but did find one ");
            expect(false).toBe(true);            
        }             
    },function(err){        
        if(expectError == true){
            console.log("no error found - but WAS expecting error");
            expect(false).toBe(true);                        
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
                el = element(by.id("add_user_add_button"));
                var tag = browser.executeScript("arguments[0].scrollIntoView(true)", el);
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

var add_new_user_ex = function(new_user_name,go_home){
    var EC = protractor.ExpectedConditions;
    element(by.id('home_manage_user_button')).click();        
    //browser.wait(EC.presenceOf($('#manage_users_add_user_button'),5000));
    element(by.id('manage_users_add_user_button')).click();
    //browser.wait(EC.presenceOf($('#add_user_user_info_title')), 5000);
    element(by.model('user_info.username')).sendKeys(new_user_name);
    element(by.model('user_info.password')).sendKeys(new_user_name);
    element(by.id('add_user_role_admin_checkbox')).click().then(function(data){
        el = element(by.id("add_user_add_button"));
        browser.executeScript("arguments[0].scrollIntoView(true)", el);
        element(by.id('add_user_add_button')).click();
    });
    browser.wait(EC.presenceOf($('#AddAnotherUser')), 5000);
    if(go_home == true){
        element(by.id('AddAnotherUser')).click();                
    }
};
    
exports.add_new_user_ex = add_new_user_ex;

var add_new_tournament = function(new_tournament_name,single_division,check_for_error,use_stripe){        
    var EC = protractor.ExpectedConditions;
    var button_to_wait_for = undefined;
    if(single_division){
        button_to_wait_for = "AddAnotherTournament";
    } else {
        button_to_wait_for = "AddDivisionsToTournament";
    }
    open_menu_ex();    
    element(by.id('menu_tournament_link')).click();
    element(by.id('manage_tournaments_add_tournament_button')).click();    
    element(by.model('tournament.tournament_name')).sendKeys(new_tournament_name);        
    if(single_division == false){
        element(by.id('add_tournament_single_division_checkbox')).click();
    } else {
        element(by.model('tournament.finals_num_qualifiers')).sendKeys("24");        
        if(use_stripe == true){
            element(by.model('tournament.stripe_sku')).sendKeys("12345abcd");
        } else {
            element(by.model('tournament.use_stripe')).click();
            element(by.model('tournament.local_price')).sendKeys("5");            
        }        
    }
    el = element(by.id("add_tournament_add_button"));
    browser.executeScript("arguments[0].scrollIntoView(true)", el);
    element(by.id('add_tournament_add_button')).click();
    if(check_for_error == true){
        checkForError(false);
    }    
    element(by.id(button_to_wait_for)).click();        
    browser.wait(EC.presenceOf($('#tournament_edit_tournament_'+new_tournament_name+'_link')), 5000);        
};

exports.add_new_tournament = add_new_tournament;

var add_new_player = function(new_player_first_name,new_player_last_name,submit_player){
    element(by.id('home_manage_players_button')).click();        
    element(by.id('manage_players_add_player_button')).click();
    expect(element(by.id('add_player_add_button')).isEnabled()).toBe(false);
    element(by.model('player_info.first_name')).sendKeys(new_player_first_name);
    expect(element(by.id('add_player_add_button')).isEnabled()).toBe(false);
    element(by.model('player_info.last_name')).sendKeys(new_player_last_name);
    expect(element(by.id('add_player_add_button')).isEnabled()).toBe(false);
    element(by.id('add_player_get_ifpa_ranking')).click();
    element(by.buttonText('Cancel')).click();
    expect(element(by.id('add_player_add_button')).isEnabled()).toBe(false);
    element(by.id('add_player_linked_division_B')).click();
    expect(element(by.id('add_player_add_button')).isEnabled()).toBe(true);
    if(submit_player == true){
        element(by.id('add_player_add_button')).click();
    }
}

exports.add_new_player = add_new_player;
