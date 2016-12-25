angular.module('app.jagoffs',[/*REPLACEMECHILD*/]);
angular.module('app.jagoffs').controller(
    'app.jagoffs',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        jagoffs_promise = TimeoutResources.GetJagoffs(undefined,{site:$scope.site});        
             
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        jagoffs_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });             
    }]
);
