
angular.module('pss_admin',[]);
angular.module('pss_admin').controller(
    'app.pss_admin_controller',[
        '$scope','$state','resourceWrapperService','listGeneration','eventTournamentLib',
        function($scope, $state,resourceWrapperService,listGeneration, eventTournamentLib) {
            $scope.bootstrap({back_button:false});            
            var on_success = function(data){                
                $scope.items=data['events'];                
                //$scope.wizard_mode_pop();
                $scope.event_create_wizard_pop($scope.items);
                var basic_sref='.edit_event_basic({id:item.event_id})';
                var advanced_sref='.edit_event_advanced({id:item.event_id})';                
                var set_list_items_actions_and_args=listGeneration.generate_set_list_items_actions_and_args('event_name',
                                                                                                            advanced_sref,
                                                                                                            basic_sref
                                                                                                           );
                _.map($scope.items, set_list_items_actions_and_args);
                _.map($scope.items, listGeneration.set_active_inactive_icon);
                $scope.toggle_item_active=eventTournamentLib.toggle_item_active;                
            };                        
            var prom =resourceWrapperService.get_wrapper_with_loading('get_events',on_success,{},{});                        
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
                var prom =resourceWrapperService.get_wrapper_with_loading('post_create_event',on_success,{},$scope.item);
            };
            var on_get_success = function(data){
                $scope.descriptions=data['descriptions'];
            };                        
            var prom =resourceWrapperService.get_wrapper_with_loading('get_event_descriptions',on_get_success,{},{});
        }
    ]);

