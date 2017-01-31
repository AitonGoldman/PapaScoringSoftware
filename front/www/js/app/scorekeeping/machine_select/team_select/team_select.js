angular.module('app.scorekeeping.machine_select.team_select',['app.scorekeeping.machine_select.team_select.process',
    /*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.machine_select.team_select').controller(
    'app.scorekeeping.machine_select.team_select',[
        '$scope','$state','TimeoutResources','Utils','Modals','$filter','$animate',
        function($scope, $state, TimeoutResources, Utils,Modals,$filter,$animate) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                

	    $scope.division_machine_id=$state.params.division_machine_id;
            $scope.player={player_id:""};            
            $scope.queue_player={player_id:""};            
            $scope.division_machine_name=$state.params.division_machine_name;

            $scope.utils = Utils;
            $scope.queues = [];
            Modals.loading();
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                            
            players_promise = TimeoutResources.GetPlayersWithTicketsForDivision($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id});
            //players_promise = TimeoutResources.GetPlayers($scope.bootstrap_promise,{site:$scope.site});
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
            $scope.keyDown = function(event){
                if(event.keyCode == 9 || event.keyCode==13){                    
                    //$state.go('.process',{process_step:{process:true},team_info:$scope.selected_players[0].teams[0],from_queue:0});
                }                
            };
            
            $scope.poop_2 = true;
            $scope.test_submit_new = function(){
                if($scope.selected_players.length != 0){                    
                    $state.go('.process',{process_step:{process:true},team_info:$scope.selected_players[0].teams[0]});

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
