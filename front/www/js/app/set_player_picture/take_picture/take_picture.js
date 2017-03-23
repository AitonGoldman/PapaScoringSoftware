angular.module('app.set_player_picture.take_picture',['app.set_player_picture.take_picture.process',
    /*REPLACEMECHILD*/]);
angular.module('app.set_player_picture.take_picture').controller(
    'app.set_player_picture.take_picture',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.player_id=$state.params.player_id;
        $scope.player_info = {};
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        $scope.player_name = $state.params.player_name;
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
