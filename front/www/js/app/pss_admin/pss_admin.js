angular.module('pss_admin',[]);
angular.module('pss_admin').controller(
    'app.pss_admin_controller',[
        '$scope','$state','resourceWrapperService','credentialsService','$ionicNavBarDelegate','$rootScope',
        function($scope, $state,resourceWrapperService,credentialsService,$ionicNavBarDelegate,$rootScope ) {
            $scope.bootstrap();
        }
    ]);
angular.module('pss_admin').controller(
    'app.pss_admin.login_controller',[
        '$scope','$state','resourceWrapperService','credentialsService','$ionicNavBarDelegate','$rootScope',
        function($scope, $state,resourceWrapperService,credentialsService,$ionicNavBarDelegate,$rootScope ) {
            $scope.pss_user={};
            $scope.bootstrap();
            $scope.login_func = function(){
                $scope.post_success = false;
                var on_success = function(data){
                    $scope.logged_in_user=data['pss_user'];
                    credentialsService.set_pss_user_credentials("pss_admin",data);
                    $scope.post_success = true;
                };
                
                var on_failure = resourceWrapperService.stay_on_current_state_for_error;            
                var prom =resourceWrapperService.get_wrapper_with_loading('post_pss_admin_login',on_success,on_failure,{},{username:$scope.pss_user.username,password:$scope.pss_user.password});            

            };
        }
    ]);

