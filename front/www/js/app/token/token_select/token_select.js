angular.module('app.token.token_select',['app.token.token_select.process',
    /*REPLACEMECHILD*/]);
angular.module('app.token.token_select').controller(
    'app.token.token_select',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {        
        $scope.site=$state.params.site;
	$scope.player_id=$state.params.player_id;
        $scope.sliders={'divisions':{},'metadivisions':{},'teams':{},
                        'divisions_costs':{},'metadivisions_costs':{},'teams_costs':{},
                        'player_id':$scope.player_id};
        token_promise = TimeoutResources.GetPlayerTokens(undefined,{site:$scope.site,player_id:$scope.player_id});
        divisions_promise = TimeoutResources.GetDivisions(token_promise,{site:$scope.site});
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                        
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        $scope.buttons={'divisions':{},metadivisions:{},teams:{}};
        $scope.total_cost=0;
        divisions_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();            
            if($scope.resources.player_tokens.data.player.teams != undefined){
                $scope.sliders.team_id=$scope.resources.player_tokens.data.player.teams[0].team_id;
            }
            _.forEach($scope.resources.player_tokens.data.tokens.divisions,function(value,key){                                
                $scope.sliders.divisions[key]=0;
                $scope.sliders.divisions_costs[key]=0;
                $scope.buttons.divisions[key]={};
                for(counter=0;counter<25;counter++){                    
                    $scope.buttons.divisions[key][counter]='green';                    
                }
            });
            _.forEach($scope.resources.player_tokens.data.tokens.metadivisions,function(value,key){                
                $scope.sliders.metadivisions[key]=0;
                $scope.sliders.metadivisions_costs[key]=0;

                $scope.buttons.metadivisions[key]={};
                for(counter=0;counter<25;counter++){                    
                    $scope.buttons.metadivisions[key][counter]='green';                    
                }
                
            });
            _.forEach($scope.resources.player_tokens.data.tokens.teams,function(value,key){                
                $scope.sliders.teams[key]=0;
                $scope.sliders.teams_costs[key]=0;
                $scope.buttons.teams[key]={};
                for(counter=0;counter<25;counter++){                    
                    $scope.buttons.teams[key][counter]='green';                    
                }                 
            });            
            //$scope.sliders.divisions=$scope.resources.player_tokens.data.tokens.divisions;
        });
        $scope.check_if_tokens_maxed_out = function(type, id){            
            if($scope.resources.player_tokens.data.available_tokens[type][id] == 0){
                return {'background-color':'red'};
            } else {
                return {};
            }
        };
        $scope.update_total_cost = function(){
            $scope.total_cost=0;
            _.forEach($scope.sliders,function(counts,type){
                if(type=="divisions_costs" || type =="metadivisions_costs" || type == "teams_costs"){
                _.forEach(counts,function(value,key){                                    
                    $scope.total_cost = $scope.total_cost+value;
                    //$scope.sliders.metadivisions[key]={value:0,division_total_cost:0};
                });      

                }
            });
            
        };
        $scope.set_token_count = function(type, division_id, number){
            for(x in $scope.buttons[type][division_id]){
                $scope.buttons[type][division_id][x]='green';
            }
            $scope.buttons[type][division_id][number]='red';
            $scope.sliders[type][division_id]=number;
            var division_price = $scope.resources.divisions.data[division_id].local_price;
            $scope.sliders[type+"_costs"][division_id]=division_price*number;
            $scope.update_total_cost();
            
        };
        $scope.disable_form_submit = function(){
            return false;
        };
        
    }]
);
