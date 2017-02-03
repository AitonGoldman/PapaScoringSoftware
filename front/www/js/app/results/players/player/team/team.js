angular.module('app.results.players.player.team',[/*REPLACEMECHILD*/]);
angular.module('app.results.players.player.team').controller(
    'app.results.players.player.team',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.player_name=$state.params.player_name;        
	$scope.player_id=$state.params.player_id;        
        $scope.team_id=$state.params.team_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        player_promise = TimeoutResources.GetFromResultsPlayer($scope.bootstrap_promise,{site:$scope.site,player_id:$scope.player_id});
        results_promise = TimeoutResources.GetTeamResults(player_promise,{site:$scope.site,team_id:$scope.team_id});
        results_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });
        $scope.doRefresh = function(){
            results_promise = TimeoutResources.GetTeamResults($scope.bootstrap_promise,{site:$scope.site,team_id:$scope.team_id});
            results_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                $scope.$broadcast('scroll.refreshComplete');
            });
        };
             
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
