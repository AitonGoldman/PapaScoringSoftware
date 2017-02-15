angular.module('app.scorekeeping.machine_select',['app.scorekeeping.machine_select.player_select',
    'app.scorekeeping.machine_select.record_score',
    'app.scorekeeping.machine_select.team_select',
    /*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.machine_select').controller(
    'app.scorekeeping.machine_select',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
	$scope.hide_back_button=$state.params.hide_back_button;

        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        division_machines_promise = TimeoutResources.GetDivisionMachines($scope.bootstrap_promise,
                                                                         {site:$scope.site,division_id:$scope.division_id});        
        division_machines_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            $scope.flattened_division_machines = _.values($scope.resources.division_machines.data);
            console.log($scope.flattened_division_machines);
            $scope.flattened_division_machines.sort(function (a, b) {
                //return (a.division_machine_id > b.division_machine_id ? 1 : -1);
                return (a.division_machine_name > b.division_machine_name ? 1 : -1);
            });            
            Modals.loaded();
        });
        $scope.goto_next_scorekeeping_step = function(division_machine_id){
            Modals.loading();
            division_machines_promise = TimeoutResources.GetDivisionMachines(undefined,
                                                                             {site:$scope.site,division_id:$scope.division_id});        
            division_machines_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();                
                division_machine = $scope.resources.division_machines.data[division_machine_id];                
                if(division_machine.team_tournament == false){
                    if(division_machine.player_id != undefined){
                        $state.go('.record_score',
                                  {division_machine_id:division_machine.division_machine_id,
                                   division_machine_name:division_machine.division_machine_name,
                                   player_name:division_machine.player.player_name,
                                   player_id:division_machine.player.player_id,
                                   team_tournament:false});
                    } else {
                        $state.go('.player_select',
                                  {division_machine_id:division_machine.division_machine_id,
                                   division_machine_name:division_machine.division_machine_name});                        
                    }
                } else {
                    if(division_machine.team_id != undefined){                    
                        $state.go('.team_select',
                                  {division_machine_id:division_machine.division_machine_id,
                                   division_machine_name:division_machine.division_machine_name,
                                   player_name:division_machine.team.team_name,
                                   player_id:division_machine.team.team_id,
                                   team_tournament:true});
                        
                    } else {
                        $state.go('.team_select',
                                  {division_machine_id:division_machine.division_machine_id,
                                   division_machine_name:division_machine.division_machine_name});
                    }
                }
            });
        };
    }]
);
