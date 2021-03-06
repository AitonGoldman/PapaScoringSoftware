angular.module('app.scorekeeping.machine_select.record_score',['app.scorekeeping.machine_select.record_score.void',
    'app.scorekeeping.machine_select.record_score.confirm',
    'app.scorekeeping.machine_select.record_score.confirm_jagoff',
    /*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.machine_select.record_score').controller(
    'app.scorekeeping.machine_select.record_score',[
        '$scope','$state','TimeoutResources','Utils','Modals','ActionSheets',
        function($scope, $state, TimeoutResources, Utils,Modals,ActionSheets) {
            $scope.site=$state.params.site;
	    $scope.division_id=$state.params.division_id;
	    //$scope.team_tournament=$state.params.team_tournament;            
            $scope.division_machine_id=$state.params.division_machine_id;
            $scope.division_machine_name=$state.params.division_machine_name;
            $scope.player_id = $state.params.player_id;
            $scope.team_id = $state.params.team_id;
            
            $scope.player_name = $state.params.player_name;
            $scope.team_name = $state.params.team_name;
            
            $scope.choose_void_action = ActionSheets.choose_void_action;
            $scope.score={score:undefined};
            $scope.utils = Utils;
            Modals.loading();
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
            $scope.bootstrap_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                $scope.team_tournament=$scope.resources.divisions.data[$scope.division_id].team_tournament;            

                if($scope.team_tournament!=true){
                    best_score_promise = TimeoutResources.GetPlayerBestScoreForMachine($scope.bootstrap_promise,
                                                                                       {site:$scope.site,
                                                                                        player_id:$scope.player_id,
                                                                                        division_machine_id:$scope.division_machine_id});
                } else {
                    best_score_promise = TimeoutResources.GetTeamBestScoreForMachine($scope.bootstrap_promise,
                                                                                     {site:$scope.site,
                                                                                      team_id:$scope.team_id,
                                                                                      division_machine_id:$scope.division_machine_id});
                }
                best_score_promise.then(function(data){                
                    
                    $scope.resources = TimeoutResources.GetAllResources();
                    //$scope.team_tournament=$scope.resources.divisions.data[$scope.division_id].team_tournament;
                    Modals.loaded();
                });                
            });
            $scope.keyDown = function(event){
                if(event.keyCode == 9 || event.keyCode==13){                    
                    //$state.go('.confirm',{score:$scope.score.score});
                }                
            };

            $scope.test_submit = function(){                
                 $state.go('.confirm',{score:$scope.score.score});
            };
            $scope.onScoreChange = function(){
                $scope.score.score = $scope.score.score.replace(/\,/g,'').replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
            };
    }]
);
