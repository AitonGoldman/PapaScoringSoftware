angular.module('app.token.token_select',['app.token.token_select.process',
    /*REPLACEMECHILD*/]);
angular.module('app.token.token_select').controller(
    'app.token.token_select',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {        
        $scope.site=$state.params.site;
	$scope.player_id=$state.params.player_id;
        $scope.sliders={'divisions':{},'metadivisions':{},'teams':{},'player_id':$scope.player_id};
        token_promise = TimeoutResources.GetPlayerTokens(undefined,{site:$scope.site,player_id:$scope.player_id});
        divisions_promise = TimeoutResources.GetDivisions(token_promise,{site:$scope.site});
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                        
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        divisions_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();            
            if($scope.resources.player_tokens.data.player.teams != undefined){
                $scope.sliders.team_id=$scope.resources.player_tokens.data.player.teams[0].team_id;
            }
            _.forEach($scope.resources.player_tokens.data.tokens.divisions,function(value,key){                
                $scope.sliders.divisions[key]=0;                
            });
            _.forEach($scope.resources.player_tokens.data.tokens.metadivisions,function(value,key){                
                $scope.sliders.metadivisions[key]=0;                
            });
            _.forEach($scope.resources.player_tokens.data.tokens.teams,function(value,key){                
                $scope.sliders.teams[key]=0;                
            });            
            
            
            //$scope.sliders.divisions=$scope.resources.player_tokens.data.tokens.divisions;
        });
        $scope.check_if_tokens_maxed_out = function(type, id){
            console.log($scope.resources.player_tokens.data.available_tokens);
            if($scope.resources.player_tokens.data.available_tokens[type][id] == 0){
                return {'background-color':'red'};
            } else {
                return {};
            }
        };
        $scope.disable_form_submit = function(){
            return false;
        };
        
    }]
);
