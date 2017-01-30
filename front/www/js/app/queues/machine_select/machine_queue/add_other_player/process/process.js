angular.module('app.queues.machine_select.machine_queue.add_other_player.process',[/*REPLACEMECHILD*/]);
angular.module('app.queues.machine_select.machine_queue.add_other_player.process').controller(
    'app.queues.machine_select.machine_queue.add_other_player.process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_machine_name=$state.params.division_machine_name;
	$scope.other_player_id=$state.params.other_player_id;
	$scope.manage=$state.params.manage;
	$scope.division_id=$state.params.division_id;
	$scope.division_machine_id=$state.params.division_machine_id;
	$scope.other_player_pin=$state.params.other_player_pin;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        other_player_data = {
            division_machine_id:$scope.division_machine_id,
            other_player_id:$scope.other_player_id,
            other_player_pin:$scope.other_player_pin
        };
        other_player_add = TimeoutResources.AddOtherPlayerToQueue($scope.bootstrap_promise,{site:$scope.site},other_player_data);
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        other_player_add.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        }, function(error){
            Modals.error(error.data.message, $scope.site, '^');                        
        });
    }]
);
