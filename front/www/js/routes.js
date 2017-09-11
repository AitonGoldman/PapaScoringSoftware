angular.module('pss').config(['$stateProvider', '$urlRouterProvider',function($stateProvider,$urlRouterProvider) {
    $urlRouterProvider.otherwise('/app/event_select');
    $stateProvider.state('app', {
        cache:false,
        abstract: true,
        url: '/app',        
        views: {
            'topView@': {
                templateUrl: 'templates/pss_admin_2.html',
                controller: 'app_controller'
            },
            'pssAdminHeader@':{
                templateUrl: 'templates/generic_pss_admin_header.html'//,
            }
        },data: {            
            header_links: []
        }                    
    }).state('test', {
        cache:false,        
        url: '/test',        
        views: {
            'topView': {
                template: '<ion-view view-title="no joy"><ion-content><br><br><br><br><a ui-sref="test2">test 2</a></ion-content></ion-view>',
                controller: 'test_controller'
            }
         }      
    }).state('test2', {
        cache:false,        
        url: '/test/test2',        
        views: {
            'topView': {
                template: '<ion-view view-title="poop"><ion-content><br><br><br><br><a ui-sref="test">poop</a></ion-content></ion-view>',
                controller: 'test_controller'
            }
         }                                  
    }).state('app.event_select',{
        cache:false,        
        url:'/event_select',
        views: {
            // 'topView@': {
            //     templateUrl: 'templates/pss_admin_2.html',
            //     controller: 'app_controller'
            // },
            'pssAdminContent@app':{
                templateUrl: 'templates/event_select_content.html',
                controller: 'app.event_select_controller'
            },
            'pssAdminHeader@':{                
                 templateUrl: 'templates/generic_header.html'//,                
             },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_select_footer.html'//,                
            }            
        },data: {
            title: "Select Events"
        }
    }).state('app.pss_admin', {
        cache:false,
        url: '/pss_admin',
        views: {
            // 'topView@': {
            //     templateUrl: 'templates/pss_admin_2.html',
            //     controller: 'app_controller'
            // },            
            'pssAdminContent@app':{
                templateUrl: 'templates/pss_admin_content.html',
                controller: 'app.pss_admin_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/pss_admin_footer.html'//,
            }            
        },data: {
            title: "Manage Events"
        }
    }).state('app.pss_admin.login', {
        cache:false,
        url: '/pss_admin_login',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/pss_admin_login.html',
                controller: 'app.pss_admin.login_controller'
                
            },
            'post_success@app.pss_admin.login':{
                templateUrl: 'templates/generic_post_success.html'//,
                //controller: 'pss_admin_controller'
            },
            'post_success_buttons@app.pss_admin.login':{
                templateUrl: 'templates/pss_admin_login_post_success_buttons.html'//,
                //controller: 'pss_admin_controller'
            }
            
        },data: {
            title: "Login"
        }
    }).state('app.pss_admin.create_event', {
        cache:false,
        url: '/create_event',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/create_event_content.html',
                controller: 'app.pss_admin.create_event_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/pss_admin_footer.html'//,
            },
            'post_success@app.pss_admin.create_event':{
                templateUrl: 'templates/generic_post_success.html'//,
                //controller: 'pss_admin_controller'
            },
            'post_success_buttons@app.pss_admin.create_event':{
                templateUrl: 'templates/event_create_post_success_buttons.html'//,
                //controller: 'pss_admin_controller'
            }            
        },data: {
            title: "Create Event"            
        }
    }).state('app.pss_admin.edit_event_wizard', {
        cache:false,
        url: '/edit_event_wizard/:event_id/:wizard_step',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/edit_event_wizard_content.html',
                controller: 'app.pss_admin.edit_event_wizard_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/pss_admin_footer.html'//,
            },
            'post_success@app.pss_admin.edit_event_wizard':{
                templateUrl: 'templates/generic_post_success.html'//,
                //controller: 'pss_admin_controller'
            },
            'post_success_buttons@app.pss_admin.edit_event_wizard':{
                templateUrl: 'templates/event_create_post_success_buttons.html'//,
                //controller: 'pss_admin_controller'
            }            
        },data: {
            title: "Manage Events"
        },params: {
            event: {value:{}}
        }
    })

    ;}]);
