angular.module('app.results.divisions.division',[/*REPLACEMECHILD*/]);
angular.module('app.results.divisions.division').controller(
    'app.results.divisions.division',[
        '$scope','$state','TimeoutResources','Utils','Modals','$timeout','$ionicScrollDelegate',
        function($scope, $state, TimeoutResources, Utils,Modals,$timeout,$ionicScrollDelegate) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
	$scope.division_name=$state.params.division_name;
        $scope.filter_limit=25;
        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        results_promise = TimeoutResources.GetDivisionResults($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id});
                
        results_promise.then(function(data){
            $scope.process_division_results();                            
            Modals.loaded();
        });

        $scope.process_division_results = function(){
            $scope.resources = TimeoutResources.GetAllResources();            
            $scope.jump_to_division = {data:$scope.resources.divisions.data[$scope.division_id]};
            division = $scope.resources.divisions.data[$scope.division_id];            
            $scope.team_division = division.team_tournament;
            if($scope.team_division==false){
                raw_results = $scope.resources.division_results.data.ranked_player_list[$scope.division_id];
            } else {                
                raw_results = $scope.resources.division_results.data.ranked_team_list[$scope.division_id];
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
                    if(top_machines[n[1].team_id].length != 0){
                        return true;
                    } else {
                        return false;
                    }                    
                }
            });
            console.log(results);
            if(division.finals_player_selection_type == "ppo"){               
                $scope.a_cutoff=division.finals_num_qualifiers_ppo_a;                
                $scope.b_cutoff=division.finals_num_qualifiers_ppo_b;
                
                a_index = $scope.find_last_div_player_ppo_idx($scope.a_cutoff,results,division);
                $scope.results_a = _.slice(results,0,a_index+1);
                _.forEach($scope.results_a, function(value) {
                    console.log(value);
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
                $scope.div_cutoff=division.finals_num_qualifiers;                                                
                //results = $scope.resources.division_results.data.ranked_player_list[$scope.division_id];
                div_index = $scope.find_last_div_player_ppo_idx($scope.div_cutoff,results,division);
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
            division = $scope.resources.divisions.data[$scope.division_id];            
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
        $scope.doRefresh = function() {
            Modals.loading();            
        };
        $scope.doneRefresh = function() {
            $scope.resources.division_results.data = undefined;
            results_promise = TimeoutResources.GetDivisionResults(undefined,{site:$scope.site,division_id:$scope.division_id});
            
            results_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();            
                $scope.$broadcast('scroll.refreshComplete');
                $scope.process_division_results();
                $scope.filter_limit=75;
                //$scope.filter_limit=$scope.filter_limit+150;
                Modals.loaded();                
            });            
        };
            $scope.increase_display_window = function(){
                $scope.filter_limit=$scope.filter_limit+50;
                $ionicScrollDelegate.scrollBottom(true);
            };
            
        $scope.loadMore = function() {
            //$http.get('/more-items').success(function(items) {
            //     useItems(items);            
            $timeout(function(){
                $scope.filter_limit=$scope.filter_limit+20;
                $scope.$broadcast('scroll.infiniteScrollComplete');
            },50);
            
           // });
        };        
        
    }]
);
