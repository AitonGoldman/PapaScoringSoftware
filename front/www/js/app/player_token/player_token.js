angular.module('app.player_token',[
    'app.player_token.confirm',
    /*REPLACEMECHILD*/]);
angular.module('app.player_token').controller(
    'app.player_token',[
        '$scope','$state','TimeoutResources','Utils','Modals','User','$ionicPopup','$ionicPopover',
        function($scope, $state, TimeoutResources, Utils,Modals,User,$ionicPopup,$ionicPopover) {
            $scope.site=$state.params.site;
            $scope.token_info = {
                divisions:{},
                metadivisions:{},
                teams:{},
                divisions_names:{},
                metadivisions_names:{},
                total_cost:0
            };
            $scope.test_range = [0,1,2,3];
            $scope.utils = Utils;
            Modals.loading();
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                        
            $scope.bootstrap_promise.then(function(data){                
               
	        $scope.player_id=User.logged_in_user().player.player_id;
                
                token_promise = TimeoutResources.GetPlayerTokens($scope.bootstrap_promise,{site:$scope.site,player_id:$scope.player_id});            
                token_promise.then(function(data){
                    $scope.resources = TimeoutResources.GetAllResources();                    
                    console.log($scope.resources);     
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
                $scope.token_info.total_cost = divisions_total;
            };
            $scope.show_ticket_prices = function(){
                $scope.$broadcast('scroll.refreshComplete');
                division_prices_string = [];
                _.forEach($scope.resources.divisions.data, function(value, key) {                    
                    division=value;
                    division_string = "";
                    if (key!="metadivisions" && division.meta_division_id==undefined){
                        division_string = division_string + division.tournament_name +" - "+division.min_num_tickets_to_purchase+" for "+ division.local_price;
                        if(division.discount_ticket_count>0){
                            division_string = division_string + ","+division.discount_ticket_count+" for "+division.discount_ticket_price;
                        } 
                        division_prices_string.push(division_string);
                    }
                    
                });
                _.forEach($scope.resources.divisions.data.metadivisions, function(value, key) {                    
                    division=value;
                    division_string = "";
                    division_string = division_string + division.meta_division_name +" - "+division.min_num_tickets_to_purchase+" for "+ division.local_price;
                    if(division.discount_ticket_count>0){
                        division_string = division_string + ","+division.discount_ticket_count+" for "+division.discount_ticket_price;
                    } 
                    division_prices_string.push(division_string);                    
                });                
                
                //$scope.popover = $ionicPopover.fromTemplate(division_prices_string, {
                //    scope: $scope
                //});
                //$scope.popover.show();
                // var alertPopup = $ionicPopup.alert({
                //    title: 'Ticket Price List',
                //    template: division_prices_string                    
                // });
                Modals.information(division_prices_string);
                //division.tournament_name division.min_num_tickets_to_purchase division.local_price  division.discount_ticket_count division.discount_ticket_price 
            };
    }]
);
