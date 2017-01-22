angular.module('app.scorekeeping',['app.scorekeeping.machine_select',
    /*REPLACEMECHILD*/]);
angular.module('app.scorekeeping').controller(
    'app.scorekeeping',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        //divisions_promise = TimeoutResources.GetDivisions(undefined,{site:$scope.site});        
             
        //
        // = TimeoutResources.GetEtcData();
        //divisions_promise.then(function(data){
        $scope.bootstrap_promise.then(function(data){
            Modals.loaded();
            $scope.resources = TimeoutResources.GetAllResources();
        });
    }]
);
