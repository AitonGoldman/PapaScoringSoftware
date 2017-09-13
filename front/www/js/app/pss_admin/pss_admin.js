
angular.module('pss_admin',[]);
angular.module('pss_admin').controller(
    'app.pss_admin_controller',[
        '$scope','$state','resourceWrapperService','listGeneration',
        function($scope, $state,resourceWrapperService,listGeneration ) {
            $scope.bootstrap({});

            $scope.toggle_view_item_actions = listGeneration.toggle_view_item_actions;
            
            var on_success = function(data){
                $scope.items=data['events'];                
                var basic_sref='.edit_event_basic({event_id:item.event_id})';
                var advanced_sref='.edit_event({event_id:item.event_id})';
                var wizard_sref='.edit_event_wizard({event_id:item.event_id,wizard_step:1})';
                var set_list_items_actions_and_args=listGeneration.generate_set_list_items_actions_and_args('event_name',
                                                                                                            advanced_sref,
                                                                                                            wizard_sref,
                                                                                                            basic_sref
                                                                                                           );
                _.map($scope.items, set_list_items_actions_and_args);  
            };                        
            var prom =resourceWrapperService.get_wrapper_with_loading('get_events',on_success,{},{});                        
        }
    ]);
angular.module('pss_admin').controller(
    'app.pss_admin.login_controller',[
        '$scope','$state','resourceWrapperService','credentialsService','$ionicNavBarDelegate','$rootScope',
        function($scope, $state,resourceWrapperService,credentialsService,$ionicNavBarDelegate,$rootScope ) {
            $scope.bootstrap({back_button:true});
            $scope.pss_user={};            
            $scope.login_func = function(){                
                var on_success = function(data){
                    $scope.logged_in_user=data['pss_user'];
                    credentialsService.set_pss_user_credentials("pss_admin",data);
                    $scope.post_results={};
                    $scope.post_results.title="Logged In!";
                    $scope.post_results.results=[['User Name',data['pss_user'].username]];                    
                    $scope.post_success = true;
                    $scope.disable_back_button();
                };
                                
                var prom =resourceWrapperService.get_wrapper_with_loading('post_pss_admin_login',on_success,{},{username:$scope.pss_user.username,password:$scope.pss_user.password});            

            };
        }
    ]);
angular.module('pss_admin').controller(
    'app.pss_admin.create_event_controller',[
        '$scope','$state','resourceWrapperService','credentialsService','$ionicNavBarDelegate','$rootScope',
        function($scope, $state,resourceWrapperService,credentialsService,$ionicNavBarDelegate,$rootScope ) {
            $scope.bootstrap({back_button:true});
            $scope.event={};            
            $scope.create_event_func = function(){                
                var on_success = function(data){
                    // $scope.logged_in_user=data['new_event'];
                    $scope.post_results={};
                    $scope.post_results.title="Event Created!";
                    $scope.post_results.results=[['Event Name',data['new_event'].name]];                                        
                    $scope.disable_back_button();
                    $scope.post_success = true;
                    
                };                                
                var prom =resourceWrapperService.get_wrapper_with_loading('post_create_event',on_success,{},{name:$scope.event.name});            

            };
        }
    ]);

angular.module('pss_admin').controller(
    'app.pss_admin.edit_event_controller',[
        '$scope','$state','resourceWrapperService','credentialsService','$ionicNavBarDelegate','$rootScope',
        function($scope, $state,resourceWrapperService,credentialsService,$ionicNavBarDelegate,$rootScope ) {                        
            $scope.bootstrap({back_button:true});
            $scope.wizard_step = $state.params.wizard_step;                        
            var basic_edit=false;
            
            if($scope.wizard_step == ""){                
                basic_edit=true;
            }
            if(_.isEmpty($state.params.event) && $scope.wizard_step > 1){
                $state.go('app.pss_admin');
            }
            if($scope.wizard_step>1){                
                $scope.item=$state.params.event;
                $scope.descriptions=$state.params.descriptions;
            }
            if(basic_edit == true || $scope.wizard_step == 1) {
                var on_success = function(data){
                    $scope.item=data['event'];
                    $scope.descriptions=data['descriptions'];                    
                };                            
                var prom =resourceWrapperService.get_wrapper_with_loading('get_event',on_success,{event_id:$state.params.event_id},{});                        
            }                                    
            
            $scope.submit_button_disabled = function(event,num_fields){                
                if(_.isEmpty(event)){
                    return true;
                }                
                if(_.size(event)<num_fields && $scope.wizard_step > 0){
                    return true;
                }
                for(i in event){                    
                    if(event[i]==""){
                        return true;
                    }
                }                
                return false;
            };
            
            $scope.edit_event_func = function(event){                
                event.wizard_configured=true;
                var on_success = function(data){                    
                    $scope.post_results={};
                    $scope.post_results.title="Event Edited!";
                    //FIXME : this should use descriptions we got from backend
                    $scope.post_results.results=[['Queue Bump Amount',event.queue_bump_amount],
                                                 ['Allowed Unused Tickets',event.number_unused_tickets_allowed],
                                                 ['Player Id Sequence Start',event.player_id_seq_start]
                                                ];                                        
                    $scope.disable_back_button();
                    $scope.post_success = true;
                };                
                var prom =resourceWrapperService.get_wrapper_with_loading('put_edit_event',on_success,{event_id:$state.params.event_id},event);            

            };
        }
    ]);

