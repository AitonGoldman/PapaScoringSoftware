angular.module('prereg.step1.step2',['prereg.step1.step2.step3',
    /*REPLACEMECHILD*/]);
angular.module('prereg.step1.step2').controller(
    'prereg.step1.step2',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
        $scope.player_first_name=$state.params.player_first_name;
        $scope.player_last_name=$state.params.player_last_name;
        $scope.player_email = $state.params.player_email;
        $scope.utils = Utils;
        $scope.isWebView = ionic.Platform.isWebView();        
        $scope.ifpa_result_selected = {};
        $scope.get_ifpa_ranking = function(){
            player_name = $scope.player_first_name+$scope.player_last_name;
            dev_info = ionic.Platform.device();            
            if (_.size(dev_info)!=0){
                $scope.is_native=true;          
            } else {
                $scope.is_native=false;
            }                
            Modals.loading();
            player_name = player_name.replace(/ /g, "");
            players_promise = TimeoutResources.GetPlayersFast(undefined,{site:$scope.site});
            
            ifpa_promise = TimeoutResources.GetIfpaRanking(players_promise,{site:$scope.site,player_name:player_name});
            ifpa_promise.then(function(data){                
                $scope.resources = TimeoutResources.GetAllResources();
                $scope.dup_player = false;
                Modals.loaded();               
                results = _.filter($scope.resources.players.data, function(value,key){                                        
                    if(value.first_name+value.last_name == player_name){                        
                        return true;
                    }                    
                });
                if(results.length > 0 ){
                    $scope.dup_player = true;
                    return;
                }
                
                
                $scope.no_players_found = false;
                $scope.too_many_players_found = false;
                $scope.only_one_player_found = false;
                if($scope.resources.ifpa_rankings.data.search == "No players found"){
                    $scope.no_players_found = true;
                    return;
                }
                
                if($scope.resources.ifpa_rankings.data.search.length > 4){
                    $scope.too_many_players_found = true;
                    return;
                }

                if($scope.resources.ifpa_rankings.data.search.length == 1){
                    $scope.only_one_player_found = true;
                    return;
                }
                
                
                $scope.multiple_players_found = true;
                //$scope.result={};
                //ActionSheets.choose_ifpa_lookup_action($scope.resources.ifpa_rankings.data.search,$scope.player_info.ifpa_result);                
            });            
        };
        $scope.get_ifpa_ranking();
        //$scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
             
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
