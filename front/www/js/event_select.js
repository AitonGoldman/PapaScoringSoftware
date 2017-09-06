angular.module('event_select',[]);
angular.module('event_select').controller(
    'event_select_controller',[
        '$scope','$state','resourceWrapperService',
        function($scope, $state,resourceWrapperService) {            
            var on_success = function(data){$scope.events=data;};
            //var on_failure = resourceWrapperService.generate_on_failure('.');
            var on_failure = resourceWrapperService.stay_on_current_state_for_error;            
            var prom =resourceWrapperService.get_wrapper_with_loading('events',on_success,on_failure);            
        }
    ]);
