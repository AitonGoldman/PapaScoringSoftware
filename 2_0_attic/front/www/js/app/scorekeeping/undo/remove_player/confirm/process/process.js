angular.module('app.scorekeeping.undo.remove_player.confirm.process',['app.scorekeeping.undo.remove_player.confirm.process.add_player',
    /*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.undo.remove_player.confirm.process').controller(
    'app.scorekeeping.undo.remove_player.confirm.process',[
        '$scope','$state','TimeoutResources','Utils','Modals','$ionicHistory',
        function($scope, $state, TimeoutResources, Utils,Modals,$ionicHistory) {
            $ionicHistory.nextViewOptions({                
                disableBack: true
            });


            $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
	$scope.division_machine_id=$state.params.division_machine_id;
        $scope.division_machine_name=$state.params.division_machine_name;
	$scope.player_id=$state.params.player_id;
	$scope.player_name=$state.params.player_name;

        $scope.utils = Utils;
        Modals.loading();
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
     
        
        // = TimeoutResources.GetEtcData();
        remove_promise.then(function(data){
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
