angular.module('app.logout',[/*REPLACEMECHILD*/]);
angular.module('app.logout').controller(
    'app.logout',[
        '$scope','$state','TimeoutResources','Utils','Modals','User',
        function($scope, $state, TimeoutResources, Utils,Modals,User) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        Modals.loading();            
        $logout_promise = TimeoutResources.Logout(undefined,{site:$scope.site});
        $logout_promise.then(function(data){            
            User.log_out();
            Modals.loaded();
        });
        
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResource.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);