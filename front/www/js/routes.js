angular.module('pss').config(['$stateProvider', '$urlRouterProvider',function($stateProvider,$urlRouterProvider) {
    $urlRouterProvider.otherwise('/event_select');
    $stateProvider.state('event_select',{
        url:'/event_select',
        views:{
            'topView@' : {                
                templateUrl:'templates/event_select.html',
                controller: 'event_select_controller'            
            }
        }
    }).state('app', {
        cache:false,
        abstract: true,
        url: '/app',        
        views: {
            'topView@': {
                templateUrl: 'templates/pss_admin_2.html',
                controller: 'pss_admin_controller'
            }
        }}).state('app.pss_admin', {
        cache:false,
        url: '/pss_admin',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/pss_admin_front.html',
                controller: 'pss_admin_controller'
            },
            'pssAdminHeader@':{
                templateUrl: 'templates/pss_admin_header.html'//,
                //controller: 'pss_admin_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/pss_admin_footer.html'//,
                //controller: 'pss_admin_controller'
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
                controller: 'pss_admin_controller'
                
            },
            'pssAdminHeader@':{
                templateUrl: 'templates/pss_admin_header_2.html'//,
                //controller: 'pss_admin_controller'
            }            
        },data: {
            title: "Enter Login Info"
        }
    })

    ;}]);
