angular.module('app.scorekeeping.undo.remove_player.confirm.process.add_player.process',[/*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.undo.remove_player.confirm.process.add_player.process').controller(
    'app.scorekeeping.undo.remove_player.confirm.process.add_player.process',[
        '$scope','$state','TimeoutResources','Utils','Modals','$ionicHistory',
        function($scope, $state, TimeoutResources, Utils,Modals,$ionicHistory) {
        $scope.site=$state.params.site;
	$scope.player_id=$state.params.player_id;
	$scope.division_id=$state.params.division_id;
	$scope.player_name_to_add=$state.params.player_name_to_add;
	$scope.division_machine_id=$state.params.division_machine_id;
	$scope.division_machine_name=$state.params.division_machine_name;
	$scope.player_name=$state.params.player_name;
	$scope.player_id_to_add=$state.params.player_id_to_add;
        $ionicHistory.nextViewOptions({                
            disableBack: true
        });

        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        add_player_to_machine_promise = TimeoutResources.AddPlayerToMachine($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id,division_machine_id:$scope.division_machine_id,player_id:$scope.player_id_to_add});
        //= TimeoutResources.GetEtcData();
        add_player_to_machine_promise.then(function(data){
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
