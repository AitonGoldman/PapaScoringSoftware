angular.module('app.tournament.edit_tournament.division_machine_list.add_division_machine',[/*REPLACEMECHILD*/]);
angular.module('app.tournament.edit_tournament.division_machine_list.add_division_machine').controller(
    'app.tournament.edit_tournament.division_machine_list.add_division_machine',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
             
        Modals.loading();
        machines_p = TimeoutResources.GetMachines($scope.bootstrap_promise,{site:$scope.site});
        // = TimeoutResources.GetEtcData();
        machines_p.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            $scope.machines = _.values($scope.resources.machines.data);
            Modals.loaded();
        });
        $scope.add_division_machine = function(machine){
            Modals.loading();
            add_machine_p = TimeoutResources.AddDivisionMachine(undefined,{site:$scope.site,division_id:$scope.division_id},{machine_id:machine.machine_id});
            // = TimeoutResources.GetEtcData();
            add_machine_p.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();                
                $state.go('.^');
                Modals.loaded();
            });            
        };
        $scope.division_machine = {division_machine_name:""};        
        $scope.update_machine_list=function(){                
            console.log($scope.division_machine.division_machine_name);
            if($scope.division_machine.division_machine_name.length > 3){                
                $scope.matches = [];
                _.forEach($scope.machines,function(value){                                
                    if(value.machine_name.toLowerCase().match("(.*"+$scope.division_machine.division_machine_name.toLowerCase()+".*)")!=null){
                        $scope.matches.push(value);
                    }                
                });
            } else {
                $scope.matches = [];
            }            
        };
        
    }]
);
