angular.module('shared',[]);
angular.module('shared').controller(
    'app.shared.edit_event_tournament_controller',[
        '$scope','$state','resourceWrapperService','credentialsService','$ionicNavBarDelegate','$rootScope','eventTournamentLib',
        function($scope, $state,resourceWrapperService,credentialsService,$ionicNavBarDelegate,$rootScope,eventTournamentLib ) {                        
            $scope.bootstrap({back_button:true});
            $scope.wizard_step = $state.params.wizard_step;                                    

            var edit_route = $state.current.data.edit_route;
            var get_route = $state.current.data.get_route;                        
            var basic_or_advanced_edit=false;
            
            if($scope.wizard_step == undefined){                
                basic_or_advanced_edit=true;
            }
            if(_.isEmpty($state.params.item) && $scope.wizard_step > 1){
                $state.go('^');
            }
            if($scope.wizard_step>1){                
                $scope.item=$state.params.item;
                $scope.descriptions=$state.params.descriptions;
            }
            var on_get_success = function(data){                    
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

            var on_edit_success = function(data){                    
                $scope.post_results={};
                $scope.post_results.title="Event Edited!";                    
                var results = [];
                
                var item = data['item'];                    
                for(field_name in item){
                    if(field_name=="bobo"){continue;}
                    if(field_name=="wizard_configured"){continue;}
                    if(_.isArray(item[field_name])){continue;}
                    if(_.isObject(item[field_name])){continue;}                                            
                    if(event.bobo[field_name]!=item[field_name]){
                        results.push([$scope.descriptions.short_descriptions[field_name],item[field_name]]);   
                    };
                }
                //FIXME : results page needs to say something about "these are the changed fields" on edit
                $scope.post_results.results=results;                    
                $scope.disable_back_button();
                $scope.post_success = true;
            };                                
            
            if(basic_or_advanced_edit == true || $scope.wizard_step == 1) {
                var prom =resourceWrapperService.get_wrapper_with_loading(get_route,on_get_success,{event_name:$state.params.event_name,id:$state.params.id},{});                
            }                                    
                                    
            $scope.edit_event_func = function(event,result_fields){                
                event.wizard_configured=true;
                var prom =resourceWrapperService.get_wrapper_with_loading(edit_route,on_edit_success,{id:$state.params.id,event_name:$state.params.event_name},event);
            };
        }
    ]);
