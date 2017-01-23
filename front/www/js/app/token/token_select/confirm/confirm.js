angular.module('app.token.token_select.confirm',['app.token.token_select.confirm.process',
    /*REPLACEMECHILD*/]);
angular.module('app.token.token_select.confirm').controller(
    'app.token.token_select.confirm',[
        '$scope','$state','TimeoutResources','Utils','Modals','User',
        function($scope, $state, TimeoutResources, Utils,Modals,User) {
            $scope.site=$state.params.site;
            $scope.player_id=$state.params.player_id;
            
            $scope.utils = Utils;
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
            $scope.token_info = $state.params.token_info;
            Modals.loading();
            // = TimeoutResources.GetEtcData();
            $scope.bootstrap_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                Modals.loaded();
            });
            $scope.create_tickets = function(){
                $scope.added_tokens = {};
                $scope.added_tokens['divisions']=$scope.token_info.divisions;
                $scope.added_tokens['metadivisions']=$scope.token_info.metadivisions;
                $scope.added_tokens['teams']=$scope.token_info.teams;
                $scope.added_tokens['comped']=$scope.token_info.comped;
                //$scope.added_tokens['player_id']=User.logged_in_user().player.player_id;
                $scope.added_tokens['player_id']=$scope.player_id;
                $state.go('.process',{process_step:{process:true},
                                      token_info:$scope.added_tokens,
                                      total_cost:$scope.token_info.total_cost
                                     });                    
            };
    }]
);
