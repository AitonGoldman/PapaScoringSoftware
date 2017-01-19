angular.module('app.ppo_qualifying_list.qualifiers',[/*REPLACEMECHILD*/]);
angular.module('app.ppo_qualifying_list.qualifiers').controller(
    'app.ppo_qualifying_list.qualifiers',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
        $scope.display_removed_players=false;
        $scope.utils = Utils;
        $scope.tie_breakers={data:{}};
        $scope.tie_breaker_ranks = {};        
        $scope.players_present={data:{}};
        $scope.removed_players={data:{}};
        $scope.tie_breaker_selects = {"a":{}};
        $scope.selecting_players = true;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        Modals.loading();
        qual_promise = TimeoutResources.GetDivisionQualifyingResultsPPO($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id},{});        
        // = TimeoutResources.GetEtcData();
        
        qual_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            $scope.set_all_players_to_present();
            Modals.loaded();
        });

        $scope.set_all_players_to_present = function(){
            _.forEach($scope.resources.ppo_qualifying_list.data.a, function(value) {
                value[1].present=true;
                $scope.players_present.data[value[1].player_id]=value[1];                
            });
            _.forEach($scope.resources.ppo_qualifying_list.data.b, function(value) {
                value[1].present=true;
                $scope.players_present.data[value[1].player_id]=value[1];                
            });
            $scope.get_num_ties_ex("a");
            $scope.get_num_ties_ex("b");                        
        };
        $scope.on_change = function(){
            $scope.tie_breakers_available = false;
            $scope.removed_players.data = _.pickBy($scope.players_present.data,{present:false});            
            if(_.size($scope.removed_players.data)==0){
                $scope.display_removed_players = false;
            } else {
                $scope.display_removed_players = true;
            }
            qual_promise = TimeoutResources.GetDivisionQualifyingResultsPPO($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id},{absent_players:$scope.removed_players.data});
            Modals.loading();            
        
            qual_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                $scope.set_all_players_to_present();
                 Modals.loaded();
            });                            
        };
        $scope.on_submit = function(){            
            $scope.removed_players.data = _.pickBy($scope.players_present.data,{present:false});            
            _.forEach($scope.resources.ppo_qualifying_list.data.a, function(value) {                
                if(value[1].selected_option){
                    $scope.tie_breaker_ranks[value[1].player_id]=value[1].selected_option;
                }
            });
            _.forEach($scope.resources.ppo_qualifying_list.data.b, function(value) {                
                if(value[1].selected_option){
                    console.log('found b values');
                    $scope.tie_breaker_ranks[value[1].player_id]=value[1].selected_option;                    
                }
            });
            for(x=1;x<50;x++){
                possible_dupes = _.filter($scope.tie_breaker_ranks, function(o) { return o == x; });
                if(possible_dupes.length > 1){
                    //return;
                }
            }
                        
            Modals.loading();            
            qual_promise = TimeoutResources.GetDivisionQualifyingResultsPPO($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id},{absent_players:$scope.removed_players.data,tie_breaker_ranks:$scope.tie_breaker_ranks});
            //
        
            qual_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                $scope.set_all_players_to_present();
                Modals.loaded();
                $scope.selecting_players = false;
                
            });                            
        };
        
        $scope.get_num_ties_ex = function(div){
            last_div_idx = $scope.resources.ppo_qualifying_list.data[div].length - 1;
            for(x=0;x<=last_div_idx;x++){
                
                cur_rank=$scope.resources.ppo_qualifying_list.data[div][x][0];
                start_idx=x;
                end_idx=x;
                new_idx=end_idx+1;                
                while(new_idx<=last_div_idx && $scope.resources.ppo_qualifying_list.data[div][new_idx][0] == cur_rank){                                        
                    end_idx=new_idx;
                    new_idx=new_idx+1;
                }
                if(start_idx != end_idx){
                    return_array = [];
                    new_start_rank = $scope.resources.ppo_qualifying_list.data[div][start_idx][0];
                    for(y=0;y<=end_idx-start_idx;y++){                
                        return_array.push(new_start_rank+y+1);
                    }
                    for(y=start_idx;y<=end_idx;y++){
                        $scope.resources.ppo_qualifying_list.data[div][y][1].select_options=return_array;
                        $scope.resources.ppo_qualifying_list.data[div][y][1].selected_option=return_array[0];                        
                        
                    }
                    x=x+(end_idx-start_idx);
                }
            }
        };
        
        $scope.get_num_ties = function(idx,div){
            rank = $scope.resources.ppo_qualifying_list.data[div][idx][0];
            last_idx = $scope.resources.ppo_qualifying_list.data[div].length-1;
            new_idx=idx-1;
            start_idx = idx;
            end_idx=idx;
            while(new_idx>=0){
                if($scope.resources.ppo_qualifying_list.data[div][new_idx][0] == rank){
                    start_idx=new_idx;
                    new_idx=new_idx-1;
                } else {
                    break;
                }                
            }
            new_idx = idx+1;
            while(new_idx<=last_idx){
                if($scope.resources.ppo_qualifying_list.data[div][new_idx][0] == rank){
                    end_idx=new_idx;
                    new_idx=new_idx+1;
                } else {                                                            
                    break;
                }                
            }
            return_array = [];
            new_rank = $scope.resources.ppo_qualifying_list.data[div][start_idx][0];
            for(x=0;x<=end_idx-start_idx;x++){                
                return_array.push(new_rank+x+1);
            }
            if(end_idx-start_idx!=0){
                $scope.tie_breakers_available = true;
            }
            return return_array;
            //return [$scope.resources.ppo_qualifying_list.data[div][idx][];]
        };
        $scope.show_tiebreaker_input = function(idx,div){
            rank = $scope.resources.ppo_qualifying_list.data[div][idx][0];
            last_idx = $scope.resources.ppo_qualifying_list.data[div].length - 1;
            if(idx == 0){
                if($scope.resources.ppo_qualifying_list.data[div][1][0]==rank){
                    return true;
                } else {
                    return false;
                }
            }
            if(idx == last_idx){
                if($scope.resources.ppo_qualifying_list.data[div][last_idx-1][0]==rank){
                    return true;
                } else {
                    return false;
                }
            }
            if($scope.resources.ppo_qualifying_list.data[div][idx-1][0]==rank || $scope.resources.ppo_qualifying_list.data[div][idx+1][0]==rank){
                return true;
            } else {
                return false;
            }
        };
        
        $scope.debug = function(){
            console.log($scope.tie_breakers);
        };
    }]
);
