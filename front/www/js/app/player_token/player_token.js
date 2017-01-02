angular.module('app.player_token',[
    'app.player_token.confirm',
    /*REPLACEMECHILD*/]);
angular.module('app.player_token').controller(
    'app.player_token',[
        '$scope','$state','TimeoutResources','Utils','Modals','User',
        function($scope, $state, TimeoutResources, Utils,Modals,User) {
            $scope.site=$state.params.site;
            $scope.token_info = {
                divisions:{},
                metadivisions:{},
                teams:{},
                divisions_names:{},
                metadivisions_names:{},
                total_cost:0
            };
            
            $scope.utils = Utils;
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
            $scope.utils = Utils;
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                        
            $scope.bootstrap_promise.then(function(data){
                Modals.loading();
                console.log(User.logged_in_user);
	        $scope.player_id=User.logged_in_user().player.player_id;
                
                token_promise = TimeoutResources.GetPlayerTokens(undefined,{site:$scope.site,player_id:$scope.player_id});            
                divisions_promise = TimeoutResources.GetDivisions(token_promise,{site:$scope.site});
                divisions_promise.then(function(data){
                    $scope.resources = TimeoutResources.GetAllResources();
                    console.log($scope.resources);
                    Modals.loaded();
                    
                    
                });
            });
            $scope.calc_total_cost = function(){
                divisions_total=0;
                _.forEach($scope.token_info.divisions, function(value, key) {
                    division_price = $scope.resources.divisions.data[key].local_price;
                    divisions_total = divisions_total + ($scope.token_info.divisions[key]*parseInt(division_price));
                    $scope.token_info.divisions_names[key]=$scope.resources.divisions.data[key].tournament_name;
                });
                _.forEach($scope.token_info.teams, function(value, key) {
                    division_price = $scope.resources.divisions.data[key].local_price;
                    divisions_total = divisions_total + ($scope.token_info.teams[key]*parseInt(division_price));
                    $scope.token_info.divisions_names[key]=$scope.resources.divisions.data[key].tournament_name;
                });                
                _.forEach($scope.token_info.metadivisions, function(value, key) {
                    console.log($scope.token_info);
                    //FIXME : ugh
                    for(x in $scope.resources.divisions.data){                        
                        if ($scope.resources.divisions.data.metadivisions[key].divisions[x] != undefined){
                            division_price = $scope.resources.divisions.data[x].local_price;        
                        }
                    }
                    divisions_total = divisions_total + ($scope.token_info.metadivisions[key]*parseInt(division_price));
                    $scope.token_info.metadivisions_names[key]=$scope.resources.divisions.data.metadivisions[key].meta_division_name;
                });
                
                
                $scope.token_info.total_cost = divisions_total;
            };
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // 
            //$scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
