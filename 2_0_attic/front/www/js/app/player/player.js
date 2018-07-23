angular.module('app.player',['app.player.add_player',
    'app.player.edit_player',
    'app.player.player_info',
    /*REPLACEMECHILD*/]);
angular.module('app.player').controller(
    'app.player',[
        '$scope','$state','TimeoutResources','Utils','Modals','ActionSheets',
        function($scope, $state, TimeoutResources, Utils, Modals, ActionSheets) {
            $scope.site=$state.params.site;
            $scope.ActionSheets = ActionSheets;    
            $scope.utils = Utils;
            Modals.loading();
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
            players_promise = TimeoutResources.GetPlayersFast($scope.bootstrap_promise,{site:$scope.site});
            if($state.current.name == 'app.in_line_player'){
                $scope.in_line_manage = true;
            } else {
                $scope.in_line_manage = false;
            }
            // = TimeoutResources.GetEtcData();
            players_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                $scope.flat_players = _.values($scope.resources.players.data);
                Modals.loaded();
        });
    }]
);
