angular.module('app.queues.machine_select.machine_queue.player_select',['app.queues.machine_select.machine_queue.player_select.confirm',
    /*REPLACEMECHILD*/]);
angular.module('app.queues.machine_select.machine_queue.player_select').controller(
    'app.queues.machine_select.machine_queue.player_select',[
        '$scope','$state','TimeoutResources','Utils','Modals','$animate','$filter',
        function($scope, $state, TimeoutResources, Utils,Modals,$animate,$filter) {
        $scope.site=$state.params.site;
	$scope.division_machine_id=$state.params.division_machine_id;
	$scope.division_id=$state.params.division_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                

        $scope.player = {};

        $scope.test_submit = function(){
            if($scope.selected_players.length != 0){
                console.log($scope.selected_players[0]);
                //$state.go('.confirm',{player_id:$scope.selected_players[0].player_id,player_name:$scope.selected_players[0].first_name+" "+$scope.selected_players[0].last_name});
                $state.go('.confirm',{player_id:$scope.selected_players[0].player_id,player_name:$scope.selected_players[0].first_name+" "+$scope.selected_players[0].last_name});
                
            }
        };
        $scope.keyDown = function(event){
            if(event.keyCode == 9 || event.keyCode==13){
                //$state.go('.confirm',{player_id:$scope.selected_players[0].player_id,player_name:$scope.selected_players[0].first_name+" "+$scope.selected_players[0].last_name});
            }
            //keyCode 9               
        };
        //players_promise = TimeoutResources.GetPlayers(undefined,{site:$scope.site});
            players_promise = TimeoutResources.GetPlayersWithTicketsForDivision($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id});

            Modals.loading();
        // = TimeoutResources.GetEtcData();
        players_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            $scope.flattened_players = _.values($scope.resources.players_with_tickets.data);
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
        
        
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
