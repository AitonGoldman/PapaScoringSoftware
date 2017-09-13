angular.module('event_select',[]);
angular.module('event_select').controller(
    'app.event_select_controller',[
        '$scope','$state','resourceWrapperService','listGeneration',
        function($scope, $state,resourceWrapperService,listGeneration) {            
            $scope.bootstrap({});            
            var on_success = function(data){
                $scope.items=data['events'];
                var set_list_items_actions_and_args=listGeneration.generate_set_list_items_ui_sref_and_args('event_name',
                                                                                                            'poop');
                _.map($scope.items, set_list_items_actions_and_args);  
                
            };                        
            var prom =resourceWrapperService.get_wrapper_with_loading('get_events',on_success,{});            
        }
    ]);
