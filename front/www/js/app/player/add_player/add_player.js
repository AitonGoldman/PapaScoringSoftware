angular.module('app.player.add_player',['app.player.add_player.process',
    /*REPLACEMECHILD*/]);
angular.module('app.player.add_player').controller(
    'app.player.add_player',[
        '$scope','$state','TimeoutResources','Utils','Modals','ActionSheets',
        function($scope, $state, TimeoutResources, Utils,Modals,ActionSheets) {
            $scope.site=$state.params.site;
            $scope.player_info={ifpa_result:{},linked_division_id:undefined};
            $scope.utils = Utils;
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
            divisions_promise = TimeoutResources.GetDivisions(undefined,{site:$scope.site});
            Modals.loading();
            // = TimeoutResources.GetEtcData();
            divisions_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                $scope.main_divisions = _.filter($scope.resources.divisions.data, { 'single_division': false});                
                Modals.loaded();
            });
            $scope.get_ifpa_ranking = function(){
                player_name = $scope.player_info.first_name;
                if(Utils.var_empty($scope.player_info.last_name) == false){
                    player_name=player_name+$scope.player_info.last_name;
                }
                Modals.loading();
                player_name = player_name.replace(/ /g, ""); 
                ifpa_promise = TimeoutResources.GetIfpaRanking(undefined,{site:$scope.site,player_name:player_name});
                ifpa_promise.then(function(data){
                    $scope.resources = TimeoutResources.GetAllResources();
                    Modals.loaded();                    
                    $scope.result={};
                    ActionSheets.choose_ifpa_lookup_action($scope.resources.ifpa_rankings.data.search,$scope.player_info.ifpa_result);                
                });            
            };
            $scope.form_not_ready_for_submit = function(){
                if ($scope.is_native == true && $scope.player_info.has_picture != true){
                    return true;
                }
                if (Utils.var_empty($scope.player_info.first_name) == true || Utils.var_empty($scope.player_info.last_name) == true || Utils.var_empty($scope.player_info.linked_division_id) == true || $scope.player_info.ifpa_result.looked_up != true){                    
                    return true;
                } else {
                    return false;
                }
            };
        }
    ]
);
