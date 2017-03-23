angular.module('app.prereg_complete.confirm',['app.prereg_complete.confirm.process',
    'app.prereg_complete.confirm.picture',
    /*REPLACEMECHILD*/]);
angular.module('app.prereg_complete.confirm').controller(
    'app.prereg_complete.confirm',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.player_id=$state.params.player_id;
	$scope.player_name=$state.params.player_name;
        $scope.player_has_pic = $state.params.player_has_pic;
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
