angular.module('app.ppo_qualifying_list.papa_qualifiers.confirm',[/*REPLACEMECHILD*/]);
angular.module('app.ppo_qualifying_list.papa_qualifiers.confirm').controller(
    'app.ppo_qualifying_list.papa_qualifiers.confirm',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
        $scope.qualifiers = $state.params.qualifiers;
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        $scope.resources = TimeoutResources.GetAllResources();     
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
