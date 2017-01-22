angular.module('app.results.players.player',[/*REPLACEMECHILD*/]);
angular.module('app.results.players.player').controller(
    'app.results.players.player',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.player_id=$state.params.player_id;
	$scope.player_name=$state.params.player_name;

        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        results_promise = TimeoutResources.GetPlayerResults($scope.bootstrap_promise,{site:$scope.site,player_id:$scope.player_id});
        results_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });
    }]
);
