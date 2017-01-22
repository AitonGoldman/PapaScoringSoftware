angular.module('app.queues.machine_select',['app.queues.machine_select.machine_queue',
    /*REPLACEMECHILD*/]);
angular.module('app.queues.machine_select').controller(
    'app.queues.machine_select',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
        $scope.queueing_available = false;
        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);
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
    }]
);
