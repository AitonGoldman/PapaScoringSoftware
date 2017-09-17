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
                var basic_sref='.edit_meta_tournament_basic({id:item.meta_tournament_id})';
                var advanced_sref='.edit_meta_tournament_advanced({id:item.meta_tournament_id})';
                var wizard_sref='.edit_meta_tournament_wizard({id:item.meta_tournament_id,wizard_step:1})';
                set_list_items_actions_and_args=listGeneration.generate_set_list_items_actions_and_args('meta_tournament_name',
                                                                                                        advanced_sref,
                                                                                                        wizard_sref,
                                                                                                        basic_sref,
                                                                                                        true
                                                                                                       );                
                _.map(meta_tournament_items, set_list_items_actions_and_args);
                $scope.meta_tournament_items = meta_tournament_items;
                //$scope.items=$scope.items.concat(meta_tournament_items);
                
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
                if($scope.tournament["finals_style"]=="MULTI"){
                    create_multi_division_tournament_func(tournament);
                } else {
                    create_normal_tournament_func(tournament);
                }                
            };
            var create_multi_division_tournament_func = function(tournament){
                var on_success = function(data){

                    $scope.post_results={};
                    $scope.post_results.title="Tournament Created!";
                    //FIXME : this should use descriptions we got from backend
                    var results = [];
                    
                    
                    var item = data['multi_division_tournament'];
                    results.push(["name",item["multi_division_tournament_name"]]);
                    results.push(["type","Multi Division"]);
                    $scope.post_results.results=results;                    
                    $scope.disable_back_button();
                    $scope.post_success = true;                        

                };
                var post_object = {multi_division_tournament_name:$scope.tournament.tournament_name,
                                   number_of_divisions:$scope.tournament.number_of_divisions};
                var prom = resourceWrapperService.get_wrapper_with_loading('post_create_multi_division_tournament',
                                                                       on_success,{event_name:$scope.event_name},
                                                                       post_object);
                
            };
            var create_normal_tournament_func = function(tournament){                                
                var on_success = function(data){                    
                    $scope.post_results={};
                    $scope.post_results.title="Tournament Created!";
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
                    results.push(["type",description]);                                        
                    $scope.post_results.results=results;                    
                    $scope.disable_back_button();
                    $scope.post_success = true;
                };                
                var prom = resourceWrapperService.get_wrapper_with_loading('post_create_tournament',
                                                                           on_success,
                                                                           {event_name:$scope.event_name},
                                                                           $scope.tournament);
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
                    $scope.post_results.results=[['MetaTournament Name',
                                                  data['new_meta_tournament'].meta_tournament_name]];                    
                    $scope.post_success = true;
                    $scope.disable_back_button();
                };
                                
                var prom_meta_tournament = resourceWrapperService.get_wrapper_with_loading('post_create_meta_tournament',
                                                                                           on_success,
                                                                                           {event_name:$scope.event_name},
                                                                                           $scope.meta_tournament);            

            };
            var prom_tournaments = resourceWrapperService.get_wrapper_with_loading('get_tournaments',
                                                                                   function(data){$scope.tournaments=data['tournaments'];},
                                                                                   {event_name:$scope.event_name},
                                                                                   {});                                    
        }
    ]);

angular.module('event').controller(
    'app.event.select_players_to_add_to_event_controller',[
        '$scope','$state','resourceWrapperService','listGeneration','eventTournamentLib',
        function($scope, $state,resourceWrapperService,listGeneration,eventTournamentLib) {
            $scope.bootstrap({back_button:true});
            $scope.toggle_view_item_actions = listGeneration.toggle_view_item_actions;

            // var generate_player_list_items_actions_and_args = function(display_label_field,advanced_sref,wizard_sref,basic_sref) {
            //     var player_list_items_actions_and_args = function(i) {                                     
            //         i.actions_ui_sref_list = [{label:"Advanced Editing",ui_sref:advanced_sref}];
            //         if(i.wizard_configured == false){
            //             basic_edit_action = {label:"Wizard Configuration",ui_sref:wizard_sref};
            //         } else {
            //             basic_edit_action = {label:"Basic Editing",ui_sref:basic_sref};
            //         }
            //         i.actions_ui_sref_list.splice(0,0,basic_edit_action);
            //         i.actions_ng_click_list=[{label:"Toggle active",ng_click:'toggle_item_active(item,event_name)'}];
            //         i.label_to_display=i[display_label_field];
                    
            //     };             
            //     return player_list_items_actions_and_args;
            // };
            // var basic_sref='.edit_tournament_basic({id:item.tournament_id})';
            // var advanced_sref='.edit_tournament_advanced({id:item.tournament_id})';
            // var wizard_sref='.edit_tournament_wizard({id:item.tournament_id,wizard_step:1})';
            // var player_list_items_actions_and_args=generate_player_list_items_actions_and_args('player_name',
            //                                                                                    advanced_sref,
            //                                                                                    wizard_sref,
            //                                                                                    basic_sref
            //                                                                                   );
            var set_list_items_ui_sref_and_args = listGeneration.generate_set_list_items_ui_sref_and_args(".add_existing_player_to_event({player_id:item.player_id})","player_name");

            var on_success = function(data){
                var raw_items=data['existing_players'];
                $scope.items = _.filter(raw_items, function(n) {
                    if(n.event_player){
                        return false;
                    };
                    return true;
                });                
                _.map($scope.items, set_list_items_ui_sref_and_args);
            };                        
            var prom =resourceWrapperService.get_wrapper_with_loading('get_players',on_success,{event_name:$scope.event_name},{});                        
        }]);

angular.module('event').controller(
    'app.event.select_players_to_add_to_event.add_players_to_event_controller',[
        '$scope','$state','resourceWrapperService','listGeneration','eventTournamentLib','$ionicPopup',
        function($scope, $state,resourceWrapperService,listGeneration,eventTournamentLib,$ionicPopup) {
            $scope.bootstrap({back_button:true});            
            
            $scope.disable_submit = function(){
                if($scope.event && $scope.event.force_ifpa_lookup==true){
                    if($scope.player.ifpa_ranking==undefined || $scope.player.ifpa_ranking==""){
                        return true;
                    }
                }
                if($scope.tournaments && $scope.tournaments.length>0){
                    if($scope.player.multi_division_tournament_id == undefined){
                        return true;
                    }
                }
                return false;
            };
            
            $scope.showAlert = function() {
                var alertPopup = $ionicPopup.alert({
                    title: 'Not Found',
                    template: 'Player not in IFPA rankings.'                    
                });

                alertPopup.then(function(res) {
                    
                });
            };
            $scope.showConfirm = function() {
                var confirmPopup = $ionicPopup.confirm({
                    title: 'Consume Ice Cream',
                    templateUrl: 'templates/ifpa_select.html',
                    scope:$scope
                });

                confirmPopup.then(function(res) {
                    if(res) {
                        var idx = $scope.ifpa_popup.multi_ifpa_ranking_index;                        
                        $scope.player.ifpa_ranking=$scope.ifpa_rankings[idx].wppr_rank;
                        $scope.player.ifpa_id=$scope.ifpa_rankings[idx].player_id;
                    } else {                        
                    }
                });
            };            
            $scope.get_ifpa_ranking = function(){
                var on_ifpa_success = function(data){
                    if(data.ifpa_ranking.search.length==0){
                        $scope.player.ifpa_ranking='not ranked';
                        $scope.showAlert();
                    }                    
                    if(data.ifpa_ranking.search.length==1){
                        $scope.player.ifpa_ranking=data.ifpa_ranking.search[0].wppr_rank;                        
                        $scope.player.ifpa_id=data.ifpa_ranking.search[0].player_id;
                    }
                    if(data.ifpa_ranking.search.length > 1){                        
                        $scope.ifpa_rankings=data.ifpa_ranking.search;                        
                        $scope.showConfirm();
                    }
                };
                var player_name=$scope.player.first_name+" "+$scope.player.last_name;
                var prom =resourceWrapperService.get_wrapper_with_loading('get_ifpa_ranking',on_ifpa_success,{event_name:$state.params.event_name,player_name:player_name},{});                            
            };
            $scope.create_player_func = function(player_id){                
                var on_create_success = function(data){                    
                    // $scope.logged_in_user=data['new_event'];                    
                    $scope.post_results={};
                    $scope.post_results.title="Player Added To Event!";
                    $scope.post_results.results=[];
                    var player_name=data['new_player'].first_name+" "+data['new_player'].last_name;
                    if(data['new_player'].extra_title!=undefined){
                        player_name=player_name+" "+data['new_player'].extra_title;
                    }
                    $scope.post_results.results.push(['Player Name',player_name]);                    
                    $scope.post_results.results.push(['Player Pin',data['new_player']['event_player']['event_player_pin']]);                                        
                    $scope.disable_back_button();
                    $scope.post_success = true;
                    
                };
                if($scope.player.ifpa_ranking=="not ranked"){
                    $scope.player.ifpa_ranking="9999999";
                }                
                if(player_id==undefined){
                    var prom =resourceWrapperService.get_wrapper_with_loading('post_create_player',on_create_success,{event_name:$state.params.event_name},$scope.player);
                } else {
                    var prom2 =resourceWrapperService.get_wrapper_with_loading('put_add_player',on_create_success,{event_name:$state.params.event_name},$scope.player);                    
                }
                

            };

            var on_player_load_success = function(data){                                
                if(data['existing_player']){
                    $scope.player = data['existing_player'];
                }
                
            };
            
            var on_success = function(data){
                $scope.tournaments = data['multi_division_tournaments'];
                $scope.event = data['event'];
            };
            $scope.player = {};
            if($state.params.player_id!=undefined){                                
                //FIXME : get_wrapper_with_loading() can not run concurrently - due to ionicloading promises
                var prom2 = resourceWrapperService.get_wrapper_without_loading('get_player',on_player_load_success,{player_id:$state.params.player_id},{});
            } 
            var prom =resourceWrapperService.get_wrapper_with_loading('get_multi_division_tournaments',on_success,{event_name:$scope.event_name},{});                                    
            $scope.ifpa_popup = {};
            
            
        }]);
