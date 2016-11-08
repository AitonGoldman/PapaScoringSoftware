angular.module('app.tournament.edit_tournament',['app.tournament.edit_tournament.process',
    /*REPLACEMECHILD*/]);
angular.module('app.tournament.edit_tournament').controller(
    'app.tournament.edit_tournament',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        
        Modals.loading();
        division_promise = TimeoutResources.GetDivision(undefined,{site:$scope.site,division_id:$scope.division_id});
        // = TimeoutResources.GetEtcData();
        division_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            $scope.division = $scope.resources.division.data;
            $scope.tournament = $scope.resources.division.data;
            console.log($scope.division);
            Modals.loaded();
        });
    }]
);
