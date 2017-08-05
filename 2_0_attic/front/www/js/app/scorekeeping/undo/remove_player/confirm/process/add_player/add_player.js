angular.module('app.scorekeeping.undo.remove_player.confirm.process.add_player',['app.scorekeeping.undo.remove_player.confirm.process.add_player.confirm',
    'app.scorekeeping.undo.remove_player.confirm.process.add_player.process',
    /*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.undo.remove_player.confirm.process.add_player').controller(
    'app.scorekeeping.undo.remove_player.confirm.process.add_player',[
        '$scope','$state','TimeoutResources','Utils','Modals','$filter',
        function($scope, $state, TimeoutResources, Utils,Modals,$filter) {
        $scope.site=$state.params.site;
	$scope.division_machine_name=$state.params.division_machine_name;
	$scope.division_machine_id=$state.params.division_machine_id;
	$scope.division_id=$state.params.division_id;
	$scope.player_name=$state.params.player_name;
	$scope.player_id=$state.params.player_id;
            $scope.player={};
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        players_promise = TimeoutResources.GetPlayersWithTicketsForDivision($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id});
        players_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();            
            $scope.flattened_players = _.values($scope.resources.players_with_tickets.data);
        });
        $scope.onPlayerIdChange = function(){                
            $scope.poop = true;
            $scope.selected_players = $filter('filter')($scope.flattened_players,{player_id:parseInt($scope.player.player_id)},true);
            if($scope.selected_players!=undefined && $scope.selected_players.length!=0){
                if($scope.selected_players[0].has_tokens != true){
                    $scope.player_img_id=0;                        
                } else {
                    if($scope.selected_players[0].on_division_machine == true){
                        $scope.player_img_id="00";                            
                    } else {
                        $scope.player_img_id=$scope.selected_players[0].player_id;
                    }
                    console.log($scope.selected_players[0]);
                    
                }                    
            }                
        };
        
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
