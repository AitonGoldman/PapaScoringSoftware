angular.module('app.generate_finals',[/*REPLACEMECHILD*/]);
angular.module('app.generate_finals').controller(
    'app.generate_finals',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;        
        $scope.papa_qualifiers = $state.params.papa_qualifiers;
        $scope.ppo_a_qualifiers = $state.params.ppo_a_qualifiers;
        $scope.ppo_b_qualifiers = $state.params.ppo_b_qualifiers;
        $scope.division_id = $state.params.division_id;
        $scope.formated_papa_division_qualifiers = [];
        $scope.formated_a_division_qualifiers = [];
        $scope.formated_b_division_qualifiers = [];
        
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                        
        $scope.resources = TimeoutResources.GetAllResources();
        $scope.team_tournament = $scope.resources.divisions.data[$scope.division_id].team_tournament == true;
        if(_.isEmpty($scope.ppo_a_qualifiers)){
            _.forEach($scope.papa_qualifiers, function(value) {
                if($scope.team_tournament){
                    $scope.formated_papa_division_qualifiers.push([value[1].team_id,value[0]+1]);
                } else {
                    $scope.formated_papa_division_qualifiers.push([value[1].player_id,value[0]+1]);
                }
                
                //$scope.players_present.data[value[1].player_id]=value[1];                
            });
            Modals.loading();
            finals_promise = TimeoutResources.CreateFinals($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id,extra_name_info:" "},$scope.formated_papa_division_qualifiers);                 finals_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                Modals.loaded();
            });                              
        }
        if(!_.isEmpty($scope.ppo_a_qualifiers)){
            
            _.forEach($scope.ppo_a_qualifiers, function(value) {
                $scope.formated_a_division_qualifiers.push([value[1].player_id,value[0]+1]);                
                //$scope.players_present.data[value[1].player_id]=value[1];                
            });
            max_a_idx = $scope.formated_a_division_qualifiers.length;
            _.forEach($scope.ppo_b_qualifiers, function(value) {
                $scope.formated_b_division_qualifiers.push([value[1].player_id,value[0]+1-max_a_idx]);                
                //$scope.players_present.data[value[1].player_id]=value[1];                
            });
            
            Modals.loading();
            finals_promise = TimeoutResources.CreateFinals($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id,extra_name_info:"A"},$scope.formated_a_division_qualifiers);        
            finals_promise_b = TimeoutResources.CreateFinals(finals_promise,{site:$scope.site,division_id:$scope.division_id,extra_name_info:"B"},$scope.formated_b_division_qualifiers);        
            finals_promise_b.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                Modals.loaded();
            });                
                        
            //console.log($scope.ppo_a_qualifiers);
        }
        
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
