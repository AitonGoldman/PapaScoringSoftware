angular.module('app.results.players',['app.results.players.player',
    /*REPLACEMECHILD*/]);
angular.module('app.results.players').controller(
    'app.results.players',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                

        players_promise = TimeoutResources.GetPlayers(undefined,{site:$scope.site});
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        players_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            $scope.flat_players = _.values($scope.resources.players.data);
            Modals.loaded();
        });
        
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
