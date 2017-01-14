angular.module('app.tournament.division_list.edit_division',['app.tournament.division_list.edit_division.process',
    'app.tournament.division_list.edit_division.division_machine_list',
    /*REPLACEMECHILD*/]);
angular.module('app.tournament.division_list.edit_division').controller(
    'app.tournament.division_list.edit_division',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
	$scope.tournament_id=$state.params.tournament_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        Modals.loading();
        division_promise = TimeoutResources.GetDivision($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id});
        // = TimeoutResources.GetEtcData();
        division_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            $scope.division = $scope.resources.division.data;
            $scope.tournament = $scope.resources.division.data;
            console.log($scope.division);
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
