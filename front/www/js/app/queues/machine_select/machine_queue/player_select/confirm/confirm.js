angular.module('app.queues.machine_select.machine_queue.player_select.confirm',['app.queues.machine_select.machine_queue.player_select.confirm.process',
    /*REPLACEMECHILD*/]);
angular.module('app.queues.machine_select.machine_queue.player_select.confirm').controller(
    'app.queues.machine_select.machine_queue.player_select.confirm',[
        '$scope','$state','TimeoutResources','Utils','Modals','User',
        function($scope, $state, TimeoutResources, Utils,Modals,User) {
            $scope.site=$state.params.site;
	    $scope.division_id=$state.params.division_id;
            $scope.division_machine_id=$state.params.division_machine_id;
	    $scope.division_machine_name=$state.params.division_machine_name;        
            $scope.player_id=$state.params.player_id;
            $scope.player_name = $state.params.player_name;
            $scope.utils = Utils;
            Modals.loading();
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                            
            $scope.bootstrap_promise.then(function(data){
                if(User.logged_in()==true){
                    $scope.logged_in_player_id = User.logged_in_user().player_id;
                }
                Modals.loaded();
            });
    }]
);
