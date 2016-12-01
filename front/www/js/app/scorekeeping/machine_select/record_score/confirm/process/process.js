angular.module('app.scorekeeping.machine_select.record_score.confirm.process',['app.scorekeeping.machine_select.record_score.confirm.process.queue_add',
    /*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.machine_select.record_score.confirm.process').controller(
    'app.scorekeeping.machine_select.record_score.confirm.process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
	$scope.division_machine_name=$state.params.division_machine_name;
	$scope.division_machine_id=$state.params.division_machine_id;
        $scope.player_id = $state.params.player_id;
        $scope.player_name = $state.params.player_name;

        
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        
        $scope.confirmed_score=$state.params.confirmed_score;
        $scope.confirmed_score.score_with_commas = $scope.confirmed_score.score;
        $scope.confirmed_score.score = $scope.confirmed_score.score.replace(/,/g, '');
        add_score_promise = TimeoutResources.AddScore(undefined,{site:$scope.site,division_machine_id:$scope.division_machine_id,score:$scope.confirmed_score.score});
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        add_score_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });
    }]
);
