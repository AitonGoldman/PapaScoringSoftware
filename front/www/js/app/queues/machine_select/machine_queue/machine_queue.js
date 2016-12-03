angular.module('app.queues.machine_select.machine_queue',[
    'app.queues.machine_select.machine_queue.player_select'
    /*REPLACEMECHILD*/]);
angular.module('app.queues.machine_select.machine_queue').controller(
    'app.queues.machine_select.machine_queue',[
        '$scope','$state','TimeoutResources','Utils','Modals','ActionSheets','User',
        function($scope, $state, TimeoutResources, Utils,Modals,ActionSheets,User) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
	$scope.division_machine_id=$state.params.division_machine_id;
	$scope.division_machine_name=$state.params.division_machine_name;
        $scope.manage = $state.params.manage;
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                            
            $scope.bootstrap_promise.then(function(data){
                if(User.logged_in()==true){
                    $scope.logged_in_player_id = User.logged_in_user().player_id;
                }
                
            });
            
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
        remove_from_queue_function = function(player_id){
            Modals.loading();
            remove_promise = TimeoutResources.RemovePlayerFromQueue(undefined,{site:$scope.site,player_id:player_id});
            remove_promise.then(function(data){
                $scope.resources=TimeoutResources.GetAllResources();
                $scope.division_machine = $scope.resources.modified_queue.data[$scope.division_machine_id];                    
                Modals.loaded();
            });
        };
        
            $scope.choose_queue_action = function(player_id,player_name){
                ActionSheets.choose_queue_action(player_name,player_id, remove_from_queue_function);
            };
        queues_promise = TimeoutResources.GetQueues(undefined,{site:$scope.site,division_id:$scope.division_id});
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        queues_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();            
            $scope.division_machine = $scope.resources.queues.data[$scope.division_machine_id];                        
            Modals.loaded();            
        });             
    }]
);
