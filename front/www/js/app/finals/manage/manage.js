angular.module('app.finals.manage',['app.finals.manage.tiebreakers',
    'app.finals.manage.rollcall',
    /*REPLACEMECHILD*/]);
angular.module('app.finals.manage').controller(
    'app.finals.manage',[
        '$scope','$state','TimeoutResources','Utils','Modals','$ionicActionSheet',
        function($scope, $state, TimeoutResources, Utils,Modals,$ionicActionSheet) {

            $scope.choose_undo_action = function(target){            
                var hideSheet = $ionicActionSheet.show({
                    buttons: [
                        { text: 'Undo Finals' }                              
                    ],                    
                    titleText: '<b style="color:red">You are about to undo this tournaments Finals!  This will delete all scores and information recorded for it.  Are you sure you want to do this?</b>',
                    cancelText: 'Cancel',
                    cancel: function() {
                        //player_info.linked_division_id = player_info.old_linked_division_id;
                        // add cancel code..
                    },
                    buttonClicked: function(index) {
                        $scope.delete_division_final();                     
                        return true;
                    }
                });
            };                  

            $scope.choose_reopen_final_round_action = function(division_final_round_id){            
                var hideSheet = $ionicActionSheet.show({
                    buttons: [
                        { text: 'Reopen Final Round' }                              
                    ],                    
                    titleText: '<b style="color:red">You are about to reopen this final round!  This will delete all scores and information for subsequent rounds.  Are you sure you want to do this?</b>',
                    cancelText: 'Cancel',
                    cancel: function() {
                        //player_info.linked_division_id = player_info.old_linked_division_id;
                        // add cancel code..
                    },
                    buttonClicked: function(index) {
                        $scope.reopen_division_final_round(division_final_round_id);                     
                        return true;
                    }
                });
            };                  
            
            $scope.delete_division_final = function(){
                Modals.loading();                
                async.waterfall([
                    function(callback){
                        TimeoutResources.DeleteDivisionFinal({site:$scope.site,division_final_id:$scope.division_final_id},undefined,callback);
                    }],function(err,result){
                        Modals.loaded();
                        if (err == null){                            
                            $scope.resources[result.resource_name] = result;
                            $scope.division_final_id=undefined;                                                    
                        } else {                            
                            console.log(err);                            
                        }
                    }
                );
            };

            $scope.reopen_division_final_round = function(division_final_round_id){
                Modals.loading();                
                async.waterfall([
                    function(callback){
                        TimeoutResources.ReopenDivisionFinalRound({site:$scope.site,division_final_round_id:division_final_round_id},undefined,callback);
                    },
                    function(result,callback){                    
                        TimeoutResources.CheckDivisionFinalExist({site:$scope.site,division_id:$scope.division_id},undefined,callback);                        
                    }
                ],function(err,result){
                        Modals.loaded();
                        if (err == null){                            
                            $scope.resources[result.resource_name] = result;
                        } else {
                            Modals.loaded();
                            console.log(err);
                        }
                    }
                );
            };
            
            $scope.initialize_division_final = function(){
                Modals.loading();                
                async.waterfall([
                    function(callback){
                        TimeoutResources.InitializeDivisionFinal({site:$scope.site,division_id:$scope.division_id},{},callback);
                    },
                    function(result, callback){
                        $scope.resources[result.resource_name] = result;
                        $scope.division_final_id=$scope.resources['division_final'].data.division_final_id;                                            
                        TimeoutResources.GetDivisionFinalTiebreakers({site:$scope.site,division_final_id:$scope.division_final_id},undefined,callback);
                    },
                    function(result, callback){
                        $scope.resources[result.resource_name] = result;
                        TimeoutResources.GetDivisionFinalImportantTiebreakerRanks({site:$scope.site,division_final_id:$scope.division_final_id},undefined,callback);
                    }
                ],function(err,result){
                    Modals.loaded();
                    if (err == null){
                        $scope.resources[result.resource_name] = result;
                        $scope.number_important_tiebreakers = Object.keys($scope.resources.division_final_important_tiebreaker_ranks.data.important_tiebreakers).length;
                        
                    } else {
                        console.log(err);                                
                    }
                });
            };
            
            $scope.site=$state.params.site;
	    $scope.division_id=$state.params.division_id;
	    $scope.division_final_id=undefined;

            if($scope.resources==undefined){
                $scope.resources = {};
            }            
            $scope.division_final_id=undefined;
            $scope.utils = Utils;
            Modals.loading();
            async.waterfall([
                function(callback){                    
                    TimeoutResources.GetDivisionsEx({site:$scope.site},undefined,callback);
                },
                function(result,callback){
                    $scope.resources[result.resource_name] = result;                                        
                    TimeoutResources.CheckDivisionFinalExist({site:$scope.site,division_id:$scope.division_id},undefined,callback);
                    
                },
                function(result,callback){                    
                    $scope.resources[result.resource_name] = result;                    
                    if($scope.resources[result.resource_name].data == null){
                        callback('no division final to load',null);
                        return;
                    }
                    $scope.division_final_id=$scope.resources['division_final'].data.division_final_id;                    
                    TimeoutResources.GetDivisionFinalRoundCount({site:$scope.site,division_final_id:$scope.division_final_id},undefined,callback);
                },
                function(result,callback){
                    $scope.resources[result.resource_name] = result;
                    if($scope.resources[result.resource_name].data != undefined){                        
                        callback('rounds already here',null);
                        return;
                    }                                                            
                    TimeoutResources.GetDivisionFinalTiebreakers({site:$scope.site,division_final_id:$scope.division_final_id},undefined,callback);                    
                },                
                function(result,callback){                    
                    $scope.resources[result.resource_name] = result;
                    if($scope.resources[result.resource_name].data.tiebreakers.length == 0){
                        callback('no tiebreakers to load',null);
                        return;
                    }                    
                    TimeoutResources.GetDivisionFinalImportantTiebreakerRanks({site:$scope.site,division_final_id:$scope.division_final_id},undefined,callback);
                    //callback(null,result);
                }                                
            ],function(err,result){
                Modals.loaded();
                if (err == null){
                    $scope.resources[result.resource_name] = result;
                    $scope.number_important_tiebreakers = Object.keys($scope.resources.division_final_important_tiebreaker_ranks.data.important_tiebreakers).length;
                    //$scope.resources = Utils.extract_results_from_response(result);
                    console.log($scope.resources);
                } else {
                    console.log(err);                                
                }
            });
            //$scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
             
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
