angular.module('app.user',['app.user.add_user',
    'app.user.edit_user',
    /*REPLACEMECHILD*/]);
angular.module('app.user').controller(
    'app.user',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        
        Modals.loading();
        get_users_promise = TimeoutResources.GetUsers($scope.bootstrap_promise,{site:$scope.site});        
        // = TimeoutResources.GetEtcData();
        get_users_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            console.log($scope.resources.users);
            Modals.loaded();
        });
    }]
);
