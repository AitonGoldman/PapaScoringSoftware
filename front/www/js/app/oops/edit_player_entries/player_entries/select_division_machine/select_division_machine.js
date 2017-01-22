angular.module('app.oops.edit_player_entries.player_entries.select_division_machine',[/*REPLACEMECHILD*/]);
angular.module('app.oops.edit_player_entries.player_entries.select_division_machine').controller(
    'app.oops.edit_player_entries.player_entries.select_division_machine',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.player_id=$state.params.player_id;

        $scope.utils = Utils;
        Modals.loading();        
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                

        machines_p = TimeoutResources.GetAllDivisionMachines($scope.bootstrap_promise,{site:$scope.site});
        // = TimeoutResources.GetEtcData();
        machines_p.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            $scope.machines = _.values($scope.resources.all_division_machines.data);
            console.log($scope.machines);
            Modals.loaded();
        });

        $scope.division_machine = {division_machine_name:""};        
        $scope.update_machine_list=function(){                            
            if($scope.division_machine.division_machine_name.length > 3){                
                $scope.matches = [];
                _.forEach($scope.machines,function(value){                                
                    if(value.division_machine_name.toLowerCase().match("(.*"+$scope.division_machine.division_machine_name.toLowerCase()+".*)")!=null){
                        $scope.matches.push(value);
                    }                
                });
            } else {
                $scope.matches = [];
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
