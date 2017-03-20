angular.module('app.ticket_prices',[/*REPLACEMECHILD*/]);
angular.module('app.ticket_prices').controller(
    'app.ticket_prices',[
        '$scope','$state','TimeoutResources','Utils','Modals',
        function($scope, $state, TimeoutResources, Utils,Modals) {
            $scope.site=$state.params.site;

            $scope.utils = Utils;
            Modals.loading();
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                        
            $scope.bootstrap_promise.then(function(data){
                $scope.resources=TimeoutResources.GetAllResources();
                $scope.division_prices = $scope.show_ticket_prices();
                Modals.loaded();
            });
            
            
            $scope.show_ticket_prices = function(){
                division_prices = [];
                _.forEach($scope.resources.divisions.data, function(value, key) {                    
                    division=value;
                    division_string = "";
                    if (key!="metadivisions" && division.meta_division_id==undefined){
                        division_info = {};
                        division_info = {min_num_tickets_to_purchase:division.min_num_tickets_to_purchase,
                                         tournament_name:division.tournament_name,
                                         local_price:division.local_price};
                        
                        //                        division_string = division_string + division.tournament_name +" - "+division.min_num_tickets_to_purchase+" for "+ division.local_price;
                        if(division.discount_ticket_count>0){
                            division_info.discount_ticket_count=division.discount_ticket_count;
                            division_info.discount_ticket_price=division.discount_ticket_price;                            
                            //division_string = division_string + ","+division.discount_ticket_count+" for "+division.discount_ticket_price;
                        } 
                        division_prices.push(division_info);
                    }
                    
                });
                _.forEach($scope.resources.divisions.data.metadivisions, function(value, key) {                    
                    division=value;
                        division_info = {};
                        division_info = {min_num_tickets_to_purchase:division.min_num_tickets_to_purchase,
                                         tournament_name:division.meta_division_name,
                                         local_price:division.local_price};
                        
                        //                        division_string = division_string + division.tournament_name +" - "+division.min_num_tickets_to_purchase+" for "+ division.local_price;
                        if(division.discount_ticket_count>0){
                            division_info.discount_ticket_count=division.discount_ticket_count;
                            division_info.discount_ticket_price=division.discount_ticket_price;                            
                            //division_string = division_string + ","+division.discount_ticket_count+" for "+division.discount_ticket_price;
                        } 
                    division_prices.push(division_info);                    
                });                
                return division_prices;
            };
            
        }]
);
