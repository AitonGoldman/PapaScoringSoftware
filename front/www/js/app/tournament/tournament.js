angular.module('app.tournament',['app.tournament.add_tournament',
    /*REPLACEMECHILD*/]);
angular.module('app.tournament').controller(
    'app.tournament',[
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
