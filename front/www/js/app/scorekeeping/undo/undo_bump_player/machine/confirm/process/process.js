angular.module('app.scorekeeping.undo.undo_bump_player.confirm.process',[/*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.undo.undo_bump_player.confirm.process').controller(
    'app.scorekeeping.undo.undo_bump_player.confirm.process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.player_id=$state.params.player_id;
	$scope.player_name=$state.params.player_name;

	$scope.division_id=$state.params.division_id;
	$scope.division_machine_id=$state.params.division_machine_id;
	$scope.division_machine_name=$state.params.division_machine_name;

        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        add_player_to_machine_promise = TimeoutResources.AddPlayerToMachine($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id,division_machine_id:$scope.division_machine_id,player_id:$scope.player_id});
        //= TimeoutResources.GetEtcData();
        add_player_to_machine_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            $scope.team_tournament = $scope.resources.divisions.data[$scope.division_id].team_tournament;
            console.log($scope.resources);
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
