angular.module('event_select',[]);
angular.module('event_select').controller(
    'app.event_select_controller',[
        '$scope','$state','resourceWrapperService','$ionicNavBarDelegate',
        function($scope, $state,resourceWrapperService,$ionicNavBarDelegate) {            
            $scope.bootstrap({});            
            var on_success = function(data){$scope.events=data;};                        
            var prom =resourceWrapperService.get_wrapper_with_loading('get_events',on_success,{});            
        }
    ]);
