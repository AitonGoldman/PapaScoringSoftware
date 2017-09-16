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
                //$scope.items=data['tournaments'];
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
                var meta_tournament_items=data['meta_tournaments'];
                var basic_meta_sref='.edit_meta_tournament_basic({id:item.meta_tournament_id})';
                var set_list_items_srefs=listGeneration.generate_set_list_items_ui_sref_and_args(basic_meta_sref,
                                                                                                 'meta_tournament_name'
                                                                                                );                
                _.map(meta_tournament_items, set_list_items_srefs);

                console.log($scope.items);
                $scope.items=$scope.items.concat(meta_tournament_items);
                console.log($scope.items);
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
                    $scope.post_results.title="Tournament Created!";
                    //FIXME : this should use descriptions we got from backend
                    var results = [];
                    
                    var item;
                    if(data['new_tournament']==undefined){
                        item = data['multi_division_tournament'];
                        results.push(["name",item["multi_division_tournament_name"]]);
                        $scope.post_results.results=results;                    
                        $scope.disable_back_button();
                        $scope.post_success = true;                        
                        return;
                    }

                    item = data['new_tournament'];                    
                    
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
                var prom;
                if($scope.tournament["finals_style"]=="MULTI"){
                    prom = resourceWrapperService.get_wrapper_with_loading('post_create_multi_division_tournament',
                                                                           on_success,{event_name:$scope.event_name},
                                                                           {multi_division_tournament_name:$scope.tournament.tournament_name,number_of_divisions:$scope.tournament.number_of_divisions});
                }else{
                    prom = resourceWrapperService.get_wrapper_with_loading('post_create_tournament',on_success,{event_name:$scope.event_name},$scope.tournament);
                }
                
                
            
            };
        }]);

angular.module('event').controller(
    'app.event.manage_tournaments.create_meta_tournament_controller',[
        '$scope','$state','resourceWrapperService','credentialsService','$ionicNavBarDelegate','$rootScope',
        function($scope, $state,resourceWrapperService,credentialsService,$ionicNavBarDelegate,$rootScope ) {            
            $scope.bootstrap({back_button:true});            
            $scope.meta_tournament={tournament_ids:{}};            
            $scope.create_meta_tournament_func = function(){                
                var on_success = function(data){
                    $scope.new_meta_tournament=data['new_meta_tournament'];
                    $scope.post_results={};
                    $scope.post_results.title="MetaTournamet created!";
                    $scope.post_results.results=[['MetaTournament Name',data['new_meta_tournament'].meta_tournament_name]];                    
                    $scope.post_success = true;
                    $scope.disable_back_button();
                };
                                
                var prom_meta_tournament = resourceWrapperService.get_wrapper_with_loading('post_create_meta_tournament',on_success,{event_name:$scope.event_name},$scope.meta_tournament);            

            };
            var prom_tournaments = resourceWrapperService.get_wrapper_with_loading('get_tournaments',function(data){$scope.tournaments=data['tournaments'];},{event_name:$scope.event_name},{});                                    
        }
    ]);
