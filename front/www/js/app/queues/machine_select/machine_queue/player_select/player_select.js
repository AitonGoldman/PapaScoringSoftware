angular.module('app.queues.machine_select.machine_queue.player_select',['app.queues.machine_select.machine_queue.player_select.confirm',
    /*REPLACEMECHILD*/]);
angular.module('app.queues.machine_select.machine_queue.player_select').controller(
    'app.queues.machine_select.machine_queue.player_select',[
        '$scope','$state','TimeoutResources','Utils','Modals','$animate','$filter','$ImageCacheFactory',
        function($scope, $state, TimeoutResources, Utils,Modals,$animate,$filter,$ImageCacheFactory) {
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
            //Modals.loaded();
                image_cache_list = [];
                for(x=0;x<$scope.flattened_players.length;x++){
                    if($scope.flattened_players[x].has_tokens == true){
                        image_cache_list[x]=$scope.http_prefix+"://"+$scope.server_ip_address+"/pics/player_"+$scope.flattened_players[x].player_id+".jpg";
                    }
                }
                //Modals.loaded();
                $ImageCacheFactory.Cache(
                     image_cache_list
                 ).then(function(){
                     console.log("Images done loading!");
                     Modals.loaded();
                 },function(failed){
                     console.log("An image failed: "+failed);
                     Modals.loaded();
                });                                                
            
        });
        $scope.selected_players=[];
        $scope.onPlayerIdChange = function(){                
            $scope.poop = true;
            $scope.selected_players = $filter('filter')($scope.flattened_players,{player_id:parseInt($scope.player.player_id)},true);
            if($scope.selected_players!=undefined && $scope.selected_players.length!=0){
                    if($scope.selected_players[0].has_tokens != true){
                        $scope.player_img_id=0;                        
                    } else {
                        $scope.player_img_id=$scope.selected_players[0].player_id;
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
