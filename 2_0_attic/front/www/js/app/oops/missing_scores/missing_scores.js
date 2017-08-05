angular.module('app.oops.missing_scores',['app.oops.missing_scores.report_player_events',
    /*REPLACEMECHILD*/]);
angular.module('app.oops.missing_scores').controller(
    'app.oops.missing_scores',[
        '$scope','$state','TimeoutResources','Utils','Modals','$animate','$filter',
        function($scope, $state, TimeoutResources, Utils,Modals,$animate,$filter) {
        $scope.site=$state.params.site;

            $scope.utils = Utils;
            Modals.loading();
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
            $animate.enabled(false);
            
            $scope.test_submit = function(){
                if($scope.selected_players.length != 0){
                    console.log($scope.selected_players[0]);
                    $state.go('.report_player_events',{player_id:$scope.selected_players[0].player_id});
                }
            };
            $scope.keyDown = function(event){
                if(event.keyCode == 9 || event.keyCode==13){
                    //$state.go('.report_player_events',{player_id:$scope.selected_players[0].player_id});
                }
                //keyCode 9               
            };
            $scope.player = {};
            players_promise = TimeoutResources.GetPlayers(undefined,{site:$scope.site});                        
            players_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                $scope.flattened_players = _.values($scope.resources.players.data);
                $animate.enabled(true);                
                Modals.loaded();
            });
            $scope.selected_players=[];
            $scope.onPlayerIdChange = function(){                
                $scope.poop = true;
                $scope.selected_players = $filter('filter')($scope.flattened_players,{player_id:parseInt($scope.player.player_id)},true);
                if($scope.selected_players!=undefined && $scope.selected_players.length!=0){
                    $scope.player_img_id=$scope.selected_players[0].player_id;
                }                
            };                          
    }]
);
