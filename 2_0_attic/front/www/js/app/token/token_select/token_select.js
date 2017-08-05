angular.module('app.token.token_select',['app.token.token_select.confirm',
    /*REPLACEMECHILD*/]);
angular.module('app.token.token_select').controller(
    'app.token.token_select',[
        '$scope','$state','TimeoutResources','Utils','Modals',
        function($scope, $state, TimeoutResources, Utils,Modals) {        
            $scope.state=$state.current.name;
            $scope.site=$state.params.site;
            $scope.token_info = {
                divisions:{},
                metadivisions:{},
                teams:{},
                divisions_names:{},
                metadivisions_names:{},
                total_cost:0,
                comped:false
            };
            
            if($state.current.name=='app.token_comp.token_select_comp'){
                $scope.comp_or_purchase_title="Comp Tickets";
                $scope.token_info.comped=true;
            } else {
                $scope.comp_or_purchase_title="Purchase Tickets";
            }
            
            $scope.utils = Utils;
            $scope.hide_back_button=$state.params.hide_back_button;
            Modals.loading();
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
            $scope.utils = Utils;
            $scope.bootstrap_promise.then(function(data){                            
                $scope.player_id=$state.params.player_id;
                token_promise = TimeoutResources.GetPlayerTokens(undefined,{site:$scope.site,player_id:$scope.player_id});
                token_promise.then(function(data){
                    $scope.resources = TimeoutResources.GetAllResources();                    
                    _.forEach($scope.resources.player_tokens.data.available_tokens.divisions_remaining_token_list, function(value, key) {
                        $scope.token_info.divisions[key]=value[0];
                    });
                    _.forEach($scope.resources.player_tokens.data.available_tokens.teams_remaining_token_list, function(value, key) {
                        $scope.token_info.teams[key]=value[0];
                    });
                    _.forEach($scope.resources.player_tokens.data.available_tokens.metadivisions_remaining_token_list, function(value, key) {
                        $scope.token_info.metadivisions[key]=value[0];
                    });
                    Modals.loaded();
                });
            });
            $scope.calc_total_cost = function(){
                divisions_total=0;
                _.forEach($scope.token_info.divisions, function(value, key) {
                    divisions_total = divisions_total + value[1];
                    $scope.token_info.divisions_names[key]=$scope.resources.divisions.data[key].tournament_name;
                });
                _.forEach($scope.token_info.teams, function(value, key) {
                    //division_price = $scope.resources.divisions.data[key].local_price;
                    divisions_total = divisions_total + value[1];//($scope.token_info.teams[key]*parseInt(division_price));
                    $scope.token_info.divisions_names[key]=$scope.resources.divisions.data[key].tournament_name;
                });                
                 _.forEach($scope.token_info.metadivisions, function(value, key) {
                       divisions_total = divisions_total + value[1];//($scope.token_info.teams[key]*parseInt(division_price));
                     $scope.token_info.metadivisions_names[key]=$scope.resources.divisions.data.metadivisions[key].meta_division_name;
                 });
                if($state.current.name=='app.token_comp.token_select_comp'){                    
                    $scope.token_info.total_cost = "COMPED";                    
                } else {
                    $scope.token_info.total_cost = divisions_total;
                }                                 
            };
        }
    ]
);
