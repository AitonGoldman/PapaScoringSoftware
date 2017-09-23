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
            title: "Select Events",
            back_title: "Switch Event"
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
            back_title: "Events",            
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
        url: '/edit_event_wizard/:id/:wizard_step',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/edit_event_wizard_content.html',
                controller: 'app.shared.edit_event_tournament_controller'
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
            title: "Edit Event",
            edit_route: "put_edit_event",
            get_route: "get_event"            
        },params: {
            item: {value:{}},
            descriptions: {value:{}}            
        }
    }).state('app.pss_admin.edit_event_basic', {
        cache:false,
        url: '/edit_event_basic/:id',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/edit_event_basic_content.html',
                controller: 'app.shared.edit_event_tournament_controller'
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
            title: "Edit Event",
            edit_route: "put_edit_event",
            get_route: "get_event"      
        },params: {
            item: {value:{}}
        }
    }).state('app.pss_admin.edit_event_advanced', {
        cache:false,
        url: '/edit_event_advanced/:id',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/edit_event_advanced_content.html',
                controller: 'app.shared.edit_event_tournament_controller'
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
            title: "Edit Event",
            edit_route: "put_edit_event",
            get_route: "get_event"      
        },params: {
            item: {value:{}}
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
            title: "Front Page",
            back_title: "Home",
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
            },
            'list@app.event.manage_tournaments':{
                templateUrl: 'templates/generic_list.html'//,
            }            
        },data: {
            title: "Manage Tournaments",
            back_title: "Manage Tournaments",
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
            title: "Create Tournament",
            quick_links_url: 'templates/event_quick_links.html'            
        }
    }).state('app.event.manage_tournaments.edit_tournament_wizard', {
        cache:false,
        url: '/edit_tournament_wizard/:id/:wizard_step',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/edit_tournament_wizard_content.html',
                controller: 'app.shared.edit_event_tournament_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'//,
            },
            'post_success@app.event.manage_tournaments.edit_tournament_wizard':{
                templateUrl: 'templates/generic_post_success.html'//,
                //controller: 'pss_admin_controller'
            },
            'post_success_buttons@app.event.manage_tournaments.edit_tournament_wizard':{
                templateUrl: 'templates/tournament_create_post_success_buttons.html'//,
                //controller: 'pss_admin_controller'
            }            
        },data: {
            title: "Edit Tournament",
            edit_route: "put_edit_tournament",
            get_route:"get_tournament"
        },params: {
            item: {value:{}},
            descriptions: {value:{}}
        }
    }).state('app.event.manage_tournaments.edit_tournament_basic', {
        cache:false,
        url: '/edit_tournament_basic/:id',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/edit_tournament_basic_content.html',
                controller: 'app.shared.edit_event_tournament_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'//,
            },
            'post_success@app.event.manage_tournaments.edit_tournament_basic':{
                templateUrl: 'templates/generic_post_success.html'//,
                //controller: 'pss_admin_controller'
            },
            'post_success_buttons@app.event.manage_tournaments.edit_tournament_basic':{
                templateUrl: 'templates/tournament_create_post_success_buttons.html'//,
                //controller: 'pss_admin_controller'
            }            
        },data: {
            title: "Edit Tournament",
            edit_route: "put_edit_tournament",
            get_route: "get_tournament"      
        },params: {
            item: {value:{}}
        }
    }).state('app.event.manage_tournaments.edit_tournament_advanced', {
        cache:false,
        url: '/edit_tournament_advanced/:id',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/edit_tournament_advanced_content.html',
                controller: 'app.shared.edit_event_tournament_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'//,
            },
            'post_success@app.event.manage_tournaments.edit_tournament_advanced':{
                templateUrl: 'templates/generic_post_success.html'//,
                //controller: 'pss_admin_controller'
            },
            'post_success_buttons@app.event.manage_tournaments.edit_tournament_advanced':{
                templateUrl: 'templates/tournament_create_post_success_buttons.html'//,
                //controller: 'pss_admin_controller'
            }            
        },data: {
            title: "Edit Tournament",
            edit_route: "put_edit_tournament",
            get_route: "get_tournament"      
        },params: {
            item: {value:{}}
        }
    }).state('app.event.manage_tournaments.create_meta_tournament', {
        cache:false,
        url: '/create_meta_tournament',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/create_meta_tournament_content.html',
                controller: 'app.event.manage_tournaments.create_meta_tournament_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'//,
            },
            'post_success@app.event.manage_tournaments.create_meta_tournament':{
                templateUrl: 'templates/generic_post_success.html'//,
                //controller: 'pss_admin_controller'
            },
            'post_success_buttons@app.event.manage_tournaments.create_meta_tournament':{
                templateUrl: 'templates/tournament_create_post_success_buttons.html'//,
                //controller: 'pss_admin_controller'
            }            
        },data: {
            title: "Create Meta Tournament"
        }
    }).state('app.event.select_players_to_add_to_event', {
        cache:false,
        url: '/select_players_to_add_to_event',
        views: {
            // 'topView@': {
            //     templateUrl: 'templates/pss_admin_2.html',
            //     controller: 'app_controller'
            // },            
            'pssAdminContent@app':{
                templateUrl: 'templates/select_players_to_add_to_event.html',
                controller: 'app.event.select_players_to_add_to_event_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'//,
            },
            'list@app.event.select_players_to_add_to_event':{
                templateUrl: 'templates/generic_list.html'//,
            }            
        },data: {
            title: "Add Players To Event",
            back_title: "Select Players",
            quick_links_url: 'templates/event_quick_links.html'
        }
    }).state('app.event.select_players_to_add_to_event.add_player_to_event', {
        cache:false,
        url: '/add_players_to_event',
        views: {
            // 'topView@': {
            //     templateUrl: 'templates/pss_admin_2.html',
            //     controller: 'app_controller'
            // },            
            'pssAdminContent@app':{
                templateUrl: 'templates/add_players_to_event_content.html',
                controller: 'app.event.select_players_to_add_to_event.add_players_to_event_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'//,
            },
            'post_success@app.event.select_players_to_add_to_event.add_player_to_event':{
                templateUrl: 'templates/generic_post_success.html'//,
                //controller: 'pss_admin_controller'
            },
            'post_success_buttons@app.event.select_players_to_add_to_event.add_player_to_event':{
                templateUrl: 'templates/add_player_post_success_buttons.html'//,
                //controller: 'pss_admin_controller'
            }            
        },data: {
            title: "Add Players To Event",
            quick_links_url: 'templates/event_quick_links.html'
        }
    }).state('app.event.select_players_to_add_to_event.add_existing_player_to_event', {
        cache:false,
        url: '/add_existing_players_to_event/:player_id',
        views: {
            // 'topView@': {
            //     templateUrl: 'templates/pss_admin_2.html',
            //     controller: 'app_controller'
            // },            
            'pssAdminContent@app':{
                templateUrl: 'templates/add_players_to_event_content.html',
                controller: 'app.event.select_players_to_add_to_event.add_players_to_event_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'//,
            },
            'post_success@app.event.select_players_to_add_to_event.add_existing_player_to_event':{
                templateUrl: 'templates/generic_post_success.html'//,
                //controller: 'pss_admin_controller'
            },
            'post_success_buttons@app.event.select_players_to_add_to_event.add_existing_player_to_event':{
                templateUrl: 'templates/add_player_post_success_buttons.html'//,
                //controller: 'pss_admin_controller'
            }            
        },data: {
            title: "Add Players To Event",
            quick_links_url: 'templates/event_quick_links.html'
        }
    }).state('app.event.manage_tournaments.edit_meta_tournament_advanced', {
        cache:false,
        url: '/edit_meta_tournament_advanced/:id',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/edit_meta_tournament_advanced_content.html',
                controller: 'app.shared.edit_event_tournament_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'//,
            },
            'post_success@app.event.manage_tournaments.edit_meta_tournament_advanced':{
                templateUrl: 'templates/generic_post_success.html'//,
                //controller: 'pss_admin_controller'
            },
            'post_success_buttons@app.event.manage_tournaments.edit_meta_tournament_advanced':{
                templateUrl: 'templates/tournament_create_post_success_buttons.html'//,
                //controller: 'pss_admin_controller'
            }            
        },data: {
            title: "Edit Meta Tournament",
            edit_route: "put_edit_meta_tournament",
            get_route: "get_meta_tournament"      
        },params: {
            item: {value:{}}
        }
    }).state('app.event.manage_tournaments.edit_meta_tournament_basic', {
        cache:false,
        url: '/edit_meta_tournament_basic/:id',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/edit_meta_tournament_basic_content.html',
                controller: 'app.shared.edit_event_tournament_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'//,
            },
            'post_success@app.event.manage_tournaments.edit_meta_tournament_basic':{
                templateUrl: 'templates/generic_post_success.html'//,
                //controller: 'pss_admin_controller'
            },
            'post_success_buttons@app.event.manage_tournaments.edit_meta_tournament_basic':{
                templateUrl: 'templates/tournament_create_post_success_buttons.html'//,
                //controller: 'pss_admin_controller'
            }            
        },data: {
            title: "Edit Meta Tournament",
            edit_route: "put_edit_meta_tournament",
            get_route: "get_meta_tournament"      
        },params: {
            item: {value:{}}
        }
    }).state('app.event.manage_tournaments.add_tournament_machine', {
        cache:false,
        url: '/add_tournament_machine/:tournament_id',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/add_tournament_machine_content.html',
                controller: 'app.event.manage_tournament_machines.add_tournament_machine_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'
            },
            'post_success@app.event.manage_tournaments.add_tournament_machine':{
                templateUrl: 'templates/generic_post_success.html'//,
                //controller: 'pss_admin_controller'
            },
            'post_success_buttons@app.event.manage_tournaments.add_tournament_machine':{
                templateUrl: 'templates/manage_tournament_add_tournament_machine_post_success_buttons.html'//,
                //controller: 'pss_admin_controller'
            }            
        },data: {
            title: "Add Machine",
            back_title: "Add Machine",
            quick_links_url: 'templates/event_quick_links.html'
        }
    }).state('app.event.manage_tournament_machines', {
        cache:false,
        url: '/manage_tournament_machines',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/manage_tournament_machines_content.html',
                controller: 'app.event.manage_tournament_machines_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'
            }            
        },data: {
            title: "Manage Machines",
            back_title: "Manage Machines",
            quick_links_url: 'templates/event_quick_links.html'
        }
    }).state('app.event.manage_tournament_machines.add_tournament_machine', {
        cache:false,
        url: '/add_tournament_machine/:tournament_id',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/add_tournament_machine_content.html',
                controller: 'app.event.manage_tournament_machines.add_tournament_machine_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'
            },
            'post_success@app.event.manage_tournament_machines.add_tournament_machine':{
                templateUrl: 'templates/generic_post_success.html'//,
                //controller: 'pss_admin_controller'
            },
            'post_success_buttons@app.event.manage_tournament_machines.add_tournament_machine':{
                templateUrl: 'templates/tournament_machine_add_post_success_buttons.html'//,
                //controller: 'pss_admin_controller'
            }            
        },data: {
            title: "Add Machine",
            back_title: "Add Machine",
            quick_links_url: 'templates/event_quick_links.html'
        }
    }).state('app.event.token_purchase', {
        cache:false,
        url: '/token',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/token_purchase_content.html',
                controller: 'app.event.token_purchase_controller'
                
            },
            'post_success@app.event.token_purchase':{
                templateUrl: 'templates/generic_post_success.html'//,
                //controller: 'pss_admin_controller'
            },
            'post_success_buttons@app.event.token_purchase':{
                templateUrl: 'templates/token_purchase_post_success_buttons.html'//,
                //controller: 'pss_admin_controller'
            }
            
        },data: {
            title: "Token Purchase"
        }
    }).state('app.register_new_pss_user', {
        cache:false,
        url: '/register_new_pss_user',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/register_new_pss_user_content.html',
                controller: 'app.register_new_pss_user_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'//,
            },
            'post_success@app.register_new_pss_user':{
                templateUrl: 'templates/generic_post_success.html'//,
                //controller: 'pss_admin_controller'
            },
            'post_success_buttons@app.register_new_pss_user':{
                templateUrl: 'templates/tournament_create_post_success_buttons.html'//,
                //controller: 'pss_admin_controller'
            }            
        },data: {
            title: "Register new user"
        }
    }).state('app.register_new_pss_user_confirm', {
        cache:false,
        url: '/register_new_pss_user_confirm',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/register_new_pss_user_confirm_content.html',
                controller: 'app.register_new_pss_user_confirm_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'//,
            },
            'post_success@app.register_new_pss_user_confirm':{
                templateUrl: 'templates/generic_post_success.html'//,
                //controller: 'pss_admin_controller'
            },
            'post_success_buttons@app.register_new_pss_user_confirm':{
                templateUrl: 'templates/tournament_create_post_success_buttons.html'//,
                //controller: 'pss_admin_controller'
            }            
        },data: {
            title: "New User Activated!"
        }
    })

    ;}]);
