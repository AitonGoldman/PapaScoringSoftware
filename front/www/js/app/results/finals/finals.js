angular.module('app.results.finals',['app.results.finals.final',
    /*REPLACEMECHILD*/]);
angular.module('app.results.finals').controller(
    'app.results.finals',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        finals_promise = TimeoutResources.GetDivisionFinals($scope.bootstrap_promise,{site:$scope.site});                
        finals_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });

        
             
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
