angular.module('app.results.division_machines.machines.machine',[/*REPLACEMECHILD*/]);
angular.module('app.results.division_machines.machines.machine').controller(
    'app.results.division_machines.machines.machine',[
        '$scope','$state','TimeoutResources','Utils','Modals','$ionicScrollDelegate',
        function($scope, $state, TimeoutResources, Utils,Modals,$ionicScrollDelegate) {
        $scope.site=$state.params.site;
        $scope.division_machine_id=$state.params.division_machine_id;
	$scope.division_machine_name=$state.params.division_machine_name;        
	$scope.division_id=$state.params.division_id;        
        $scope.jump_to_division_machine = {data:{division_machine_name:"Jump To Machine..."}};
        $scope.utils = Utils;        
        Modals.loading_no_spinner();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                                
        $scope.filter_limit=75;
        
        results_promise = TimeoutResources.GetDivisionMachineResults($scope.bootstrap_promise,
                                                                     {site:$scope.site,division_machine_id:$scope.division_machine_id});
        //division_machines_promise = TimeoutResources.GetDivisionMachines(results_promise,{site:$scope.site,division_id:$scope.division_id});        
        
        Modals.loading_no_spinner();        
        results_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            $scope.team_tournament = $scope.resources.divisions.data[$scope.division_id].team_tournament;
            //$scope.resources.division_machines.data["-1"]=$scope.jump_to_division_machine.data;
            console.log($scope.resources);
            Modals.loaded();            
        });
        $scope.doRefresh = function() {
            Modals.loading_no_spinner();            
        };
        $scope.doneRefresh = function() {
            results_promise = TimeoutResources.GetDivisionMachineResults(undefined,
                                                                         {site:$scope.site,division_machine_id:$scope.division_machine_id});            
            results_promise.then(function(data){                
                $scope.resources = TimeoutResources.GetAllResources();
                Modals.loaded();
                $scope.$broadcast('scroll.refreshComplete');                
            });
        };                        

        $scope.increase_display_window = function(){
            $scope.filter_limit=$scope.filter_limit+50;
            $ionicScrollDelegate.scrollBottom(true);
        };
        
        $scope.jump_to_machine_results = function(){                        
            if($scope.jump_to_division_machine.data == undefined || $scope.jump_to_division_machine.data.division_machine_id == undefined){
                return;
            }
            
            $state.go("^.machine",({division_machine_id:$scope.jump_to_division_machine.data.division_machine_id,division_machine_name:$scope.jump_to_division_machine.data.division_machine_name}));
        };
    }]
);
