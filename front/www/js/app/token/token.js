angular.module('app.token',['app.token.token_select',
    /*REPLACEMECHILD*/]);
angular.module('app.token').controller(
    'app.token',[
        '$scope','$state','TimeoutResources','Utils','Modals','$filter','$animate',
        function($scope, $state, TimeoutResources, Utils,Modals,$filter,$animate) {
            $scope.state = $state.current.name;
            $animate.enabled(false);            
            $scope.hide_back_button=$state.params.hide_back_button;
            $scope.test_submit = function(){
                if($scope.selected_players.length != 0){
                    console.log($scope.selected_players[0]);                    
                    var route_string='.token_select';
                    if($scope.state == "app.token_comp"){
                        route_string='.token_select_comp';
                    }
                    $state.go(route_string,{player_id:$scope.selected_players[0].player_id});
                }
            };
            $scope.keyDown = function(event){
                if(event.keyCode == 9 || event.keyCode==13){
                    //$state.go('.token_select',{player_id:$scope.selected_players[0].player_id});
                }
                //keyCode 9               
            };
            $scope.site=$state.params.site;
            
            $scope.player = {};
            $scope.utils = Utils;
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                            
            Modals.loading();
            players_promise = TimeoutResources.GetPlayersFast($scope.bootstrap_promise,{site:$scope.site});            
            // = TimeoutResources.GetEtcData();
            players_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();                
                $scope.flattened_players = _.values($scope.resources.players.data);
                _.forEach($scope.flattened_players, function(value) {                    
                    ImgCache.isCached(http_prefix+"://"+server_ip_address+"/pics/player_"+value.player_id+'.jpg',function(path,success){
                        if(!success){
                            ImgCache.cacheFile(http_prefix+"://"+server_ip_address+"/pics/player_"+value.player_id+'.jpg');
                        }                        
                    });
                    
                    //img_prom = QImgCache.cacheFile('http://192.168.1.178/pics/player_'+value.player_id+'.jpg');
                    //img_prom.then(function(data){
                        
                    //});
                });

                //ImgCache.cacheFile('http://192.168.1.178/pics/player_125.jpg');
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
        }
    ]
);
