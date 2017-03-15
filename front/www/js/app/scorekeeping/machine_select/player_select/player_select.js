angular.module('app.scorekeeping.machine_select.player_select',['app.scorekeeping.machine_select.player_select.process',
    /*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.machine_select.player_select').controller(
    'app.scorekeeping.machine_select.player_select',[
        '$scope','$state','TimeoutResources','Utils','Modals','$animate','$filter','$timeout','$ImageCacheFactory',
        function($scope, $state, TimeoutResources, Utils,Modals,$animate,$filter,$timeout,$ImageCacheFactory) {
            $animate.enabled(false);                                          
            $scope.player_status = "N/A";                        

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
                $scope.team_tournament = $scope.resources.divisions.data[$scope.division_id].team_tournament;

                $scope.queues = $scope.resources.queues.data[$scope.division_machine_id].queues;
                if($scope.queues.length > 0){
                    $scope.queue_player.player_id=$scope.queues[0].player.player_id;
                    $scope.poop = true;
                    $scope.selected_players = [$scope.queue_player];
                    $scope.player_img_id = $scope.queue_player.player_id;
                }                
                $scope.flattened_players = _.values($scope.resources.players_with_tickets.data);
                $animate.enabled(true);
                _.forEach($scope.flattened_players, function(value) {                    
                    ImgCache.isCached(http_prefix+"://"+server_ip_address+"/pics/player_"+value.player_id+'.jpg',function(path,success){
                        if(!success){
                            ImgCache.cacheFile(http_prefix+"://"+server_ip_address+"/pics/player_"+value.player_id+'.jpg');
                        }                        
                    });
                });
                Modals.loaded();
            });
            
            $scope.find_queue_for_player = function(player_id,cur_division_machine_id){
                $scope.existing_player_queue_machine_name = undefined;
                _.forEach($scope.resources.queues.data, function(machine, machine_id) {                    
                    _.forEach(machine.queues, function(queue, idx) {                                                
                        if (queue.player_id == player_id && machine_id != cur_division_machine_id){
                            console.log(idx);
                            $scope.existing_player_queue_machine_name = queue.division_machine.division_machine_name;
                        } 
                    });                    
                });                
                
            };
            $scope.onPlayerIdChange = function(){                
                $scope.player_status = "";                        
                $scope.poop = true;
                $scope.selected_players = $filter('filter')($scope.flattened_players,{player_id:parseInt($scope.player.player_id)},true);
                if($scope.selected_players!=undefined && $scope.selected_players.length!=0){
                    if($scope.selected_players[0].has_tokens != true){
                        $scope.player_img_id=0;
                        if($scope.team_tournament != true ){
                            $scope.player_status = "No More Tickets";
                        } else {
                            if($scope.selected_players[0].team_id == "" || $scope.selected_players[0].team_id == undefined){
                                $scope.player_status = "Not on a team";                                
                            } else {
                                $scope.player_status = "No More Tickets";
                            }
                            //$scope.player_status = $scope.selected_players[0].team_id;
                        }
                        
                    } else {
                        if($scope.selected_players[0].on_division_machine == true){
                            $scope.player_img_id="00";
                            $scope.player_status = "Already On Machine";
                        } else {                            
                            $scope.find_queue_for_player($scope.selected_players[0].player_id,$scope.division_machine_id);
                            if($scope.team_tournament != true ){
                                $scope.player_status = "Player Has Tickets";
                            } else {
                                $scope.player_status = "Team Has Tickets";
                            }
                                
                                
                            $scope.player_img_id=$scope.selected_players[0].player_id;
                        }                                                
                    }                    
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
                    args = {process_step:{process:true},player_info:$scope.selected_players[0],from_queue:0};
                    if($scope.existing_player_queue_machine_name != undefined){
                        console.log('go');
                        args.existing_queue_machine= $scope.existing_player_queue_machine_name;
                    }                    
                    $state.go('.process',args);
                    //$state.go('.process',{process_step:{process:true},player_info:$scope.selected_players[0],from_queue:0});
                }
            };

    }]
);
