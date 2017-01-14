angular.module('app.queues.machine_select.machine_queue.player_select.confirm.process',[/*REPLACEMECHILD*/]);
angular.module('app.queues.machine_select.machine_queue.player_select.confirm.process').controller(
    'app.queues.machine_select.machine_queue.player_select.confirm.process',[
        '$scope','$state','TimeoutResources','Utils','Modals','User',
        function($scope, $state, TimeoutResources, Utils,Modals,User) {
        $scope.site=$state.params.site;
	$scope.division_machine_id=$state.params.division_machine_id;
	$scope.division_machine_name=$state.params.division_machine_name;
	$scope.division_id=$state.params.division_id;
        $scope.player_id = $state.params.player_id;
        $scope.player_name = $state.params.player_name;

        if(User.logged_in() == true && User.logged_in_user().player_id != undefined){
            $scope.player_id=User.logged_in_user().player_id;
            $scope.player_name=User.logged_in_user().first_name+" "+User.logged_in_user().last_name;
        }    
        
        
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        
        add_to_queue_promise = TimeoutResources.AddToQueue($scope.bootstrap_promise,{site:$scope.site},{division_machine_id:$scope.division_machine_id,player_id:$scope.player_id});
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        add_to_queue_promise.then(function(data){
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
