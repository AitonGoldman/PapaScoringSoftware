angular.module('app.queue_view',['app.queue_view.queue',
    /*REPLACEMECHILD*/]);
angular.module('app.queue_view').controller(
    'app.queue_view',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
        $scope.selected_machines={};
        $scope.columns_obj = {columns:undefined};
        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                      
        divisions_promise = TimeoutResources.GetAllDivisionMachines(undefined,{site:$scope.site,});        
        divisions_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            $scope.division_machines = {};
            queuing_divisions = _.filter($scope.resources.divisions.data, function(o) { return o.queuing; });
            _.forEach(queuing_divisions, function(value, key) {
                $scope.division_machines[value.division_id]=_.filter($scope.resources.all_division_machines.data, function(o) { return o.division_id == value.division_id; });
            });
            $scope.go_to_queue = function(division_id){
                flattened_machines = _.toPairs($scope.selected_machines);
                filtered_machines = _.filter(flattened_machines, function(o) { return o[1] == true; });                
                machine_info = {division_id:division_id,columns:$scope.columns_obj.columns};
                machine_fields = ['game_1','game_2','game_3','game_4','game_5','game_6','game_7','game_8','game_9','game_10','game_11','game_12'];
                _.forEach(machine_fields, function(value,key) {                    
                    idx = parseInt(key);
                    if (filtered_machines[idx]){
                        machine_info[value]=filtered_machines[idx][0];
                    }                    
                });                               
                $state.go('.queue',machine_info);
            };
            Modals.loaded();
        });
    }]
);
