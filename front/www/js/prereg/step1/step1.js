angular.module('prereg.step1',['prereg.step1.step2',
    /*REPLACEMECHILD*/]);
angular.module('prereg.step1').controller(
    'prereg.step1',[
        '$scope','$state','TimeoutResources','Utils','Modals',
        function($scope, $state, TimeoutResources, Utils,Modals) {
            $scope.site=$state.params.site;
            $scope.player_info = {};
            $scope.utils = Utils;
            //$scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
            
            //Modals.loading();
            // = TimeoutResources.GetEtcData();
            //.then(function(data){
            // $scope.resources = TimeoutResources.GetAllResources();
            //  Modals.loaded();
            //})
        }]
);
