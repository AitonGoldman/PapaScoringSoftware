angular.module('app.queue_view',['app.queue_view.queue',
    /*REPLACEMECHILD*/]);
angular.module('app.queue_view').controller(
    'app.queue_view',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                      
        divisions_promise = TimeoutResources.GetDivisions(undefined,{site:$scope.site});        
        divisions_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });
    }]
);
