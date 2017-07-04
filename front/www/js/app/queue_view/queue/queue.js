angular.module('app.queue_view.queue',[/*REPLACEMECHILD*/]);
angular.module('app.queue_view.queue').controller(
    'app.queue_view.queue',[
        '$scope','$state','TimeoutResources','Utils','Modals','$timeout',
        function($scope, $state, TimeoutResources, Utils,Modals,$timeout) {
            $scope.site=$state.params.site;
	    $scope.division_id=$state.params.division_id;
            $scope.start_range = $state.params.start_range;
            $scope.end_range = $state.params.end_range;
            $scope.num_players_to_show = $state.params.num_players_to_show;
            if($scope.num_players_to_show == undefined || $scope.num_players_to_show == ""){
                $scope.num_players_to_show = 6;
            }
            $scope.game_1 = $state.params.game_1;
            $scope.game_2 = $state.params.game_2;
            $scope.game_3 = $state.params.game_3;
            $scope.game_4 = $state.params.game_4;
            $scope.game_5 = $state.params.game_5;
            $scope.game_6 = $state.params.game_6;
            $scope.game_7 = $state.params.game_7;
            $scope.game_8 = $state.params.game_8;
            $scope.game_9 = $state.params.game_9;
            $scope.game_10 = $state.params.game_10;
            $scope.game_11 = $state.params.game_11;
            $scope.game_12 = $state.params.game_12;
            $scope.game_13 = $state.params.game_13;        
            $scope.game_14 = $state.params.game_14;        
            $scope.game_15 = $state.params.game_15;        
            $scope.game_16 = $state.params.game_16;        
            
            $scope.columns = $state.params.columns;
            $scope.utils = Utils;
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);
            var get_queues = function(){
                queues_promise = TimeoutResources.GetCyclingQueues(undefined,{site:$scope.site,division_id:$scope.division_id});
                Modals.loading();
                // = TimeoutResources.GetEtcData();
                queues_promise.then(function(data){
                    if(data == undefined){
                        $timeout(get_queues,15000);                        
                    }
                    $scope.resources = TimeoutResources.GetAllResources();                    
                    $scope.flattened_queues = _.filter(_.values($scope.resources.queues.data), function(o) { return o.division_machine_id == $scope.game_1 || o.division_machine_id == $scope.game_2 || o.division_machine_id == $scope.game_3 || o.division_machine_id == $scope.game_4 || o.division_machine_id == $scope.game_5 || o.division_machine_id == $scope.game_6 || o.division_machine_id == $scope.game_7 || o.division_machine_id == $scope.game_8|| o.division_machine_id == $scope.game_9|| o.division_machine_id == $scope.game_10|| o.division_machine_id == $scope.game_11|| o.division_machine_id == $scope.game_12 || o.division_machine_id == $scope.game_13|| o.division_machine_id == $scope.game_14|| o.division_machine_id == $scope.game_15|| o.division_machine_id == $scope.game_16; });
                    $scope.machine_players=$scope.resources.queues.machine_players;
                    $scope.flattened_queues_concat=[];
                    $scope.row_size = Math.ceil($scope.flattened_queues.length/$scope.columns);
                    
                    rows_left = Math.ceil($scope.flattened_queues.length/$scope.row_size);
                    row_start = 0;
                    row_end = $scope.row_size;
                    for(x=rows_left;x>=0;x=x-1){                        
                        $scope.flattened_queues_concat.push(_.slice($scope.flattened_queues,row_start,row_end));
                        row_start=row_start+$scope.row_size;
                        row_end=row_start+$scope.row_size;
                    }
                    // $scope.flattened_queues_concat.push(_.slice($scope.flattened_queues,0,$scope.row_size));
                    // if($scope.columns == 2){                        
                    //     $scope.flattened_queues_concat.push(_.slice($scope.flattened_queues,$scope.row_size));
                    // } else {
                    
                    //     $scope.flattened_queues_concat.push(_.slice($scope.flattened_queues,$scope.row_size,$scope.row_size+$scope.row_size));
                    //     $scope.flattened_queues_concat.push(_.slice($scope.flattened_queues,$scope.row_size+$scope.row_size));                        
                    // }
                    
                    Modals.loaded();
                    
                    
                    if($state.current.name == 'app.queue_view.queue'){                        
                        $timeout(get_queues,15000);
                    }
                });             
            };
            get_queues();
            
            //Modals.loading();
            // = TimeoutResources.GetEtcData();
            //.then(function(data){
            // $scope.resources = TimeoutResources.GetAllResources();
            //  Modals.loaded();
            //})
        }]
);
