angular.module('app.queues',['app.queues.machine_select',
    /*REPLACEMECHILD*/]);
angular.module('app.queues').controller(
    'app.queues',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        $scope.bootstrap_promise.then(function(data){        
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });             
    }]
);
