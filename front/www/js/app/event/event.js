angular.module('event',[]);
angular.module('event').controller(
    'app.event_controller',[
        '$scope','$state','resourceWrapperService','listGeneration',
        function($scope, $state,resourceWrapperService,listGeneration ) {
            $scope.bootstrap({back_button:true});            
        }]);

angular.module('event').controller(
    'app.event.login_controller',[
        '$scope','$state','resourceWrapperService','credentialsService','$ionicNavBarDelegate','$rootScope',
        function($scope, $state,resourceWrapperService,credentialsService,$ionicNavBarDelegate,$rootScope ) {            
            $scope.bootstrap({back_button:true});            
            $scope.pss_user={};            
            $scope.login_func = function(){                
                var on_success = function(data){
                    $scope.logged_in_user=data['pss_user'];
                    credentialsService.set_pss_user_credentials($scope.event_id,data);
                    $scope.post_results={};
                    $scope.post_results.title="Logged In!";
                    $scope.post_results.results=[['User Name',data['pss_user'].username]];                    
                    $scope.post_success = true;
                    $scope.disable_back_button();
                };
                                
                var prom =resourceWrapperService.get_wrapper_with_loading('post_event_login',on_success,{event_name:$scope.event_name},{username:$scope.pss_user.username,password:$scope.pss_user.password});            

            };
        }
    ]);

angular.module('event').controller(
    'app.event.manage_tournaments_controller',[
        '$scope','$state','resourceWrapperService','listGeneration','eventTournamentLib',
        function($scope, $state,resourceWrapperService,listGeneration,eventTournamentLib) {
            $scope.bootstrap({back_button:true});
            $scope.toggle_view_item_actions = listGeneration.toggle_view_item_actions;
            
            var on_success = function(data){
                $scope.items=data['tournaments'];                
                var basic_sref='.edit_tournament_basic({id:item.tournament_id})';
                var advanced_sref='.edit_tournament_advanced({id:item.tournament_id})';
                var wizard_sref='.edit_tournament_wizard({id:item.tournament_id,wizard_step:1})';
                var set_list_items_actions_and_args=listGeneration.generate_set_list_items_actions_and_args('tournament_name',
                                                                                                            advanced_sref,
                                                                                                            wizard_sref,
                                                                                                            basic_sref
                                                                                                           );                
                _.map($scope.items, set_list_items_actions_and_args);
                _.map($scope.items, listGeneration.set_active_inactive_icon);                
                $scope.toggle_item_active=eventTournamentLib.toggle_item_active;                
            };                        
            var prom =resourceWrapperService.get_wrapper_with_loading('get_tournaments',on_success,{event_name:$scope.event_name},{});                        
        }]);

angular.module('event').controller(
    'app.event.manage_tournaments.create_tournament_controller',[
        '$scope','$state','resourceWrapperService','listGeneration',
        function($scope, $state,resourceWrapperService,listGeneration ) {
            $scope.bootstrap({back_button:true});
            $scope.tournament={};

            $scope.create_tournament_func = function(tournament){                                
                var on_success = function(data){                    
                    $scope.post_results={};
                    $scope.post_results.title="Event Edited!";
                    //FIXME : this should use descriptions we got from backend
                    var results = [];
                    
                    var item = data['new_tournament'];                    
                    results.push(["name",item["tournament_name"]]);
                    var description;
                    if(item["finals_style"]=="PAPA"){
                        description="Single Division";
                    }
                    if(item["finals_style"]=="PPO"){
                        description="Single Division with A/B finals";
                    }
                    if(item["finals_style"]=="PAPA" && item["multi_division_tournament_id"]!=undefined ){
                        description="Muti Division";
                    }                    
                    results.push(["type",description]);                                        
                    $scope.post_results.results=results;                    
                    $scope.disable_back_button();
                    $scope.post_success = true;
                };                
                var prom =resourceWrapperService.get_wrapper_with_loading('post_create_tournament',on_success,{event_name:$scope.event_name},$scope.tournament);            
            
            };
        }]);
