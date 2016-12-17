angular.module('app.oops.missing_scores.report_player_events.report_division_events',[/*REPLACEMECHILD*/]);
angular.module('app.oops.missing_scores.report_player_events.report_division_events').controller(
    'app.oops.missing_scores.report_player_events.report_division_events',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.player_id=$state.params.player_id;
	$scope.audit_log_id=$state.params.audit_log_id;
        $scope.audit_log={time_delta:15};
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        
        Modals.loading();
        audit_log_promise = TimeoutResources.GetAuditLogMissingScores(undefined,{site:$scope.site,player_id:$scope.player_id,audit_log_id:$scope.audit_log_id,time_delta:15});
        
        // = TimeoutResources.GetEtcData();
        audit_log_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });
        $scope.get_division_events = function(){
            Modals.loading();
            audit_log_promise = TimeoutResources.GetAuditLogMissingScores(undefined,{site:$scope.site,player_id:$scope.player_id,audit_log_id:$scope.audit_log_id,time_delta:15});
            audit_log_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                Modals.loaded();
            });            
        };
        
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
