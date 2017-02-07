angular.module('app.scorekeeping.machine_select.player_select',['app.scorekeeping.machine_select.player_select.process',
    /*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.machine_select.player_select').controller(
    'app.scorekeeping.machine_select.player_select',[
        '$scope','$state','TimeoutResources','Utils','Modals','$animate','$filter','$timeout','$ImageCacheFactory',
        function($scope, $state, TimeoutResources, Utils,Modals,$animate,$filter,$timeout,$ImageCacheFactory) {
            $animate.enabled(false);                                          

            $scope.site=$state.params.site;
	    $scope.division_id=$state.params.division_id;
	    $scope.division_machine_id=$state.params.division_machine_id;
            $scope.player={player_id:""};            
            $scope.queue_player={player_id:""};            
            $scope.division_machine_name=$state.params.division_machine_name;
            $scope.player_id = $state.params.player_id;
            $scope.player_name = $state.params.player_name;
	    $scope.hide_back_button=$state.params.hide_back_button;

            $scope.utils = Utils;
            $scope.queues = [];
            Modals.loading();
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
            
            $scope.selected_players=[];
            //players_promise = TimeoutResources.GetPlayers($scope.bootstrap_promise,{site:$scope.site});
            players_promise = TimeoutResources.GetPlayersWithTicketsForDivision($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id});
            queues_promise = TimeoutResources.GetQueues(players_promise,{site:$scope.site,division_id:$scope.division_id});
            queues_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();            
                $scope.queues = $scope.resources.queues.data[$scope.division_machine_id].queues;
                if($scope.queues.length > 0){
                    $scope.queue_player.player_id=$scope.queues[0].player.player_id;
                    $scope.poop = true;
                    $scope.selected_players = [$scope.queue_player];
                    $scope.player_img_id = $scope.queue_player.player_id;
                }                
                $scope.flattened_players = _.values($scope.resources.players_with_tickets.data);
                $animate.enabled(true);
                image_cache_list = [];
                for(x=0;x<$scope.flattened_players.length;x++){
                    image_cache_list[x]=$scope.http_prefix+"://"+$scope.server_ip_address+"/pics/player_"+$scope.flattened_players[x].player_id+".jpg";
                }
                Modals.loaded();
                // $ImageCacheFactory.Cache(
                //     image_cache_list
                // ).then(function(){
                //     console.log("Images done loading!");
                //     Modals.loaded();
                // },function(failed){
                //     console.log("An image failed: "+failed);
                //     Modals.loaded();
                // });                                                
            });
            
        
            $scope.onPlayerIdChange = function(){                
                $scope.poop = true;
                $scope.selected_players = $filter('filter')($scope.flattened_players,{player_id:parseInt($scope.player.player_id)},true);
                if($scope.selected_players!=undefined && $scope.selected_players.length!=0){
                    $scope.player_img_id=$scope.selected_players[0].player_id;
                }                
            };
            $scope.keyDown = function(event){
                if(event.keyCode == 9 || event.keyCode==13){                    
                    //$state.go('.process',{process_step:{process:true},player_info:$scope.selected_players[0],from_queue:0});
                }                
            };
            
            $scope.poop_2 = true;
            $scope.testChange = function(){
                $scope.poop_2 = false;
                Modals.loading();
                $scope.selected_players = [];
                bump_queue_promise = TimeoutResources.BumpQueue(undefined,{site:$scope.site,division_machine_id:$scope.division_machine_id});                                         
                bump_queue_promise.then(function(data){                    
                    $scope.resources = TimeoutResources.GetAllResources();                                        
                    for(i in $scope.resources.queues.data[$scope.division_machine_id].queues){                        
                        $scope.queues[i]=$scope.resources.queues.data[$scope.division_machine_id].queues[i];
                    }
                    if($scope.queues.length > $scope.resources.queues.data[$scope.division_machine_id].queues.length){
                        $scope.queues.pop();
                    }
                    if($scope.queues.length > 0){
                        $scope.queue_player.player_id=$scope.queues[0].player.player_id;
                        $scope.player_img_id = $scope.queue_player.player_id;
                        $scope.selected_players = [$scope.queue_player];
                        
                    }
                    $scope.poop_2 = true;                    
                    Modals.loaded();
            });
                
            };
            $scope.test_submit = function(){
                if($scope.selected_players.length != 0){
                    $state.go('.process',{process_step:{process:true},player_info:$scope.selected_players[0],from_queue:0});
                    //$state.go('.process',{process_step:{process:true},player_info:$scope.selected_players[0],from_queue:0});
                }
            };

    }]
);
