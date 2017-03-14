angular.module('app.scorekeeping.undo',['app.scorekeeping.undo.remove_player',
    'app.scorekeeping.undo.undo_bump_player',
    /*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.undo').controller(
    'app.scorekeeping.undo',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;

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
