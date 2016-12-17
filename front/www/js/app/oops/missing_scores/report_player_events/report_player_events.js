angular.module('app.oops.missing_scores.report_player_events',['app.oops.missing_scores.report_player_events.report_division_events',
    /*REPLACEMECHILD*/]);
angular.module('app.oops.missing_scores.report_player_events').controller(
    'app.oops.missing_scores.report_player_events',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.player_id=$state.params.player_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        audit_log_promise = TimeoutResources.GetAuditLogMissingTokens(undefined,{site:$scope.site,player_id:$scope.player_id});
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        audit_log_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });
             
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
