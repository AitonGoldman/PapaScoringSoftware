angular.module('app.scorekeeping.machine_select.record_score.confirm_jagoff',['app.scorekeeping.machine_select.record_score.confirm_jagoff.process',
    /*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.machine_select.record_score.confirm_jagoff').controller(
    'app.scorekeeping.machine_select.record_score.confirm_jagoff',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
	$scope.team_tournament=$state.params.team_tournament;
	$scope.score=$state.params.score;
	$scope.player_id=$state.params.player_id;
	$scope.division_machine_id=$state.params.division_machine_id;
	$scope.player_name=$state.params.player_name;
	$scope.division_machine_name=$state.params.division_machine_name;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
             
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
