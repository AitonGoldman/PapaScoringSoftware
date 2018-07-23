angular.module('app.remove_player.confirm',['app.remove_player.confirm.process',
    /*REPLACEMECHILD*/]);
angular.module('app.remove_player.confirm').controller(
    'app.remove_player.confirm',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.player_id=$state.params.player_id;
	$scope.player_name=$state.params.player_name;
	$scope.machine_name=$state.params.machine_name;

        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        $scope.bootstrap_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });
    }]
);
