angular.module('app.user',['app.user.add_user',
    /*REPLACEMECHILD*/]);
angular.module('app.user').controller(
    'app.user',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
             
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResource.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
