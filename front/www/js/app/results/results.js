angular.module('app.results',['app.results.divisions',
    'app.results.division_machines',
    'app.results.players',
    /*REPLACEMECHILD*/]);
angular.module('app.results').controller(
    'app.results',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
             
        $scope.bootstrap_promise.then(function(data){
        $scope.resources = TimeoutResources.GetAllResources();
         Modals.loaded();
        })
    }]
);
