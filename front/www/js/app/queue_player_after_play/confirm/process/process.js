angular.module('app.queue_player_after_play.confirm.process',[/*REPLACEMECHILD*/]);
angular.module('app.queue_player_after_play.confirm.process').controller(
    'app.queue_player_after_play.confirm.process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
	$scope.player_id=$state.params.player_id;        
	$scope.player_name=$state.params.player_name;        
        $scope.division_machine_just_played_id=$state.params.division_machine_just_played_id;
        $scope.division_machine_just_played_name=$state.params.division_machine_just_played_name;        
        $scope.division_machine_to_queue_on_id=$state.params.division_machine_to_queue_on_id;
	$scope.division_machine_to_queue_on_name=$state.params.division_machine_to_queue_on_name;        

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        add_to_queue_promise = TimeoutResources.AddToQueue($scope.bootstrap_promise,{site:$scope.site},{division_machine_id:$scope.division_machine_to_queue_on_id,player_id:$scope.player_id});
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        add_to_queue_promise.then(function(data){
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
