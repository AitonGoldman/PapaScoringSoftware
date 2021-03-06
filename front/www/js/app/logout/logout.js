angular.module('app.logout',[/*REPLACEMECHILD*/]);
angular.module('app.logout').controller(
    'app.logout',[
        '$scope','$state','TimeoutResources','Utils','Modals','User','$ionicHistory',
        function($scope, $state, TimeoutResources, Utils,Modals,User,$ionicHistory) {
            $ionicHistory.clearHistory();
            $scope.site=$state.params.site;            
            $scope.utils = Utils;
            Modals.loading();            
            logout_promise = TimeoutResources.Logout(undefined,{site:$scope.site});            
            logout_promise.then(function(data){            
                User.log_out();
                Modals.loaded();                
            });
            $scope.go_home = function(){
                $state.go('app',{},{reload:true});
            };
    }]
);
