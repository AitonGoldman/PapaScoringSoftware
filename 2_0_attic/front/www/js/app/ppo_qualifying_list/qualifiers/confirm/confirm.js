angular.module('app.ppo_qualifying_list.qualifiers.confirm',[/*REPLACEMECHILD*/]);
angular.module('app.ppo_qualifying_list.qualifiers.confirm').controller(
    'app.ppo_qualifying_list.qualifiers.confirm',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
        $scope.a_qualifiers=$state.params.a_qualifiers;
        $scope.b_qualifiers=$state.params.b_qualifiers;        
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
             
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
