angular.module('app.finals',['app.finals.manage',
    /*REPLACEMECHILD*/]);
angular.module('app.finals').controller(
    'app.finals',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
             
        
        // = TimeoutResources.GetEtcData();
        $scope.bootstrap_promise.then(function(data){
         $scope.resources = TimeoutResources.GetAllResources();
          Modals.loaded();
        });
    }]
);
