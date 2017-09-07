angular.module('app',['event_select','pss_admin']);
angular.module('app').controller(
    'app_controller',[
        '$scope','$state','credentialsService','$ionicNavBarDelegate','$rootScope','$cookies',
        function($scope, $state,credentialsService,$ionicNavBarDelegate,$rootScope,$cookies ) {
            if ($rootScope.credentials == undefined){
                $rootScope.credentials=credentialsService;
            }
            $scope.test_alert = function(message){
                alert(message);
            };
            $scope.bootstrap = function(){
                //FIXME : rely on cookies to tell us if we are logged in after page reload                
                $scope.state = $state;
                $ionicNavBarDelegate.title($state.current.data.title);
            };
        }
    ]
);
