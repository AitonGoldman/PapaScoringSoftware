angular.module('app.queues',['app.queues.machine_select',
    /*REPLACEMECHILD*/]);
angular.module('app.queues').controller(
    'app.queues',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        divisions_promise = TimeoutResources.GetDivisions(undefined,{site:$scope.site});        
             
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        divisions_promise.then(function(data){
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
