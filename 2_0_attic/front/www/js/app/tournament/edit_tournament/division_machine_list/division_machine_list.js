angular.module('app.tournament.edit_tournament.division_machine_list',['app.tournament.edit_tournament.division_machine_list.add_division_machine',
    'app.tournament.edit_tournament.division_machine_list.upload_pic',
    /*REPLACEMECHILD*/]);
angular.module('app.tournament.edit_tournament.division_machine_list').controller(
    'app.tournament.edit_tournament.division_machine_list',[
        '$scope','$state','TimeoutResources','Utils','Modals','ActionSheets',
        function($scope, $state, TimeoutResources, Utils,Modals,ActionSheets) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
            $scope.choose_machine_action=ActionSheets.choose_machine_action;
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
             
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        division_machines_p = TimeoutResources.GetDivisionMachines($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id});
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
    }]
);
