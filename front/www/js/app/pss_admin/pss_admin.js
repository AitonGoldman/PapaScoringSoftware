
angular.module('pss_admin',[]);
angular.module('pss_admin').controller(
    'app.pss_admin_controller',[
        '$scope','$state','resourceWrapperService','listGeneration','eventTournamentLib',
        function($scope, $state,resourceWrapperService,listGeneration, eventTournamentLib) {
            $scope.bootstrap({});
            
            $scope.toggle_view_item_actions = listGeneration.toggle_view_item_actions;
            
            var on_success = function(data){
                $scope.items=data['events'];                
                var basic_sref='.edit_event_basic({id:item.event_id})';
                var advanced_sref='.edit_event_advanced({id:item.event_id})';
                var wizard_sref='.edit_event_wizard({id:item.event_id,wizard_step:1})';                
                var set_list_items_actions_and_args=listGeneration.generate_set_list_items_actions_and_args('event_name',
                                                                                                            advanced_sref,
                                                                                                            wizard_sref,
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
                    $scope.post_results={};
                    $scope.post_results.title="Logged In!";
                    $scope.post_results.results=[['User Name',data['pss_user'].username]];                    
                    $scope.post_success = true;                    
                    $scope.disable_back_button();
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
            var edit_route = $state.current.data.edit_route;
            var get_route = $state.current.data.get_route;            
            console.log(edit_route);
            var basic_edit=false;
            
            if($scope.wizard_step == undefined){                
                basic_edit=true;
            }
            if(_.isEmpty($state.params.item) && $scope.wizard_step > 1){
                $state.go('^');
            }
            if($scope.wizard_step>1){                
                $scope.item=$state.params.item;
                $scope.descriptions=$state.params.descriptions;
            }
            if(basic_edit == true || $scope.wizard_step == 1) {
                var on_success = function(data){                    
                    $scope.item=data['item'];
                    var orig_item_fields=[];
                    for(i in $scope.item){
                        orig_item_fields.push(i);
                    }
                    $scope.item.bobo={};
                    for(idx in orig_item_fields){
                        field_name = orig_item_fields[idx];
                        $scope.item.bobo[field_name]=$scope.item[field_name];
                    }
                    $scope.descriptions=data['descriptions'];                    
                };                            
                ////var prom =resourceWrapperService.get_wrapper_with_loading('get_event',on_success,{event_id:$state.params.event_id},{});                
                var prom =resourceWrapperService.get_wrapper_with_loading(get_route,on_success,{event_name:$state.params.event_name,id:$state.params.id},{});                        
            }                                    
            
            $scope.submit_button_disabled = function(item,num_fields){                
                if(_.isEmpty(item)){
                    return true;
                }                
                if(_.size(item)<num_fields && $scope.wizard_step > 0){
                    return true;
                }
                for(i in item){                    
                    if(item[i]==""){
                        return true;
                    }
                }                
                return false;
            };
            
            $scope.filter_id_field = function(field_name){
                if(field_name.indexOf("_id")>0 || field_name.indexOf("secret") > 0){
                    return false;
                } else {
                    return true;
                }
            };
            
            $scope.edit_event_func = function(event,result_fields){                
                event.wizard_configured=true;
                var on_success = function(data){                    
                    $scope.post_results={};
                    $scope.post_results.title="Event Edited!";
                    //FIXME : this should use descriptions we got from backend
                    var results = [];
                    
                    var item = data['item'];                    
                    // if(result_fields == undefined){
                    //     result_fields=[];
                    //     for(key in item){
                    //         if(key.indexOf('_id')==-1 && key.indexOf('secret')==-1){
                    //             result_fields.push(key);
                    //         }                            
                    //     }
                    // }                    
                    // for(result_field_idx in result_fields){
                    //     result_field = result_fields[result_field_idx];
                    //     results.push([$scope.descriptions.short_descriptions[result_field],item[result_field]]);
                    // }                    

                    // results = [];
                    for(field_name in item){
                        if(field_name=="bobo"){
                            continue;
                        }
                        if(field_name=="wizard_configured"){
                            continue;
                        }
                        if(_.isArray(item[field_name])){
                            continue;
                        }
                        if(_.isObject(item[field_name])){
                            continue;
                        }                        
                        
                        if(event.bobo[field_name]!=item[field_name]){
                            results.push([$scope.descriptions.short_descriptions[field_name],item[field_name]]);   
                        };
                    }
                    //FIXME : results page needs to say something about "these are the changed fields" on edit
                    $scope.post_results.results=results;                    
                    $scope.disable_back_button();
                    $scope.post_success = true;
                };                
                //var prom =resourceWrapperService.get_wrapper_with_loading('put_edit_event',on_success,{event_id:$state.params.event_id},event);
                var prom =resourceWrapperService.get_wrapper_with_loading(edit_route,on_success,{id:$state.params.id,event_name:$state.params.event_name},event);            
            };
        }
    ]);

