angular.module('event_select',[]);
angular.module('event_select').controller(
    'app.event_select_controller',[
        '$scope','$state','resourceWrapperService','listGeneration','$location',
        function($scope, $state,resourceWrapperService,listGeneration,$location) {            
            $scope.bootstrap({});            
            if($scope.is_event_html() || $scope.is_event_dns()){
                $state.go('app.pss_admin');
                return;
            } 
            
            var on_success = function(data){
                $scope.items=data['events'];
                var set_list_items_actions_and_args=listGeneration.generate_set_list_items_ui_sref_and_args('event_name',
                                                                                                            'poop');
                _.map($scope.items, set_list_items_actions_and_args);  
                
            };                        
            var prom =resourceWrapperService.get_wrapper_with_loading('get_events',on_success,{});            
        }
    ]);
