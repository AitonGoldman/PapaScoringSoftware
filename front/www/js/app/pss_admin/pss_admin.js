angular.module('pss_admin',[]);
angular.module('pss_admin').controller(
    'app.pss_admin_controller',[
        '$scope','$state','resourceWrapperService','credentialsService','$ionicNavBarDelegate','$rootScope',
        function($scope, $state,resourceWrapperService,credentialsService,$ionicNavBarDelegate,$rootScope ) {
            $scope.bootstrap({});
            
            $scope.toggle_view_item_actions = function(item){
                if(item.display_actions==undefined){
                    item.display_actions=true;
                    return;
                }
                item.display_actions=item.display_actions==false;
            };
            
            var set_list_items_ui_sref_and_args = function(i) {                
                //FIXME : the label_to_display should probably be set on the backend? Not sure about this
                i.ui_sref='app.pss_admin.edit_event({event_id:event.event_id})';
                i.label_to_display=i.event_name;                
            };
            var set_list_items_actions_and_args = function(i) {                
                //FIXME : the label_to_display should probably be set on the backend? Not sure about this
                i.actions_ui_sref_list = [{label:"Advanced Editing",ui_sref:"app.pss_admin.edit_event({event_id:event.event_id})"}];
                if(i.wizard_configured == false){
                    basic_edit_action = {label:"Wizard Configuration",ui_sref:"app.pss_admin.edit_event_wizard({event_id:event.event_id,wizard_step:1})"};
                } else {
                    basic_edit_action = {label:"Basic Editing",ui_sref:"app.pss_admin.edit_event_basic({event_id:event.event_id,wizard_step:0})"};
                }
                i.actions_ui_sref_list.splice(0,0,basic_edit_action);
                i.label_to_display=i.event_name;                
            };             
            var on_success = function(data){
                $scope.events=data['events'];
                //_.map($scope.events, set_list_items_ui_sref_and_args);
                _.map($scope.events, set_list_items_actions_and_args);  
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
    'app.pss_admin.edit_event_wizard_controller',[
        '$scope','$state','resourceWrapperService','credentialsService','$ionicNavBarDelegate','$rootScope',
        function($scope, $state,resourceWrapperService,credentialsService,$ionicNavBarDelegate,$rootScope ) {            
            $scope.wizard_step = $state.params.wizard_step;
            if(_.isEmpty($state.params.event) && $scope.wizard_step > 1){
                $state.go('app.pss_admin');
            }
            //if($scope.wizard_step==0){
            //    $scope.event={};
            //} else {
            if($scope.wizard_step!=0){
                $scope.event=$state.params.event;    
            } else {
                var on_success = function(data){
                    $scope.event=data['event'];
                    //_.map($scope.events, set_list_items_ui_sref_and_args);
                    //_.map($scope.events, set_list_items_actions_and_args);  
                };                            
                var prom =resourceWrapperService.get_wrapper_with_loading('get_event',on_success,{event_id:$state.params.event_id},{});                        
            }
            
            //}
            $scope.bootstrap({back_button:true});            
            
            $scope.submit_button_disabled = function(event,num_fields){                
                if(_.isEmpty(event)){
                    return true;
                }                
                if(_.size(event)<num_fields && $scope.wizard_step > 0){
                    return true;
                }
                for(i in event){
                    console.log(i);
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
                    $scope.post_results.results=[['Queue Bump Amount',event.queue_bump_amount],
                                                 ['Allowed Unused Tickets',event.number_unused_tickets_allowed],
                                                 ['Player Id Sequence Start',event.player_id_seq_start]
                                                ];                                        
                    $scope.disable_back_button();
                    $scope.post_success = true;
                };                
                //var on_failure = resourceWrapperService.stay_on_current_state_for_error;            
                //var prom =resourceWrapperService.get_wrapper_with_loading('put_edit_event',on_success,on_failure,{event_id:$state.params.event_id},event); 
                var prom =resourceWrapperService.get_wrapper_with_loading('put_edit_event',on_success,{event_id:$state.params.event_id},event);            

            };
        }
    ]);

