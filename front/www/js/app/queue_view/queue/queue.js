angular.module('app.queue_view.queue',[/*REPLACEMECHILD*/]);
angular.module('app.queue_view.queue').controller(
    'app.queue_view.queue',[
        '$scope','$state','TimeoutResources','Utils','Modals','$timeout',
        function($scope, $state, TimeoutResources, Utils,Modals,$timeout) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
        $scope.start_range = $state.params.start_range;
        $scope.end_range = $state.params.end_range;
        
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);
            var get_queues = function(){
                queues_promise = TimeoutResources.GetQueues(undefined,{site:$scope.site,division_id:$scope.division_id});
                Modals.loading();
                // = TimeoutResources.GetEtcData();
                queues_promise.then(function(data){            
                    $scope.resources = TimeoutResources.GetAllResources();
                    $scope.flattened_queues = _.values($scope.resources.queues.data);
                    Modals.loaded();
                    $timeout(get_queues,15000);                    
                });             

            };
            get_queues();
            
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
