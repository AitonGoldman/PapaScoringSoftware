angular.module('app.scorekeeping.machine_select.add_player_to_queue',['app.scorekeeping.machine_select.add_player_to_queue.confirm',
    /*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.machine_select.add_player_to_queue').controller(
    'app.scorekeeping.machine_select.add_player_to_queue',[
        '$scope','$state','TimeoutResources','Utils','Modals','$animate','$filter',
        function($scope, $state, TimeoutResources, Utils,Modals,$animate,$filter) {
        $scope.site=$state.params.site;
	    $scope.division_machine_id=$state.params.division_machine_id;
	    $scope.division_machine_name=$state.params.division_machine_name;
            $scope.player_status = "";                        
            
	$scope.division_id=$state.params.division_id;
        $scope.player = {};

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        $scope.test_submit = function(){
            if($scope.selected_players.length != 0){
                console.log($scope.selected_players[0]);
                //$state.go('.confirm',{player_id:$scope.selected_players[0].player_id,player_name:$scope.selected_players[0].first_name+" "+$scope.selected_players[0].last_name});
                $state.go('.confirm',{player_id:$scope.selected_players[0].player_id,player_name:$scope.selected_players[0].first_name+" "+$scope.selected_players[0].last_name});
                
            }
        };

        players_promise = TimeoutResources.GetPlayersWithTicketsForDivision($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id});

        Modals.loading();        
        players_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            $scope.flattened_players = _.values($scope.resources.players_with_tickets.data);
            $animate.enabled(true);
            _.forEach($scope.flattened_players, function(value) {
                if(value.has_tokens == true){
                    ImgCache.isCached(http_prefix+"://"+server_ip_address+"/pics/player_"+value.player_id+'.jpg',function(path,success){
                        if(!success){
                            ImgCache.cacheFile(http_prefix+"://"+server_ip_address+"/pics/player_"+value.player_id+'.jpg');
                        }                        
                    });
                }                   
            });
            
            //Modals.loaded();
            //image_cache_list = [];
            // for(x=0;x<$scope.flattened_players.length;x++){
            //     if($scope.flattened_players[x].has_tokens == true){
            //         image_cache_list[x]=$scope.http_prefix+"://"+$scope.server_ip_address+"/pics/player_"+$scope.flattened_players[x].player_id+".jpg";
            //     }
            // }
            Modals.loaded();            
        });
            $scope.selected_players=[];
            $scope.disable_review_button = function(){
                if ($scope.selected_players.length == 0){
                    return true;
                }
                if ($scope.selected_players[0].has_tokens != true){
                    return true;
                }                
                return false;
            };
        $scope.onPlayerIdChange = function(){                
            $scope.player_status = "";                        
            $scope.poop = true;
            $scope.selected_players = $filter('filter')($scope.flattened_players,{player_id:parseInt($scope.player.player_id)},true);
            console.log($scope.selected_players);
            if($scope.selected_players!=undefined && $scope.selected_players.length!=0){
                if($scope.selected_players[0].has_tokens != true){
                    $scope.player_img_id=0;
                    $scope.player_status = "No Tickets In Division";                                                
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
