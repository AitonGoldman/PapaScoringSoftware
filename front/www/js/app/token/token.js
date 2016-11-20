angular.module('app.token',[/*REPLACEMECHILD*/]);
angular.module('app.token').controller(
    'app.token',[
        '$scope','$state','TimeoutResources','Utils','Modals','$filter','$animate',
        function($scope, $state, TimeoutResources, Utils,Modals,$filter,$animate) {
            $animate.enabled(false);
            $scope.test_submit = function(){
                alert("hi there");
            };
            $scope.keyDown = function(event){
                //keyCode 9               
            };
            $scope.site=$state.params.site;
            
            $scope.player = {};
            $scope.utils = Utils;
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
            players_promise = TimeoutResources.GetPlayers(undefined,{site:$scope.site});
            Modals.loading();
            // = TimeoutResources.GetEtcData();
            players_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                $scope.flattened_players = _.values($scope.resources.players.data);                                              $animate.enabled(true);                              
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
        }
    ]
);
