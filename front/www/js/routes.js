angular.module('pss').config(['$stateProvider', '$urlRouterProvider',function($stateProvider,$urlRouterProvider) {
    $urlRouterProvider.otherwise('/app/event_select');
    $stateProvider.state('app.event_select',{
        url:'/event_select',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/event_select_content.html',
                controller: 'app.event_select_controller'
            },
            'pssAdminHeader@':{
                templateUrl: 'templates/event_select_header.html'//,                
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_select_footer.html'//,
                
            }            
        },data: {
            title: "Select Events"
        }
    }).state('app', {
        cache:false,
        abstract: true,
        url: '/app',        
        views: {
            'topView@': {
                templateUrl: 'templates/pss_admin_2.html',
                controller: 'app_controller'
            }
        }
    }).state('app.pss_admin', {
        cache:false,
        url: '/pss_admin',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/pss_admin_content.html',
                controller: 'app.pss_admin_controller'
            },
            'pssAdminHeader@':{
                templateUrl: 'templates/pss_admin_header.html'//,
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
            'pssAdminHeader@':{
                templateUrl: 'templates/pss_admin_header.html'//,
                //controller: 'pss_admin_controller'
            }            
        },data: {
            title: "Enter Login Info"
        }
    })

    ;}]);
