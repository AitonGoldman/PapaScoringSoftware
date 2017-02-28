angular.module('app.cycling_machine_results_view',[/*REPLACEMECHILD*/]);
angular.module('app.cycling_machine_results_view').controller(
    'app.cycling_machine_results_view',[
        '$scope','$state','TimeoutResources','Utils','Modals','$timeout','$ionicScrollDelegate',
        function($scope, $state, TimeoutResources, Utils,Modals,$timeout,$ionicScrollDelegate) {
            $scope.site=$state.params.site;
            $scope.starting_division_machine_id=parseInt($state.params.starting_division_machine_id);
            $scope.division_id=$state.params.division_id;
            $scope.current_division_machine_idx = 0;
            $scope.current_division_machine_id = undefined;
            
            $scope.cur_num_results_displayed = 15;
            $scope.utils = Utils;
            
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);
            $scope.display_next_result = function(){
                console.log($scope.resources);
                $timeout(function(){                    
                    if($scope.resources.division_machine_results.data.length < $scope.cur_num_results_displayed){
                        $ionicScrollDelegate.scrollTo(0,0);                        
                        $scope.cur_num_results_displayed = 15;
                        $scope.current_division_machine_idx=$scope.current_division_machine_idx+1;
                        if($scope.current_division_machine_idx > $scope.num_machines_in_division-1){
                            $scope.current_division_machine_idx=0;
                        }
                        division_machine_key = _.keys($scope.resources.division_machines.data)[$scope.current_division_machine_idx];
                        $scope.current_division_machine_id=$scope.resources.division_machines.data[division_machine_key].division_machine_id;
                        console.log($scope.current_division_machine_id);
                        $scope.get_division_machine_results($scope.current_division_machine_id).then(function(data){
                            $scope.display_next_result();
                        });                        
                    } else {                        
                        $scope.cur_num_results_displayed = $scope.cur_num_results_displayed +10;                        
                        $ionicScrollDelegate.scrollBy(0,500,true);                        
                        $scope.display_next_result();                        
                    }
                }, 1000);
                
            };
            $scope.bootstrap_promise.then(function(data){
                $ionicScrollDelegate.getScrollView().options.animationDuration = 1000;
                TimeoutResources.GetDivisionMachines(undefined,{site:$scope.site,division_id:$scope.division_id}).then(function(data){
                    $scope.resources=TimeoutResources.GetAllResources();
                    $scope.num_machines_in_division=_.keys($scope.resources.division_machines.data).length;
                    division_machine_key = _.keys($scope.resources.division_machines.data)[$scope.current_division_machine_idx];
                    $scope.current_division_machine_id=$scope.resources.division_machines.data[division_machine_key].division_machine_id;                    
                    $scope.get_division_machine_results($scope.current_division_machine_id).then(function(data){
                        $scope.display_next_result();
                    });
                    
                });
                
                
            });
            
            $scope.get_division_machine_results = function(division_machine_id){
                Modals.loading();                
                results_promise = TimeoutResources.GetDivisionMachineResults(undefined,
                                                                             {site:$scope.site,division_machine_id:division_machine_id});                        
                return results_promise.then(function(data){
                    $scope.resources = TimeoutResources.GetAllResources();
                    $scope.team_tournament = $scope.resources.divisions.data[$scope.division_id].team_tournament;
                    //$scope.resources.division_machines.data["-1"]=$scope.jump_to_division_machine.data;
                    $scope.division_machine_name = $scope.resources.division_machine_results.data[0].machine_name;
                    console.log('get_division_machine_results');
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
