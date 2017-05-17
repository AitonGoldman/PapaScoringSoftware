angular.module('app.finals.manage.rollcall',[/*REPLACEMECHILD*/]);
angular.module('app.finals.manage.rollcall').controller(
    'app.finals.manage.rollcall',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
	$scope.division_final_id=$state.params.division_final_id;
        $scope.resources = {};
        $scope.scoreReviewed={checked:true};

        $scope.utils = Utils;
        //$scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);
        $scope.generate_rounds = function(){
            Modals.loading();
            thing = async.waterfall([
                function(callback){                
                    TimeoutResources.GenerateDivisionFinalRounds({site:$scope.site,division_final_id:$scope.division_final_id},$scope.resources.division_final_players.data,callback);                              }                                            
            ],function(err,result){
                Modals.loaded();
                if (err == null){
                    $scope.resources[result.resource_name] = result;                    
                    console.log($scope.resources);
                    //$scope.resources = Utils.extract_results_from_response(result);
                } else {
                    console.log(err);                                
                }
            });            
        };
        
        $scope.update_rollcall = function(){
            Modals.loading();
            thing = async.waterfall([
                function(callback){                
                    TimeoutResources.UpdateDivisionFinalPlayersRollcall({site:$scope.site,division_final_id:$scope.division_final_id},$scope.resources.division_final_players.data,callback);                              }                                            
            ],function(err,result){
                Modals.loaded();
                if (err == null){
                    $scope.resources[result.resource_name] = result;                
                    console.log($scope.resources);
                    //$scope.resources = Utils.extract_results_from_response(result);
                } else {
                    console.log(err);                                
                }
            });            
        };
        Modals.loading();
        //$scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state); 
        thing = async.waterfall([
            function(callback){                    
                TimeoutResources.GetDivisionFinalRoundCount({site:$scope.site,division_final_id:$scope.division_final_id},undefined,callback);
            },
            function(result,callback){                    
                $scope.resources[result.resource_name] = result;                
                console.log($scope.resources[result.resource_name].data);
                if($scope.resources[result.resource_name].data != undefined){
                    $state.go('.^');
                    callback('rounds already here',null);
                    return;
                }                    

                TimeoutResources.GetDivisionsEx({site:$scope.site},undefined,callback);
            },
            function(result,callback){                
                $scope.resources[result.resource_name] = result;                
                TimeoutResources.GetDivisionFinalPlayers({site:$scope.site,division_final_id:$scope.division_final_id},undefined,callback);                    
            }                                            
        ],function(err,result){            
            if (err == null){
                Modals.loaded();
                $scope.resources[result.resource_name] = result;                
                console.log($scope.resources);
                //$scope.resources = Utils.extract_results_from_response(result);
            } else {
                console.log(err);                                
            }
        });

        
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
