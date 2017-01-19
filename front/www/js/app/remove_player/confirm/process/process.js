angular.module('app.remove_player.confirm.process',[/*REPLACEMECHILD*/]);
angular.module('app.remove_player.confirm.process').controller(
    'app.remove_player.confirm.process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.player_id=$state.params.player_id;
	$scope.division_machine_id=$state.params.division_machine_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }        
        remove_promise = TimeoutResources.RemovePlayerFromMachine($scope.bootstrap_promise,
                                                                  {site:$scope.site,
                                                                   player_id:$scope.player_id,
                                                                   division_machine_id:$scope.division_machine_id});
     
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        remove_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });
    }]
);
