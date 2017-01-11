angular.module('app.queues.machine_select',['app.queues.machine_select.machine_queue',
    /*REPLACEMECHILD*/]);
angular.module('app.queues.machine_select').controller(
    'app.queues.machine_select',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);

        queues_promise = TimeoutResources.GetQueues($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id});
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        queues_promise.then(function(data){
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
