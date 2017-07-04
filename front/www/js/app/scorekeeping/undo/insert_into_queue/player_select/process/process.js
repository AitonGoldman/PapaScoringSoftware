angular.module('app.scorekeeping.undo.insert_into_queue.player_select.process',[/*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.undo.insert_into_queue.player_select.process').controller(
    'app.scorekeeping.undo.insert_into_queue.player_select.process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
	$scope.division_machine_id=$state.params.division_machine_id;
        
        $scope.player_id_to_add=$state.params.player_id_to_add;
        $scope.resources={};
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        
     
        Modals.loading();
        //audit_log_promise = TimeoutResources.GetAuditLogMissingTokensEx({site:$scope.site,player_id:$scope.player_id},{},$scope.resources);                 
        insert_promise  = TimeoutResources.InsertPlayerIntoQueueEx({site:$scope.site,player_id:$scope.player_id_to_add,division_machine_id:$scope.division_machine_id},{},$scope.resources);
        insert_promise.then(function(data){            
            Modals.loaded();
        });
    }]
);
