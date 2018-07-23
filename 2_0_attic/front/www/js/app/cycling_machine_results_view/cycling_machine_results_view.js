angular.module('app.cycling_machine_results_view',[/*REPLACEMECHILD*/]);
angular.module('app.cycling_machine_results_view').controller(
    'app.cycling_machine_results_view',[
        '$scope','$state','TimeoutResources','Utils','Modals','$timeout','$ionicScrollDelegate',
        function($scope, $state, TimeoutResources, Utils,Modals,$timeout,$ionicScrollDelegate) {
            $scope.site=$state.params.site;
            $scope.current_division_machine_idx = 0;
            $scope.current_division_idx = 0;            
            $scope.current_division_machine_id = undefined;
            $scope.max_results_per_page=80;
            $scope.cur_num_results_displayed = 15;
            $scope.utils = Utils;            
            $scope.timeout_between_loads=5000;
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);
            $scope.display_next_result = function(){                
                $timeout(function(){                    
                    if($scope.resources.division_machine_results.data.length < $scope.cur_num_results_displayed || $scope.cur_num_results_displayed >= $scope.max_results_per_page){
                        $ionicScrollDelegate.scrollTo(0,0);                        
                        $scope.cur_num_results_displayed = 15;
                        $scope.current_division_machine_idx=$scope.current_division_machine_idx+1;
                        if($scope.current_division_machine_idx > $scope.num_machines_in_division-1){
                            $scope.current_division_idx=$scope.current_division_idx+1;
                            existing_divisions = _.filter(_.keys($scope.resources.divisions.data),function(o){return o != "metadivisions";});
                            if($scope.current_division_idx > existing_divisions.length - 1){
                                console.log('here wwe go');
                                $scope.current_division_idx = 0;
                            }
                            $scope.division_id=_.keys($scope.resources.divisions.data)[$scope.current_division_idx];                                            
                            $scope.current_division_division_machines = _.filter($scope.resources.all_division_machines.data, function(o) { return o.division_id==$scope.division_id; });
                            $scope.current_division_machine_idx=0;
                            
                        }
                        //division_machine_key = _.keys($scope.resources.division_machines.data)[$scope.current_division_machine_idx];
                        $scope.current_division_machine_id=$scope.current_division_division_machines[$scope.current_division_machine_idx].division_machine_id;
                        $scope.get_division_machine_results($scope.current_division_machine_id).then(function(data){
                            $scope.display_next_result();
                        });                        
                    } else {                        
                        $scope.cur_num_results_displayed = $scope.cur_num_results_displayed +10;                        
                        $ionicScrollDelegate.scrollBy(0,500,true);                        
                        $scope.display_next_result();                        
                    }
                }, $scope.timeout_between_loads);
                
            };
            $scope.bootstrap_promise.then(function(data){
                $scope.resources=TimeoutResources.GetAllResources();
                //$scope.starting_division_machine_id=1;
                $scope.division_id=_.keys($scope.resources.divisions.data)[$scope.current_division_idx];                
                $ionicScrollDelegate.getScrollView().options.animationDuration = 1000;
                TimeoutResources.GetCyclingAllDivisionMachines(undefined,{site:$scope.site}).then(function(data){                    
                    $scope.resources=TimeoutResources.GetAllResources();                    
                    $scope.current_division_division_machines = _.filter($scope.resources.all_division_machines.data, function(o) { return o.division_id==$scope.division_id; });
                    $scope.num_machines_in_division=$scope.current_division_division_machines.length;
                    division_machine = $scope.current_division_division_machines[$scope.current_division_machine_idx];                    
                    $scope.current_division_machine_id=division_machine.division_machine_id;                    
                    $scope.get_division_machine_results($scope.current_division_machine_id).then(function(data){
                        $scope.display_next_result();
                    });
                    
                });
                
                
            });
            
            $scope.get_division_machine_results = function(division_machine_id){
                //Modals.loading();                
                results_promise = TimeoutResources.GetCyclingDivisionMachineResults(undefined,
                                                                             {site:$scope.site,division_machine_id:division_machine_id});                        
                return results_promise.then(function(data){
                    $scope.resources = TimeoutResources.GetAllResources();
                    $scope.team_tournament = $scope.resources.divisions.data[$scope.division_id].team_tournament;
                    //$scope.resources.division_machines.data["-1"]=$scope.jump_to_division_machine.data;
                    $scope.division_machine_name = $scope.current_division_division_machines[$scope.current_division_machine_idx].division_machine_name;
                    ////$scope.division_machine_name = $scope.resources.division_machine_results.data[0].machine_name;                    
                    //Modals.loaded();            
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

angular.module('app.cycling_division_results_view',[/*REPLACEMECHILD*/]);
angular.module('app.cycling_division_results_view').controller(
    'app.cycling_division_results_view',[
        '$scope','$state','TimeoutResources','Utils','Modals','$timeout','$ionicScrollDelegate',
        function($scope, $state, TimeoutResources, Utils,Modals,$timeout,$ionicScrollDelegate) {
            $scope.site=$state.params.site;
            $scope.starting_division_id=parseInt($state.params.starting_division_id);            
            $scope.current_division_id = 1;
            $scope.num_divisions=4;
            $scope.cur_num_results_displayed = 15;
            $scope.utils = Utils;
            $scope.current_division_idx = 0;            
            $scope.max_results_per_page=80;            
            $scope.timeout_between_loads=5000;
            
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);
            $scope.display_next_result = function(){                
                $timeout(function(){                                        
		    if($scope.concat_results.length < $scope.cur_num_results_displayed || $scope.cur_num_results_displayed > $scope.max_results_per_page){

                        console.log('moving to next division...');
                        $ionicScrollDelegate.scrollTo(0,0);                        
                        $scope.cur_num_results_displayed = 15;
                        $scope.current_division_idx=$scope.current_division_idx+1;
                        existing_divisions = _.filter(_.keys($scope.resources.divisions.data),function(o){return o != "metadivisions";});
                        if($scope.current_division_idx > existing_divisions.length - 1){
                            console.log('here wwe go');
                            $scope.current_division_idx = 0;
                        }
                        $scope.current_division_id=_.keys($scope.resources.divisions.data)[$scope.current_division_idx];                                            
                        $scope.team_division = $scope.resources.divisions.data[$scope.current_division_id].team_tournament;                                

                        $scope.get_division_results($scope.current_division_id).then(function(data){
                            $scope.display_next_result();                            
                        });                        
                    } else {                        
                        $scope.cur_num_results_displayed = $scope.cur_num_results_displayed +10;                        
                        console.log('increment...'+$scope.cur_num_results_displayed);
                        $ionicScrollDelegate.scrollBy(0,500,true);                        
                        $scope.display_next_result();                        
                    }
                }, $scope.timeout_between_loads);
            };
            $scope.bootstrap_promise.then(function(data){
                $ionicScrollDelegate.getScrollView().options.animationDuration = 1000;
                $scope.resources = TimeoutResources.GetAllResources();
                $scope.current_division_id=_.keys($scope.resources.divisions.data)[$scope.current_division_idx];
                $scope.team_division = $scope.resources.divisions.data[$scope.current_division_id].team_tournament;                                
                $scope.get_division_results($scope.current_division_id).then(function(data){
                    $scope.display_next_result();
                });                                
            });
            
            $scope.get_division_results = function(division_id){
                //Modals.loading();                
                results_promise = TimeoutResources.GetCyclingDivisionResults(undefined,
                                                                             {site:$scope.site,division_id:division_id});                        
                return results_promise.then(function(data){
                    if(data != undefined){
                        $scope.process_division_results();    
                    }
                    console.log(data);
                    //$scope.resources = TimeoutResources.GetAllResources();                                        
                    $scope.division_name = $scope.resources.divisions.data[division_id].tournament_name;                    
                    //Modals.loaded();            
                });            
            };
        $scope.process_division_results = function(){
            $scope.resources = TimeoutResources.GetAllResources();            
            $scope.jump_to_division = {data:$scope.resources.divisions.data[$scope.current_division_id]};
            division = $scope.resources.divisions.data[$scope.current_division_id];            
	    
            //$scope.team_division = division.team_tournament;
            if($scope.team_division != true){                
                raw_results = $scope.resources.division_results.data.ranked_player_list[$scope.current_division_id];
            } else {
                raw_results = $scope.resources.division_results.data.ranked_team_list[$scope.current_division_id];                
            }            
            top_machines = $scope.resources.division_results.data.top_machines[division.division_id];
            results = _.remove(raw_results,function(n) {
                if($scope.team_division==false){
                    if(top_machines[n[1].player_id].length != 0){
                        return true;
                    } else {
                        return false;
                    }
                } else {
                    console.log(n[1]);
                    if(top_machines[n[1].team_id].length != 0){
                        return true;
                    } else {
                        return false;
                    }                    
                }
            });            
            if(division.finals_player_selection_type == "ppo"){               
                $scope.a_cutoff=division.finals_num_qualifiers_ppo_a;                
                $scope.b_cutoff=division.finals_num_qualifiers_ppo_b;
                
                a_index = $scope.find_last_div_player_ppo_idx($scope.a_cutoff,results,division);
                $scope.results_a = _.slice(results,0,a_index+1);
                _.forEach($scope.results_a, function(value) {                    
                    value[1].a_division=true;                    
                });
                b_index = $scope.find_last_div_player_ppo_idx($scope.b_cutoff,
                                                              _.slice(results,a_index+1),
                                                              division);
                $scope.results_b = _.slice(_.slice(results,a_index+1),
                                           0,
                                           b_index+1);                
                $scope.rest_results = _.slice(results,a_index+1+b_index+1);
                $scope.divider_a = [[0,{divider:'A QUALIFYING CUTOFF'}]];                                
                if($scope.results_b.length > 0){
                    $scope.divider_b = [[0,{divider:'B QUALIFYING CUTOFF'}]];
                    $scope.concat_results = _.concat($scope.results_a,$scope.divider_a,$scope.results_b,$scope.divider_b,$scope.rest_results);                                  
                } else {
                    $scope.concat_results = _.concat($scope.results_a,$scope.divider_a);          
                }
            }
            if(division.finals_player_selection_type == "papa"){
                console.log('figuring out cutoff..');
                $scope.div_cutoff=division.finals_num_qualifiers;
                console.log('cutoff is ..'+$scope.div_cutoff);
                //results = $scope.resources.division_results.data.ranked_player_list[$scope.division_id];
                div_index = $scope.find_last_div_player_ppo_idx($scope.div_cutoff,results,division);
                console.log('div_index is '+div_index);
                console.log('passing in results...');
                console.log(results);
                $scope.qualifying_results = _.slice(results,0,div_index+1);                
                $scope.rest_results = _.slice(results,div_index+1);
                $scope.divider = [[0,{divider:'QUALIFYING CUTOFF'}]];                
                $scope.concat_results = _.concat($scope.qualifying_results,$scope.divider,$scope.rest_results);                
            }                            
            //Modals.loaded();
        };
        $scope.find_last_div_player_ppo_idx = function(cutoff,results,division){
            if(results.length <= cutoff ){                                                
                idx = results.length-1;
                console.log('returning idx..'+idx);
                return idx;
            }
            idx = cutoff-1;
            top_machines = $scope.resources.division_results.data.top_machines[division.division_id];
            while(idx+1 != results.length && results[idx][0]==results[idx+1][0]){                
                idx=idx+1;                
            }
            return idx;
        };
        $scope.jump_to_division_results = function(){                        
            if($scope.jump_to_division.data == undefined || $scope.jump_to_division.data.division_id == undefined){
                return;
            }
            
            $state.go("^.division",({division_id:$scope.jump_to_division.data.division_id,division_name:$scope.jump_to_division.data.division_name}));
        };
        $scope.check_player_is_ifpa_limited = function(player){
            division = $scope.resources.divisions.data[$scope.current_division_id];            
            $scope.a_cutoff=division.finals_num_qualifiers_ppo_a;
            $scope.div_cutoff=division.finals_num_qualifiers;            
            if(division.finals_player_selection_type == "ppo"){
                if (division.ppo_a_ifpa_range_end > player.ifpa_ranking && player.a_division != true){                                        
                    return true;
                } else {                   
                    return false;
                }
            }
            if(division.finals_player_selection_type == "papa"){
                if (division.ifpa_range_end > player.ifpa_ranking){                                        
                    return true;
                } else {                   
                    return false;
                }
            }
            
            
            return false;
        };            
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
