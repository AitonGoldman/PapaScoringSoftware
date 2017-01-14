angular.module('app.player.player_info',[/*REPLACEMECHILD*/]);
angular.module('app.player.player_info').controller(
    'app.player.player_info',[
        '$scope','$state','TimeoutResources','Utils','Modals','User',
        function($scope, $state, TimeoutResources, Utils,Modals,User) {
        $scope.site=$state.params.site;
	$scope.player_id=$state.params.player_id;
            $scope.User = User;
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
            Modals.loading();
            player_queue_promise = TimeoutResources.GetPlayerQueue($scope.bootstrap_promise,{site:$scope.site,player_id:$scope.player_id});
            division_promise = TimeoutResources.GetDivisions(player_queue_promise,{site:$scope.site});
            player_promise = TimeoutResources.GetPlayer(division_promise,{site:$scope.site,player_id:$scope.player_id});
            player_tokens_promise = TimeoutResources.GetPlayerTokens(player_promise,{site:$scope.site,player_id:$scope.player_id});
        
            // = TimeoutResources.GetEtcData();
            player_tokens_promise.then(function(data){            
            if(User.logged_in_user().is_player == false){                        
                player_pin_promise = TimeoutResources.GetPlayerPin(undefined,{site:$scope.site,player_id:$scope.player_id});
                player_pin_promise.then(function(data){
                    $scope.resources = TimeoutResources.GetAllResources();
                    Modals.loaded();
                });
            } else {
                $scope.resources = TimeoutResources.GetAllResources();
                Modals.loaded();
            }
            
        });
    }]
);
