angular.module('app.player',['app.player.add_player',
    'app.player.edit_player',
    /*REPLACEMECHILD*/]);
angular.module('app.player').controller(
    'app.player',[
        '$scope','$state','TimeoutResources','Utils','Modals','ActionSheets',
        function($scope, $state, TimeoutResources, Utils, Modals, ActionSheets) {
        $scope.site=$state.params.site;
            $scope.ActionSheets = ActionSheets;    
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        players_promise = TimeoutResources.GetPlayers(undefined,{site:$scope.site});
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        players_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            $scope.flat_players = _.values($scope.resources.players.data);
            Modals.loaded();
        });
    }]
);
