angular.module('app.queues.machine_select',['app.queues.machine_select.machine_queue',
    /*REPLACEMECHILD*/]);
angular.module('app.queues.machine_select').controller(
    'app.queues.machine_select',[
        '$scope','$state','TimeoutResources','Utils','Modals','ActionSheets',
        function($scope, $state, TimeoutResources, Utils,Modals,ActionSheets) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
        $scope.queueing_available = false;
        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);
        queues_promise = TimeoutResources.GetQueues($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id});
        queues_promise.then(function(data){            
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });
        //division_machine_id:division_machine.division_machine_id,division_machine_name:division_machine.division_machine_name
        $scope.choose_queue_action_or_no_action = function(division_machine){            
            if(division_machine.player_id == undefined && division_machine.queues.length > 0){
                $state.go('.machine_queue',{division_machine_id:division_machine.division_machine_id,division_machine_name:division_machine.division_machine_name});
                return;
            }
            if(division_machine.player_id != undefined){
                $state.go('.machine_queue',{division_machine_id:division_machine.division_machine_id,division_machine_name:division_machine.division_machine_name});
                return;
            }
            
            ActionSheets.queue_no_action();            
        };
        $scope.doRefresh = function() {
            queues_promise = TimeoutResources.GetQueues($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id});
            queues_promise.then(function(data){
                $scope.$broadcast('scroll.refreshComplete');                
            });
        };                
    }]
);
