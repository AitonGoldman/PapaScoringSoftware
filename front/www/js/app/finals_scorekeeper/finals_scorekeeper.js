angular.module('app.finals_scorekeeper',['app.finals_scorekeeper.division_final',
    /*REPLACEMECHILD*/]);
angular.module('app.finals_scorekeeper').controller(
    'app.finals_scorekeeper',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        finals_promise = TimeoutResources.GetDivisionFinals($scope.bootstrap_promise,{site:$scope.site});        
        // = TimeoutResources.GetEtcData();
        finals_promise.then(function(data){
         $scope.resources = TimeoutResources.GetAllResources();
          Modals.loaded();
        });
    }]
);
