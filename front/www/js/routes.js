angular.module('pss').config(['$stateProvider', '$urlRouterProvider',function($stateProvider,$urlRouterProvider) {
    $urlRouterProvider.otherwise('/app/event_select');
    $stateProvider.state('app', {
        cache:false,
        abstract: true,
        url: '/app',        
        views: {
            'topView@': {
                templateUrl: 'templates/app/app_content.html',//check
                controller: 'app_controller'
            }
        },data: {            
            header_links: []
        }                    
    }).state('app.event_select',{
        cache:false,        
        url:'/event_select',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/app/event_select/event_select_content.html',
                controller: 'app.event_select_controller'
            },
            'pssAdminHeader@':{                
                 templateUrl: 'templates/app/event_select/event_select_header.html'// check                
             },
            'pssAdminFooter@app':{
                templateUrl: 'templates/app/event_select/event_select_footer.html'// check                
            }            
        },data: {
            title: "Select Events",
            back_title: "Switch Event"
        }
    }).state('app.pss_admin', {
        cache:false,
        url: '/pss_admin',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/app/pss_admin/pss_admin_content.html',
                controller: 'app.pss_admin_controller'
            },
            'pssAdminHeader@':{
                templateUrl: 'templates/app/pss_admin/pss_admin_header.html'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/pss_admin_footer.html'
            }
        },data: {
            title: "Home",
            back_title: "Home",            
            quick_links_url: 'templates/pss_admin_quick_links.html'
        }
    }).state('app.pss_admin.login', {
        cache:false,
        url: '/pss_admin_login',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/app/pss_admin/login/pss_admin_login.html',
                controller: 'app.pss_admin.login_controller'
                
            },
            'post_success@app.pss_admin.login':{
                templateUrl: 'templates/generic_post_success.html'// check                
            }
            
        },data: {
            title: "Login"            
        }
    }).state('app.pss_admin.create_event', {
        cache:false,
        url: '/create_event',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/app/pss_admin/create_event/create_event_content.html',
                controller: 'app.pss_admin.create_event_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/pss_admin_footer.html'// check
            },
            'post_success@app.pss_admin.create_event':{
                templateUrl: 'templates/generic_post_success.html'// check                
            }            
        },data: {
            title: "Create Event"            
        }
    }).state('app.pss_admin.edit_event_basic', {
        cache:false,
        url: '/edit_event_basic/:id',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/app/pss_admin/edit_event_basic/edit_event_basic_content.html',
                controller: 'app.shared.edit_event_tournament_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/pss_admin_footer.html'// check
            },
            'post_success@app.pss_admin.edit_event_basic':{
                templateUrl: 'templates/generic_post_success.html'// check
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
                templateUrl: 'templates/app/pss_admin/edit_event_advanced/edit_event_advanced_content.html',
                controller: 'app.shared.edit_event_tournament_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/pss_admin_footer.html'// check
            },
            'post_success@app.pss_admin.edit_event_advanced':{
                templateUrl: 'templates/generic_post_success.html'// check                
            }            
        },data: {
            title: "Edit Event",
            edit_route: "put_edit_event",
            get_route: "get_event"      
        },params: {
            item: {value:{}}
        }
    }).state('app.pss_admin.quick_create_tournament', {
        cache:false,
        url: '/quick_create_tournament/:event_id',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/app/event/manage_tournaments/create_tournament/create_tournament_content.html',
                controller: 'app.event.manage_tournaments.create_tournament_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html' // check
            },
            'post_success@app.pss_admin.quick_create_tournament':{
                templateUrl: 'templates/generic_post_success.html'
            },
            'post_success_buttons@app.pss_admin.quick_create_tournament':{
                templateUrl: 'templates/quick_create_event_tournament_post_success_buttons.html'                
            }
        },data: {
            title: "Create Tournament",
            quick_links_url: 'templates/pss_admin_quick_links.html'            
        }
    }).state('app.pss_admin.quick_add_tournament_machine', {
        cache:false,
        url: '/quick_add_tournament_machine/:tournament_id/:event_id',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/app/event/manage_tournament_machines/add_tournament_machine/add_tournament_machine_content.html',
                controller: 'app.event.manage_tournament_machines.add_tournament_machine_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html' // check
            },
            'post_success@app.pss_admin.quick_add_tournament_machine':{
                templateUrl: 'templates/generic_post_success.html'                
            },
            'post_success_buttons@app.pss_admin.quick_add_tournament_machine':{
                templateUrl: 'templates/quick_add_tournament_machine_post_success_buttons.html'                
            }            
        },data: {
            title: "Add Machine",
            back_title: "Add Machine",
            quick_links_url: 'templates/event_quick_links.html'
        }
    }).state('app.event', {
        cache:false,
        url: '/event/:event_name',
        views: {
            'pssAdminHeader@':{
                templateUrl: 'templates/app/event/event_header.html'// check
            },
            'pssAdminContent@app':{
                templateUrl: 'templates/app/event/event_content.html',
                controller: 'app.event_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'// check
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
                templateUrl: 'templates/app/event/login/event_login.html',
                controller: 'app.pss_admin.login_controller'
                
            },
            'post_success@app.event.login':{
                templateUrl: 'templates/generic_post_success.html'// check                
            }
            
        },data: {
            title: "Login"
        }
    }).state('app.pss_admin.quick_create_scorekeepers_existing', {
        cache:false,
        url: '/quick_create_scorekeepers_existing/:event_id/:event_role_name',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/app/shared/quick_create_scorekeeper_existing.html',
                controller: 'app.shared.quick_create_user'
                
            },
            'post_success@app.pss_admin.quick_create_scorekeepers_existing':{
                templateUrl: 'templates/generic_post_success.html'// check                
            }
            
        },data: {
            title: "QuickAdd Scorekeepers"
        }
    }).state('app.pss_admin.quick_create_scorekeepers_new', {
        cache:false,
        url: '/quick_create_scorekeepers_new/:event_id/:event_role_name',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/app/shared/quick_create_scorekeeper_new.html',
                controller: 'app.shared.quick_create_user'
                
            },
            'post_success@app.pss_admin.quick_create_scorekeepers_new':{
                templateUrl: 'templates/generic_post_success.html'// check                
            }
            
        },data: {
            title: "QuickAdd Scorekeepers"
        }
    }).state('app.event.manage_tournaments', {
        cache:false,
        url: '/manage_tournaments',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/app/event/manage_tournaments/manage_tournaments_content.html',
                controller: 'app.event.manage_tournaments_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'// check
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
            'pssAdminContent@app':{
                templateUrl: 'templates/app/event/manage_tournaments/create_tournament/create_tournament_content.html',
                controller: 'app.event.manage_tournaments.create_tournament_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'// check
            },
            'post_success@app.event.manage_tournaments.create_tournament':{
                templateUrl: 'templates/generic_post_success.html'// check                
            },
            'post_success_buttons@app.event.manage_tournaments.create_tournament':{
                templateUrl: 'templates/create_tournament_post_success_buttons.html'                
            }
        },data: {
            title: "Create Tournament",
            quick_links_url: 'templates/event_quick_links.html'            
        }
    }).state('app.event.manage_tournaments.edit_tournament_basic', {
        cache:false,
        url: '/edit_tournament_basic/:id',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/app/event/manage_tournaments/edit_tournament_basic/edit_tournament_basic_content.html',
                controller: 'app.shared.edit_event_tournament_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'// check
            },
            'post_success@app.event.manage_tournaments.edit_tournament_basic':{
                templateUrl: 'templates/generic_post_success.html'// check
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
                templateUrl: 'templates/app/event/manage_tournaments/edit_tournament_advanced/edit_tournament_advanced_content.html',
                controller: 'app.shared.edit_event_tournament_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'
            },
            'post_success@app.event.manage_tournaments.edit_tournament_advanced':{
                templateUrl: 'templates/generic_post_success.html'
            }            
        },data: {
            title: "Edit Tournament",
            edit_route: "put_edit_tournament",
            get_route: "get_tournament"      
        },params: {
            item: {value:{}}
        }
    }).state('app.event.manage_meta_tournaments', {
        cache:false,
        url: '/manage_meta_tournaments',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/app/event/manage_meta_tournaments/manage_meta_tournaments_content.html',
                controller: 'app.event.manage_tournaments_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'
            }            
        },data: {
            title: "Manage MetaTournaments",
            back_title: "Manage MetaTournaments",
            quick_links_url: 'templates/event_quick_links.html'
        }
    }).state('app.event.manage_meta_tournaments.create_meta_tournament', {
        cache:false,
        url: '/create_meta_tournament',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/app/event/manage_meta_tournaments/create_meta_tournament/create_meta_tournament_content.html',
                controller: 'app.event.manage_tournaments.create_meta_tournament_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'// check
            },
            'post_success@app.event.manage_meta_tournaments.create_meta_tournament':{
                templateUrl: 'templates/generic_post_success.html'// check
            }            
        },data: {
            title: "Create Meta Tournament"
        }
    }).state('app.event.select_players_to_add_to_event', {
        cache:false,
        url: '/select_players_to_add_to_event',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/app/event/select_players_to_add_to_event/select_players_to_add_to_event.html',
                controller: 'app.event.select_players_to_add_to_event_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'// check
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
            'pssAdminContent@app':{
                templateUrl: 'templates/app/event/select_players_to_add_to_event/add_player_to_event/add_players_to_event_content.html',
                controller: 'app.event.select_players_to_add_to_event.add_players_to_event_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'// check
            },
            'post_success@app.event.select_players_to_add_to_event.add_player_to_event':{
                templateUrl: 'templates/generic_post_success.html'// check                
            }            
        },data: {
            title: "Register Players",
            quick_links_url: 'templates/event_quick_links.html'
        }
    }).state('app.event.select_players_to_add_to_event.add_existing_player_to_event', {
        cache:false,
        url: '/add_existing_players_to_event/:player_id',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/app/event/select_players_to_add_to_event/add_player_to_event/add_players_to_event_content.html',
                controller: 'app.event.select_players_to_add_to_event.add_players_to_event_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'// check
            },
            'post_success@app.event.select_players_to_add_to_event.add_existing_player_to_event':{
                templateUrl: 'templates/generic_post_success.html'// check
                //controller: 'pss_admin_controller'
            }            
        },data: {
            title: "Register Players",
            quick_links_url: 'templates/event_quick_links.html'
        }
    }).state('app.event.manage_tournaments.edit_meta_tournament_advanced', {
        cache:false,
        url: '/edit_meta_tournament_advanced/:id',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/app/event/manage_tournaments/edit_meta_tournament_advanced/edit_meta_tournament_advanced_content.html',
                controller: 'app.shared.edit_event_tournament_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'// check
            },
            'post_success@app.event.manage_tournaments.edit_meta_tournament_advanced':{
                templateUrl: 'templates/generic_post_success.html'// check
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
                templateUrl: 'templates/app/event/manage_tournaments/edit_meta_tournament_basic/edit_meta_tournament_basic_content.html',
                controller: 'app.shared.edit_event_tournament_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'// check
            },
            'post_success@app.event.manage_tournaments.edit_meta_tournament_basic':{
                templateUrl: 'templates/generic_post_success.html'// check
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
                templateUrl: 'templates/app/event/manage_tournament_machines/add_tournament_machine/add_tournament_machine_content.html',
                controller: 'app.event.manage_tournament_machines.add_tournament_machine_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html' // check
            },
            'post_success@app.event.manage_tournaments.add_tournament_machine':{
                templateUrl: 'templates/generic_post_success.html'// check
            },
            'post_success_buttons@app.event.manage_tournaments.add_tournament_machine':{
                templateUrl: 'templates/add_tournament_machine_post_success_buttons.html'                
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
                templateUrl: 'templates/app/event/manage_tournament_machines/manage_tournament_machines_content.html',
                controller: 'app.event.manage_tournament_machines_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html' //check
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
                templateUrl: 'templates/app/event/manage_tournament_machines/add_tournament_machine/add_tournament_machine_content.html',
                controller: 'app.event.manage_tournament_machines.add_tournament_machine_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'
            },
            'post_success@app.event.manage_tournament_machines.add_tournament_machine':{
                templateUrl: 'templates/generic_post_success.html'// check
            },
            'post_success_buttons@app.event.manage_tournament_machines.add_tournament_machine':{
                templateUrl: 'templates/add_tournament_machine_post_success_buttons.html'                
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
                templateUrl: 'templates/app/event/token_purchase/token_purchase_content.html',
                controller: 'app.event.token_purchase_controller'
                
            },
            'post_success@app.event.token_purchase':{
                templateUrl: 'templates/generic_post_success.html'// check                
            }
            
        },data: {
            title: "Token Purchase"
        },params: {
            player: {value:{}}
        }
    }).state('app.register_new_pss_user', {
        cache:false,
        url: '/register_new_pss_user',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/app/register_new_pss_user/register_new_pss_user_content.html',
                controller: 'app.register_new_pss_user_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'// check
            }            
        },data: {
            title: "Register new user"
        }
    }).state('app.register_new_pss_user_confirm', {
        cache:false,
        url: '/register_new_pss_user_confirm',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/app/register_new_pss_user_confirm/register_new_pss_user_confirm_content.html',
                controller: 'app.register_new_pss_user_confirm_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html'// check
            },
            'post_success@app.register_new_pss_user_confirm':{
                templateUrl: 'templates/generic_post_success.html'// check
                //controller: 'pss_admin_controller'
            }            
        },data: {
            title: "New User Activated!"
        }
    }).state('app.event.player_info', {
        cache:false,
        url: '/player_info',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/app/event/player_info/player_info_content.html',
                controller: 'app.event.player_info_controller'                
            }
            
        },data: {
            title: "Player Info"
        }
    }).state('app.event.quick_create_tournament', {
        cache:false,
        url: '/quick_create_tournament',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/app/event/manage_tournaments/create_tournament/create_tournament_content.html',
                controller: 'app.event.manage_tournaments.create_tournament_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html' // check
            },
            'post_success@app.event.quick_create_tournament':{
                templateUrl: 'templates/generic_post_success.html'
            },
            'post_success_buttons@app.event.quick_create_tournament':{
                templateUrl: 'templates/quick_create_tournament_post_success_buttons.html'                
            }
        },data: {
            title: "Create Tournament",
            quick_links_url: 'templates/event_quick_links.html'            
        }
    }).state('app.event.quick_add_tournament_machine', {
        cache:false,
        url: '/quick_add_tournament_machine/:tournament_id',
        views: {
            'pssAdminContent@app':{
                templateUrl: 'templates/app/event/manage_tournament_machines/add_tournament_machine/add_tournament_machine_content.html',
                controller: 'app.event.manage_tournament_machines.add_tournament_machine_controller'
            },
            'pssAdminFooter@app':{
                templateUrl: 'templates/event_footer.html' // check
            },
            'post_success@app.event.quick_add_tournament_machine':{
                templateUrl: 'templates/generic_post_success.html'                
            },
            'post_success_buttons@app.event.quick_add_tournament_machine':{
                templateUrl: 'templates/quick_add_tournament_machine_post_success_buttons.html'                
            }            
        },data: {
            title: "Add Machine",
            back_title: "Add Machine",
            quick_links_url: 'templates/event_quick_links.html'
        }
    })

    ;}]);
