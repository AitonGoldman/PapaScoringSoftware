
angular.module('pss_admin',[]);
angular.module('pss_admin').controller(
    'app.pss_admin_controller',[
        '$scope','$state','resourceWrapperService','listGeneration','eventTournamentLib','credentialsService','$ionicScrollDelegate',
        function($scope, $state,resourceWrapperService,listGeneration, eventTournamentLib, credentialsService, $ionicScrollDelegate) {
            $scope.bootstrap({back_button:false});
            $scope.active_tab=1;
            $scope.toggle_tab = function(){
                $scope.active_tab=$scope.active_tab*-1;
            };
            var on_tournament_success = function(data){
                console.log(data);
                $scope.tournaments=data.tournaments;
            };
            var on_success = function(data){                
                $scope.items=data['events'];                                                                
                //$scope.event_create_wizard_pop($scope.items);
                var basic_sref='.edit_event_basic({id:item.event_id})';
                var advanced_sref='.edit_event_advanced({id:item.event_id})';                
                //var set_list_items_actions_and_args=listGeneration.generate_set_list_items_actions_and_args('event_name',
                //                                                                                            advanced_sref,
                //                                                                                            basic_sref
                //                                                                                           );
                var actions = [
                    {'label':'QuickCreate Tournament','ui_sref':'app.pss_admin.quickcreate_tournament'},
                    {'label':'Manage Tournament Machines','ui_sref':'app.pss_admin.manage_tournament_machines'},
                    {'label':'Manage Users','ui_sref':''},
                    {'label':'Manage Tournaments','ui_sref':'app.pss_admin.manage_tournaments'},                                        
                    {'label':'Edit Event','ui_sref':'app.pss_admin.edit_event_basic({id:item.event_id})'},
                    {'label':'Login to Event','ui_sref':''},                                        
                    
                ];
                var set_items_actions_and_args = listGeneration.generate_set_items_actions_and_args('event_name',actions);
                //_.map($scope.items, set_list_items_actions_and_args);
                _.map($scope.items, set_items_actions_and_args);
                _.map($scope.items, listGeneration.set_active_inactive_icon);
                $scope.toggle_item_active=eventTournamentLib.toggle_item_active;                
                var pss_user_id = credentialsService.get_credentials()['pss_admin'].pss_user_id;
                var test_event_creator = function (o) { return o.event_creator_pss_user_id==pss_user_id; };
                if(_.filter($scope.items, test_event_creator).length == 0){
                    $scope.event_create_wizard_pop('pss_admin','no_events');
                };
                if(_.filter($scope.items, test_event_creator).length > 0){
                    $scope.event_create_wizard_pop('pss_admin','1_event_no_tournaments');
                };                
                
            };
            ionic.DomUtil.ready(function(){
                $scope.scrollAmount = $ionicScrollDelegate.$getByHandle('tournamentlist').getScrollPosition().left;                
                var myElement = angular.element( document.querySelector( '.pooping' ) );
                                
            });

            var prom = resourceWrapperService.get_wrapper_with_loading('get_events',on_success,{},{});
            prom.then(function(data){
                if(data['events'].length==0){
                    return;
                }
                var tourney_prom = resourceWrapperService.get_wrapper_with_loading('get_tournaments',
                                                                                   on_tournament_success,
                                                                                   {event_name:data['events'][0].event_name},
                                                                                   {});
            });

            $scope.scrollCheck=function(){
                $scope.scrollAmount = $ionicScrollDelegate.$getByHandle('tournamentlist').getScrollPosition().left;
            };
        }
    ]);
angular.module('pss_admin').controller(
    'app.pss_admin.login_controller',[
        '$scope','$state','resourceWrapperService','credentialsService','$ionicNavBarDelegate','$rootScope',
        function($scope, $state,resourceWrapperService,credentialsService,$ionicNavBarDelegate,$rootScope ) {
            $scope.bootstrap({back_button:true});
            
            $scope.enable_back_button();
            $scope.pss_user={};            
            $scope.login_func = function(rest_resource,event){                
                var on_success = function(data){                    
                    $scope.logged_in_user=data['pss_user'];                    

                    //FIXME : HOLY SHIT IS THIS A BAD IDEA!!  NEED TO IMPLEMENT A
                    //        TIME LIMITED TOKEN SYSTEM SO THAT WE CAN LOGIN
                    //        TO EVENTS FROM EVENT MANAGEMENT WITHOUT HAVING TO ASK
                    //        FOR A PASSWORD.  Specifically, an endpoint on pss_admin
                    //        will give you a token which is a itsdangerous encoded
                    //        string (the current date/time/seconds/milliseconds)
                    //        which will expire in 10 seconds, and is recorded in the
                    //        pss_user table.  
                    //        This token can be used to login to a site for the next 10 seconds
                    
                    data['pss_user_password']=$scope.pss_user.password;
                    
                    credentialsService.set_pss_user_credentials(event,data);
                    $scope.post_success_handler("Logged In!",[['User Name',data['pss_user'].username]],$scope);

                };
                var url_params = {};
                if($scope.event_name != 'pss_admin'){
                    url_params = {event_name:$scope.event_name};
                }
                var prom =resourceWrapperService.get_wrapper_with_loading(rest_resource,on_success,url_params,{username:$scope.pss_user.username,password:$scope.pss_user.password});            
            };
        }
    ]);
angular.module('pss_admin').controller(
    'app.pss_admin.create_event_controller',[
        '$scope','$state','resourceWrapperService','credentialsService','$ionicNavBarDelegate','$rootScope',
        function($scope, $state,resourceWrapperService,credentialsService,$ionicNavBarDelegate,$rootScope ) {
            $scope.bootstrap({back_button:true});
            $scope.item={};            
            $scope.create_event_func = function(){                
                var on_success = function(data){
                    $scope.post_success_handler("Event Created!",[['Event Name',data['new_event'].name]],$scope);
                };
                $scope.item.active=true;
                var prom =resourceWrapperService.get_wrapper_with_loading('post_create_event',on_success,{},$scope.item);
            };
            var on_get_success = function(data){
                $scope.descriptions=data['descriptions'];
            };                        
            var prom =resourceWrapperService.get_wrapper_with_loading('get_event_descriptions',on_get_success,{},{});
        }
    ]);

