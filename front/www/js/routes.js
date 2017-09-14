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
            },
            'list@app.pss_admin':{
                templateUrl: 'templates/generic_list.html'//,
            }
        },data: {
            title: "Manage Events",
            quick_links_url: 'templates/pss_admin_quick_links.html'
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
                controller: 'app.pss_admin.edit_event_controller'
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
            title: "Edit Event"
        },params: {
            event: {value:{}},
            descriptions: {value:{}}
        }
    }).state('app.pss_admin.edit_event_basic', {
        cache:false,
        url: '/edit_event_basic/:event_id',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/edit_event_basic_content.html',
                controller: 'app.pss_admin.edit_event_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/pss_admin_footer.html'//,
            },
            'post_success@app.pss_admin.edit_event_basic':{
                templateUrl: 'templates/generic_post_success.html'//,
                //controller: 'pss_admin_controller'
            },
            'post_success_buttons@app.pss_admin.edit_event_basic':{
                templateUrl: 'templates/event_create_post_success_buttons.html'//,
                //controller: 'pss_admin_controller'
            }            
        },data: {
            title: "Edit Event"
        },params: {
            event: {value:{}}
        }
    }).state('app.pss_admin.edit_event_advanced', {
        cache:false,
        url: '/edit_event_advanced/:event_id',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/edit_event_advanced_content.html',
                controller: 'app.pss_admin.edit_event_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/pss_admin_footer.html'//,
            },
            'post_success@app.pss_admin.edit_event_advanced':{
                templateUrl: 'templates/generic_post_success.html'//,
                //controller: 'pss_admin_controller'
            },
            'post_success_buttons@app.pss_admin.edit_event_advanced':{
                templateUrl: 'templates/event_create_post_success_buttons.html'//,
                //controller: 'pss_admin_controller'
            }            
        },data: {
            title: "Edit Event"
        },params: {
            event: {value:{}}
        }
    }).state('app.event', {
        cache:false,
        url: '/event/:event_name',
        views: {
            // 'topView@': {
            //     templateUrl: 'templates/pss_admin_2.html',
            //     controller: 'app_controller'
            // },            
            'pssAdminHeader@':{
                templateUrl: 'templates/generic_event_header.html'//,
            },
            'pssAdminContent@app':{
                templateUrl: 'templates/event_content.html',
                controller: 'app.event_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'//,
            }
        },data: {
            title: "Event Front Page",
            quick_links_url: 'templates/event_quick_links.html'
        }
    }).state('app.event.login', {
        cache:false,
        url: '/event_login',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/event_login.html',
                controller: 'app.pss_admin.login_controller'
                
            },
            'post_success@app.event.login':{
                templateUrl: 'templates/generic_post_success.html'//,
                //controller: 'pss_admin_controller'
            },
            'post_success_buttons@app.event.login':{
                templateUrl: 'templates/event_login_post_success_buttons.html'//,
                //controller: 'pss_admin_controller'
            }
            
        },data: {
            title: "Login"
        }
    }).state('app.event.manage_tournaments', {
        cache:false,
        url: '/manage_tournaments',
        views: {
            // 'topView@': {
            //     templateUrl: 'templates/pss_admin_2.html',
            //     controller: 'app_controller'
            // },            
            'pssAdminContent@app':{
                templateUrl: 'templates/manage_tournaments_content.html',
                controller: 'app.event.manage_tournaments_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'//,
            },
            'list@app.pss_admin':{
                templateUrl: 'templates/generic_list.html'//,
            }
        },data: {
            title: "Manage Tournaments",
            quick_links_url: 'templates/event_quick_links.html'
        }
    }).state('app.event.manage_tournaments.create_tournament', {
        cache:false,
        url: '/create_tournament',
        views: {
            // 'topView@': {
            //     templateUrl: 'templates/pss_admin_2.html',
            //     controller: 'app_controller'
            // },            
            'pssAdminContent@app':{
                templateUrl: 'templates/create_tournament_content.html',
                controller: 'app.event.manage_tournaments.create_tournament_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'//,
            },
            'post_success@app.event.manage_tournaments.create_tournament':{
                templateUrl: 'templates/generic_post_success.html'//,
                //controller: 'pss_admin_controller'
            },
            'post_success_buttons@app.event.manage_tournaments.create_tournament':{
                templateUrl: 'templates/tournament_create_post_success_buttons.html'//,
                //controller: 'pss_admin_controller'
            }
        },data: {
            title: "Manage Tournaments",
            quick_links_url: 'templates/event_quick_links.html'
        }
    })

    ;}]);
