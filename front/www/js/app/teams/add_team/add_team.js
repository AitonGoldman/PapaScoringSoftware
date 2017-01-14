angular.module('app.teams.add_team',['app.teams.add_team.process',
    /*REPLACEMECHILD*/]);
angular.module('app.teams.add_team').controller(
    'app.teams.add_team',[
        '$scope','$state','TimeoutResources','Utils','Modals','$animate','$filter',
        function($scope, $state, TimeoutResources, Utils,Modals,$animate,$filter) {
            $scope.site=$state.params.site;

            $scope.utils = Utils;

            $animate.enabled(false);
            $scope.test_submit = function(){
                //if($scope.selected_players1.length != 0 && $scope.selected_players2.length != 0){
                if($scope.selected_players[0].length != 0 && $scope.selected_players[1].length != 0){
                    // $state.go('.process',{process_step:{process:true},
                    //                       team_info:{player_one_id:$scope.selected_players[0][0].player_id,
                    //                                  player_one_name:$scope.selected_players[0][0].first_name+" "+$scope.selected_players[0][0].last_name,
                    //                                  player_two_id:$scope.selected_players[1][0].player_id,
                    //                                  player_two_name:$scope.selected_players[1][0].first_name+" "+$scope.selected_players[1][0].last_name
                    //                                 }
                    //                      });
                }
            };
            $scope.keyDown = function(event){
                if(event.keyCode == 9 || event.keyCode==13){
                    $state.go('.process',{process_step:{process:true},
                                          team_info:{player_one_id:$scope.selected_players[0][0].player_id,
                                                     player_one_name:$scope.selected_players[0][0].first_name+" "+$scope.selected_players[0][0].last_name,
                                                     player_two_id:$scope.selected_players[1][0].player_id,
                                                     player_two_name:$scope.selected_players[1][0].first_name+" "+$scope.selected_players[1][0].last_name
                                                    }
                                         });
                    
                    //$state.go('.process',{team_info:{player_one_id:$scope.selected_players[0][0].player_id,player_two_id:$scope.selected_players[1][0].player_id}});
                }
                //keyCode 9               
            };
            $scope.player = {};
            $scope.player_2 = {};
            $scope.team_players = [{},{}];
            $scope.utils = Utils;
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
            players_promise = TimeoutResources.GetPlayers($scope.bootstrap_promise,{site:$scope.site});
            Modals.loading();
            // = TimeoutResources.GetEtcData();
            players_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                $scope.flattened_players = _.values($scope.resources.players.data);                                              $animate.enabled(true);                              
                Modals.loaded();
            });
            //$scope.selected_players1=[];
            //$scope.selected_players2=[];
            $scope.selected_players=[[],[]];
            $scope.onPlayerIdChange = function(player_index){                                
                $scope.poop = true;
                // $scope.selected_players1 = $filter('filter')($scope.flattened_players,{player_id:parseInt($scope.player.player_id)},true);
                // if($scope.selected_players1!=undefined && $scope.selected_players1.length!=0){
                //     $scope.player1_img_id=$scope.selected_players1[0].player_id;
                // }
                $scope.selected_players[player_index] = $filter('filter')($scope.flattened_players,{player_id:parseInt($scope.team_players[player_index].player_id)},true);
                console.log($scope.selected_players);
                if($scope.selected_players[player_index]!=undefined && $scope.selected_players[player_index].length!=0){
                    //$scope.player1_img_id=$scope.selected_players1[0].player_id;
                    $scope.team_players[player_index].player_img_id=$scope.selected_players[player_index][0].player_id;
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
