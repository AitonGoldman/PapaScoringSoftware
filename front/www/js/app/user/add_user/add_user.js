angular.module('app.user.add_user',['app.user.add_user.process',
    /*REPLACEMECHILD*/]);
angular.module('app.user.add_user').controller(
    'app.user.add_user',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        $scope.user_info={roles:{}};        
        Modals.loading();
        get_roles_promise = TimeoutResources.GetRoles(undefined,{site:$scope.site});
        // = TimeoutResources.GetEtcData();
        get_roles_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });
    }]
);
