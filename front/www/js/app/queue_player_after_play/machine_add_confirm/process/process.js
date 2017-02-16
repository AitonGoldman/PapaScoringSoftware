angular.module('app.queue_player_after_play.machine_add_confirm.process',[/*REPLACEMECHILD*/]);
angular.module('app.queue_player_after_play.machine_add_confirm.process').controller(
    'app.queue_player_after_play.machine_add_confirm.process',[
        '$scope','$state','TimeoutResources','Utils','Modals','$ionicHistory',
        function($scope, $state, TimeoutResources, Utils,Modals,$ionicHistory) {
            $ionicHistory.nextViewOptions({disableBack:true});            

            $scope.site=$state.params.site;
	$scope.player_id=$state.params.player_id;
	$scope.division_machine_just_played_id=$state.params.division_machine_just_played_id;
	$scope.division_name=$state.params.division_name;
	$scope.player_name=$state.params.player_name;
	$scope.division_machine_to_add_to_id=$state.params.division_machine_to_add_to_id;
	$scope.division_id=$state.params.division_id;
	$scope.division_machine_to_add_to_name=$state.params.division_machine_to_add_to_name;
	$scope.division_machine_just_played_name=$state.params.division_machine_just_played_name;

        $scope.utils = Utils;
        Modals.loading();        
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        
        add_player_to_machine_promise = TimeoutResources.AddPlayerToMachine($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id,division_machine_id:$scope.division_machine_to_add_to_id,player_id:$scope.player_id});
            //= TimeoutResources.GetEtcData();
        add_player_to_machine_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
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
