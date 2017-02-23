angular.module('app.queues.machine_select.machine_queue',[
    'app.queues.machine_select.machine_queue.player_select',
    'app.queues.machine_select.machine_queue.add_other_player',
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
            $scope.User = User;
            Modals.loading();            
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                            
            queues_promise = TimeoutResources.GetQueues($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id});
            queues_promise.then(function(data){
                if(User.logged_in()==true && User.has_role('player')){                    
                    $scope.logged_in_player_id = User.logged_in_user().player.player_id;
                    $scope.logged_in_player_name = User.logged_in_user().player.first_name+" "+User.logged_in_user().player.last_name;
                }                
                $scope.resources = TimeoutResources.GetAllResources();            
                console.log($scope.resources);
                $scope.division_machine = $scope.resources.queues.data[$scope.division_machine_id];                        
                Modals.loaded();            
            });             
            
            remove_from_queue_function = function(player_id){
                Modals.loading();
                remove_promise = TimeoutResources.RemovePlayerFromQueue(undefined,{site:$scope.site,player_id:player_id});
                remove_promise.then(function(data){
                    $scope.resources=TimeoutResources.GetAllResources();
                    console.log($scope.resources.modified_queue.data);
                    $scope.division_machine = $scope.resources.modified_queue.data[$scope.division_machine_id];                    
                    Modals.loaded();
                });
            };
            
            $scope.choose_queue_action = function(player_id,player_name){
                ActionSheets.choose_queue_action(player_name,player_id, remove_from_queue_function);
            };
            $scope.doRefresh = function() {
                queues_promise = TimeoutResources.GetQueues($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id});
                queues_promise.then(function(data){
                    $scope.$broadcast('scroll.refreshComplete');
                    $scope.resources = TimeoutResources.GetAllResources();
                    $scope.division_machine = $scope.resources.queues.data[$scope.division_machine_id];
                });
            };                
            
    }]
);
