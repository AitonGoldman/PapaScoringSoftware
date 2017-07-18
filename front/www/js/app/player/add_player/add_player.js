angular.module('app.player.add_player',['app.player.add_player.process',
    /*REPLACEMECHILD*/]);
angular.module('app.player.add_player').controller(
    'app.player.add_player',[
        '$scope','$state','TimeoutResources','Utils','Modals','ActionSheets',
        function($scope, $state, TimeoutResources, Utils,Modals,ActionSheets) {
            $scope.site=$state.params.site;
            $scope.player_info={ifpa_result:{},linked_division_id:undefined};
            $scope.utils = Utils;
            $scope.division_ifpa_limits={};
            Modals.loading();
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
            //divisions_promise = TimeoutResources.GetDivisions(undefined,{site:$scope.site});            
            // = TimeoutResources.GetEtcData();
            $scope.bootstrap_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                $scope.limit_divisions_based_on_ranking(99999999);
                $scope.main_division_count = _.filter($scope.resources.divisions.data, { 'single_division': false}).length;
                dev_info = ionic.Platform.device();            
                if (_.size(dev_info)!=0){
                    $scope.is_native=true;          
                }                
                Modals.loaded();
            });
            $scope.limit_divisions_based_on_ranking = function(ranking){
                $scope.main_divisions = _.filter($scope.resources.divisions.data, { 'single_division': false});
                $scope.num_div_allowed=0;                
                _.forEach($scope.main_divisions, function(value, key) {
                    $scope.division_ifpa_limits[value.division_id]=value.ifpa_range_start;
                    if($scope.division_ifpa_limits[value.division_id] < $scope.player_info.ifpa_result){
                        $scope.num_div_allowed=$scope.num_div_allowed+1;
                    }                                
                });       
            };
            $scope.get_ifpa_ranking = function(){
                player_name = $scope.player_info.first_name;
                if(Utils.var_empty($scope.player_info.last_name) == false){
                    player_name=player_name+$scope.player_info.last_name;
                } else {
                    return
                }
                Modals.loading();
                player_name = player_name.replace(/ /g, ""); 
                ifpa_promise = TimeoutResources.GetIfpaRanking(undefined,{site:$scope.site,player_name:player_name});
                ifpa_promise.then(function(data){
                    $scope.resources = TimeoutResources.GetAllResources();
                    Modals.loaded();                    
                    $scope.result={};
                    ActionSheets.choose_ifpa_lookup_action($scope.resources.ifpa_rankings.data.search,$scope.player_info.ifpa_result,$scope.limit_divisions_based_on_ranking);                
                });            
            };
            $scope.form_not_ready_for_submit = function(){
                if (Utils.var_empty($scope.player_info.first_name) == true || Utils.var_empty($scope.player_info.last_name) == true){                    
                    return true;
                } else {
                    return false;
                }
            };            
        }
    ]
);
