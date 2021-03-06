angular.module('app.scorekeeping.machine_select.record_score.confirm',[    'app.scorekeeping.machine_select.record_score.confirm.process',
                                                                           /*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.machine_select.record_score.confirm').controller(
    'app.scorekeeping.machine_select.record_score.confirm',[
        '$scope','$state','TimeoutResources','Utils','Modals','ActionSheets',
        function($scope, $state, TimeoutResources, Utils,Modals,ActionSheets) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
	$scope.division_machine_name=$state.params.division_machine_name;
	$scope.division_machine_id=$state.params.division_machine_id;
	$scope.player_id=$state.params.player_id;
	$scope.player_name=$state.params.player_name;
	$scope.score=$state.params.score;
            $scope.choose_void_action = ActionSheets.choose_void_action;
	//$scope.team_tournament=$state.params.team_tournament;            

            $scope.utils = Utils;
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
            $scope.bootstrap_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                $scope.team_tournament=$scope.resources.divisions.data[$scope.division_id].team_tournament;            
            });     
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
