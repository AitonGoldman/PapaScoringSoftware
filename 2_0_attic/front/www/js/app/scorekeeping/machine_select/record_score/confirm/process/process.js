angular.module('app.scorekeeping.machine_select.record_score.confirm.process',['app.scorekeeping.machine_select.record_score.confirm.process.queue_add',
    /*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.machine_select.record_score.confirm.process').controller(
    'app.scorekeeping.machine_select.record_score.confirm.process',[
        '$scope','$state','TimeoutResources','Utils','Modals','$ionicHistory',
        function($scope, $state, TimeoutResources, Utils,Modals,$ionicHistory) {
            $ionicHistory.nextViewOptions({disableBack:true});            

            $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
	$scope.division_machine_name=$state.params.division_machine_name;
	$scope.division_machine_id=$state.params.division_machine_id;
            $scope.player_id = $state.params.player_id;
            $scope.team_id = $state.params.team_id;
            $scope.team_name = $state.params.team_name;
            
        $scope.player_name = $state.params.player_name;
	    //$scope.team_tournament=$state.params.team_tournament;            
            $scope.requeue = false;
            $scope.restarted = false;            
            $scope.show_redo=true;
            $scope.queue_args={queue_args:{division_machine_id:$scope.division_machine_id,division_machine_name:$scope.division_machine_name,team_tournament:false,previous_player_id:$scope.player_id,previous_player_name:$scope.player_name}};

        
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);        
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        
        $scope.confirmed_score=$state.params.confirmed_score;
        $scope.confirmed_score.score_with_commas = $scope.confirmed_score.score;
        $scope.confirmed_score.score = $scope.confirmed_score.score.replace(/,/g, '');
        queues_promise = TimeoutResources.GetQueues($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id});
        
        add_score_promise = TimeoutResources.AddScore(queues_promise,{site:$scope.site,division_machine_id:$scope.division_machine_id,score:$scope.confirmed_score.score});
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        add_score_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();            
            $scope.team_tournament=$scope.resources.divisions.data[$scope.division_id].team_tournament;            

            $scope.division_machine_queue_length = $scope.resources.queues.data[$scope.division_machine_id].queues.length;
            if($scope.division_machine_queue_length>0){                
                $scope.division_machine_queue_player = $scope.resources.queues.data[$scope.division_machine_id].queues[0].player.player_name;
            }
            

            if ($scope.resources.added_score.player_token_data == 0){
                delete $scope.queue_args.queue_args.previous_player_id;
                delete $scope.queue_args.queue_args.previous_player_name;
            }                
            
            Modals.loaded();
        });
            $scope.re_queue_player = function(){
                delete $scope.queue_args.queue_args.previous_player_id;
                delete $scope.queue_args.queue_args.previous_player_name;
                Modals.loading();
                add_to_queue_promise = TimeoutResources.AddToQueue(undefined,{site:$scope.site},{division_machine_id:$scope.division_machine_id,player_id:$scope.player_id});            
                add_to_queue_promise.then(function(data){
                    $scope.resources = TimeoutResources.GetAllResources();
                    $scope.show_redo=false;
                    $scope.requeue=true;
                    Modals.loaded();
                });                        
            };
            $scope.re_add_player = function(){
                delete $scope.queue_args.queue_args.previous_player_id;
                delete $scope.queue_args.queue_args.previous_player_name;
                
                $state.go('.^.^.^.player_select.process',{process_step:{process:true},player_info:{player_id:$scope.player_id,team_id:$scope.team_id},from_queue:0,division_machine_id:$scope.division_machine_id,division_machine_name:$scope.division_machine_name},{inherit:true});
            };                       
    }]
);
