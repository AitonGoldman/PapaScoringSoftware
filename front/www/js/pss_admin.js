angular.module('pss_admin',[]);
angular.module('pss_admin').controller(
    'pss_admin_controller',[
        '$scope','$state','resourceWrapperService','credentialsService','$ionicNavBarDelegate','$rootScope',
        function($scope, $state,resourceWrapperService,credentialsService,$ionicNavBarDelegate,$rootScope ) {                        
            $rootScope.credentials=credentialsService;            
            $scope.state = $state;
            $scope.viewnum="";            
            //$ionicNavBarDelegate.title($state.current.data.title);
            
            //var on_success = function(data){$scope.events=data;};
            //var on_failure = resourceWrapperService.generate_on_failure('.');
            //var on_failure = resourceWrapperService.stay_on_current_state_for_error;            
            //var prom =resourceWrapperService.get_wrapper_with_loading('events',on_success,on_failure);            
        }
    ]);

