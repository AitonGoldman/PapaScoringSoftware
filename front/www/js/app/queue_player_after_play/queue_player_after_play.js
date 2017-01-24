angular.module('app.queue_player_after_play',['app.queue_player_after_play.confirm',
    /*REPLACEMECHILD*/]);
angular.module('app.queue_player_after_play').controller(
    'app.queue_player_after_play',[
        '$scope','$state','TimeoutResources','Utils','Modals','ActionSheets',
        function($scope, $state, TimeoutResources, Utils,Modals,ActionSheets) {
        $scope.site=$state.params.site;
	$scope.player_id=$state.params.player_id;
	$scope.division_id=$state.params.division_id;
	$scope.player_name=$state.params.player_name;
        //FIXME : need to add this info at the scorekeeping route level
        $scope.division_name=$state.params.division_name;
        $scope.division_machine_just_played_id=$state.params.division_machine_just_played_id;
        $scope.utils = Utils;
        $scope.queueing_available = false;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        //division_machines_promise = TimeoutResources.GetDivisionMachines($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id});                
        queues_promise = TimeoutResources.GetQueues($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id});
        
        queues_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();            
            _.forEach($scope.resources.queues.data, function(machine, key) {
                
                if(machine.queues.length > 0 || machine.player_id != undefined){                    
                    $scope.queueing_available = true;
                }
            });

            Modals.loaded();
        });
        $scope.choose_queue_action_or_no_action = function(division_machine){            
            if(division_machine.player_id == undefined && division_machine.queues.length > 0){
                //$state.go('.machine_queue',{division_machine_id:division_machine.division_machine_id,division_machine_name:division_machine.division_machine_name});
                $state.go('.confirm',{division_machine_to_queue_on_id:division_machine.division_machine_id,division_machine_to_queue_on_name:division_machine.division_machine_name});
                return;
            }
            if(division_machine.player_id != undefined){
                $state.go('.confirm',{division_machine_to_queue_on_id:division_machine.division_machine_id,division_machine_to_queue_on_name:division_machine.division_machine_name});                
                //$state.go('.machine_queue',{division_machine_id:division_machine.division_machine_id,division_machine_name:division_machine.division_machine_name});
                return;
            }
            
            ActionSheets.queue_no_action();
            //ui-sref='.machine_queue({division_machine_id:division_machine.division_machine_id,division_machine_name:division_machine.division_machine_name})'
        };
        
        //ui-sref='.confirm({division_machine_to_queue_on_id:division_machine.division_machine_id,division_machine_to_queue_on_name:division_machine.division_machine_name})'
    }]
);
