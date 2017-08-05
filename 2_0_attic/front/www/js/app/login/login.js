angular.module('app.login',['app.login.process',
    /*REPLACEMECHILD*/]);
angular.module('app.login').controller(
    'app.login',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils=Utils;
        //$scope.controller_bootstrap($scope,$state);                
        $scope.user = {};
        //FIXME : should reroute to home if already logged in
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResource.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
