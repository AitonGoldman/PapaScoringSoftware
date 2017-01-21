angular.module('app.logout',[/*REPLACEMECHILD*/]);
angular.module('app.logout').controller(
    'app.logout',[
        '$scope','$state','TimeoutResources','Utils','Modals','User',
        function($scope, $state, TimeoutResources, Utils,Modals,User) {
            $scope.site=$state.params.site;            
            $scope.utils = Utils;
            Modals.loading();
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                        
            logout_promise = TimeoutResources.Logout(undefined,{site:$scope.site});            
            logout_promise.then(function(data){            
                User.log_out();
                Modals.loaded();
            });        
    }]
);
