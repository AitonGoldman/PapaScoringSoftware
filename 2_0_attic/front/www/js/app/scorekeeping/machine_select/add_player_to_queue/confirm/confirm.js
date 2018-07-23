angular.module('app.scorekeeping.machine_select.add_player_to_queue.confirm',['app.scorekeeping.machine_select.add_player_to_queue.confirm.process',
    /*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.machine_select.add_player_to_queue.confirm').controller(
    'app.scorekeeping.machine_select.add_player_to_queue.confirm',[
        '$scope','$state','TimeoutResources','Utils','Modals','User',
        function($scope, $state, TimeoutResources, Utils,Modals,User) {
        $scope.site=$state.params.site;
	$scope.division_machine_id=$state.params.division_machine_id;
	$scope.player_name=$state.params.player_name;
	$scope.division_machine_name=$state.params.division_machine_name;
	$scope.player_id=$state.params.player_id;
	$scope.division_id=$state.params.division_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        queue_promise = TimeoutResources.GetPlayerQueue($scope.bootstrap_promise,{site:$scope.site,player_id:$scope.player_id});
        token_promise = TimeoutResources.GetPlayerTokens(queue_promise,{site:$scope.site,player_id:$scope.player_id});
        token_promise.then(function(data){
            if(User.logged_in()==true){
                $scope.logged_in_player_id = User.logged_in_user().player_id;
            }
            $scope.resources = TimeoutResources.GetAllResources();
            if($scope.resources.divisions.data[$scope.division_id].meta_division_id != undefined){
                meta_division_id = $scope.resources.divisions.data[$scope.division_id].meta_division_id;
                $scope.num_tokens_left = $scope.resources.player_tokens.data.tokens.metadivisions[meta_division_id];                    
            } else {
                $scope.num_tokens_left = $scope.resources.player_tokens.data.tokens.divisions[$scope.division_id];                    
                
            }            
            console.log($scope.num_tokens_left);
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
