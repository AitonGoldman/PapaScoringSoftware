angular.module('app.tournament.division_list.edit_division.division_machine_list',['app.tournament.division_list.edit_division.division_machine_list.add_division_machine',
    /*REPLACEMECHILD*/]);
angular.module('app.tournament.division_list.edit_division.division_machine_list').controller(
    'app.tournament.division_list.edit_division.division_machine_list',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
	$scope.tournament_id=$state.params.tournament_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                

        Modals.loading();
        // = TimeoutResources.GetEtcData();
        division_machines_p = TimeoutResources.GetDivisionMachines(undefined,{site:$scope.site,division_id:$scope.division_id});
        division_machines_p.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });
        $scope.remove_machine = function(machine){
            Modals.loading();
            // = TimeoutResources.GetEtcData();
            division_delete_machine_p = TimeoutResources.DeleteDivisionMachine(undefined,{site:$scope.site,division_id:$scope.division_id,division_machine_id:machine.division_machine_id});
            division_delete_machine_p.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                machine.removed=true;
                Modals.loaded();
            });            
        };
        
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
