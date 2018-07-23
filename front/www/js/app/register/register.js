angular.module('register',[]);
angular.module('register').controller(
    'app.register_new_pss_user_controller',[
        '$scope','$state','$ionicScrollDelegate','resourceWrapperService',
        function($scope, $state,$ionicScrollDelegate,resourceWrapperService) {
            $scope.bootstrap({back_button:true});            
            $scope.new_pss_user={};            
            $scope.request_register_pss_user_func = function(){                                
                var on_success = function(data){                    
                    $scope.post_success = true;                    
                };
                                
                var prom_register_user = resourceWrapperService.get_wrapper_with_loading('post_request_register_pss_user',
                                                                                         on_success,
                                                                                         {},
                                                                                         $scope.new_pss_user);            

            };
        }]);

angular.module('register').controller(
    'app.register_new_pss_user_confirm_controller',[
        '$scope','$state','$ionicScrollDelegate','resourceWrapperService','$location',
        function($scope, $state,$ionicScrollDelegate,resourceWrapperService,$location) {
            $scope.bootstrap({back_button:true});            
            $scope.new_pss_user={};
            var itsdangerous_string = $location.search()['itsdangerous'];
            var on_success = function(data){                    
                
            };                                
            var prom_register_user = resourceWrapperService.get_wrapper_with_loading('get_confirm_register_pss_user',
                                                                                     on_success,
                                                                                     {itsdangerous:itsdangerous_string},
                                                                                     {});            
        }]);
