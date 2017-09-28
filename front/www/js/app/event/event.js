angular.module('event',[]);
angular.module('event').controller(
    'app.event_controller',[
        '$scope','$state','resourceWrapperService','listGeneration',
        function($scope, $state,resourceWrapperService,listGeneration ) {
            $scope.bootstrap({back_button:true});
            $scope.check_for_hiding_based_on_wizard();            
            $scope.wizard_mode_pop();                            
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
                    //$scope.post_results={};
                    //$scope.post_results.title="Logged In!";
                    //$scope.post_results.results=[['User Name',data['pss_user'].username]];
                    //$scope.post_success = true;
                    //$scope.disable_back_button();
                    $scope.post_success_handler("Logged In!",[['User Name',data['pss_user'].username]],$scope);
                    
                };
                                
                var prom =resourceWrapperService.get_wrapper_with_loading('post_event_login',on_success,{event_name:$scope.event_name},{username:$scope.pss_user.username,password:$scope.pss_user.password});            

            };
        }
    ]);

angular.module('event').controller(
    'app.event.manage_tournaments_controller',[
        '$scope','$state','resourceWrapperService','listGeneration','eventTournamentLib','$cookies',
        function($scope, $state,resourceWrapperService,listGeneration,eventTournamentLib,$cookies) {
            $scope.bootstrap({back_button:true});
            $scope.check_for_hiding_based_on_wizard();            
            $scope.toggle_view_item_actions = listGeneration.toggle_view_item_actions;
            $scope.toggle_item_active=eventTournamentLib.toggle_item_active;                
            var on_success = function(data){
                //$scope.items=data['tournaments'];
                $scope.items=data['tournaments'];
                $scope.wizard_mode_pop();                                
                var wizard_mode = $cookies.get('wizard_mode');
                if($state.current.name=='app.event.manage_tournaments' && wizard_mode == '3' && $scope.items.length==1 && $scope.items[0].tournament_machines.length > 0){
                    $scope.pop("all done");
                }

                var basic_sref='.edit_tournament_basic({id:item.tournament_id})';
                var advanced_sref='.edit_tournament_advanced({id:item.tournament_id})';                
                var set_list_items_actions_and_args=listGeneration.generate_set_list_items_actions_and_args('tournament_name',
                                                                                                            advanced_sref,
                                                                                                            basic_sref
                                                                                                           );                
                _.map($scope.items, set_list_items_actions_and_args);
                _.map($scope.items, listGeneration.set_add_machine_action);
                _.map($scope.items, listGeneration.set_active_inactive_icon);

                var meta_tournament_items=data['meta_tournaments'];
                basic_sref='.edit_meta_tournament_basic({id:item.meta_tournament_id})';
                advanced_sref='.edit_meta_tournament_advanced({id:item.meta_tournament_id})';                
                set_list_items_actions_and_args=listGeneration.generate_set_list_items_actions_and_args('meta_tournament_name',
                                                                                                        advanced_sref,
                                                                                                        basic_sref,
                                                                                                        false
                                                                                                       );                
                _.map(meta_tournament_items, set_list_items_actions_and_args);
                $scope.meta_tournament_items = meta_tournament_items;                
                
            };                        
            var prom =resourceWrapperService.get_wrapper_with_loading('get_tournaments',on_success,{event_name:$scope.event_name},{});                        
        }]);

angular.module('event').controller(
    'app.event.manage_tournament_machines_controller',[
        '$scope','$state','resourceWrapperService','listGeneration','eventTournamentLib','$timeout','$ionicActionSheet',
        function($scope, $state,resourceWrapperService,listGeneration,eventTournamentLib,$timeout,$ionicActionSheet) {            
            $scope.bootstrap();
            $scope.toggle_view_item_actions = listGeneration.toggle_view_item_actions;
                       
            $scope.remove_item = function(item){
            var hideSheet = $ionicActionSheet.show({
                destructiveText: 'Remove Machine',
                titleText: 'Are you SURE you want to remove this machine?',
                cancelText: 'Cancel',
                cancel: function() {
                    // add cancel code..
                },
                buttonClicked: function(index) {                    
                    return true;
                },
                destructiveButtonClicked: function(index){
                    eventTournamentLib.remove_item(item,$state.params.event_name);
                    hideSheet();
                }
            });

            };
            
            var on_success = function(data){                
                $scope.items=data['tournaments'];
                $scope.toggle_item_active=eventTournamentLib.toggle_item_active;                
                _.forEach($scope.items, function(tournament) {
                    _.map(tournament.tournament_machines, listGeneration.generate_tournament_machine_actions('tournament_machine_name'));                    
                    _.map(tournament.tournament_machines,function(i){i.actions_ui_sref_list=[];});
                    _.map(tournament.tournament_machines, listGeneration.set_active_inactive_icon);
                    tournament.tournament_machines = _.filter(tournament.tournament_machines, function(o) { return o.removed!=true; });

                });                                
            };                        
            var prom =resourceWrapperService.get_wrapper_with_loading('get_tournaments',on_success,{event_name:$scope.event_name},{});                        
        }]);

angular.module('event').controller(
    'app.event.manage_tournament_machines.add_tournament_machine_controller',[
        '$scope','$state','resourceWrapperService','listGeneration','eventTournamentLib','$cookies',
        function($scope, $state,resourceWrapperService,listGeneration,eventTournamentLib,$cookies) {
            $scope.bootstrap();            
            $scope.tournament_machines={tournament_id:$state.params.tournament_id};            
            $scope.add_machine_func = function(){                
                var filtered_values =  _.filter($scope.items, function(item) {                                
                    if(item.checked==true){                    
                         return true;
                     }                        
                    return false;
                });

                $scope.tournament_machines.tournament_machines=filtered_values;
                
                var on_submit_success = function(data){                    
                    $scope.item=data['item'];
                    //$scope.post_results={};
                    //$scope.post_results.title="Machines Added!";                    
                    //$scope.post_results.results=[];
                    var results = [];
                    _.forEach(filtered_values, function(machine) {
                        results.push(["Machine Name",machine.machine_name]);
                    });
                    $scope.post_success_handler("Machines Added!",results,$scope);
                    if(parseInt($cookies.get('wizard_mode'))<555){
                        $cookies.put('wizard_mode','555');
                    }
                    

                    //$scope.post_success = true;
                    //$scope.disable_back_button();
                    
                };                        
                var prom =resourceWrapperService.get_wrapper_with_loading('post_add_tournament_machines',
                                                                          on_submit_success,
                                                                          {event_name:$scope.event_name},
                                                                          $scope.tournament_machines);                        

            };
            var on_get_success = function(data){                
                $scope.items = data['machines'];                
            };
            var prom =resourceWrapperService.get_wrapper_with_loading('get_machines',on_get_success,{event_name:$scope.event_name},{});                        

        }]);

angular.module('event').controller(
    'app.event.manage_tournaments.create_tournament_controller',[
        '$scope','$state','resourceWrapperService','listGeneration',
        function($scope, $state,resourceWrapperService,listGeneration ) {
            $scope.bootstrap({back_button:true});
            $scope.item={};
            $scope.state = $state.current.name;
            if($scope.state == "app.event.quick_create_tournament"){                
                $scope.item.active=true;
            }
            $scope.create_tournament_func = function(tournament){
                if($scope.item["finals_style"]=="MULTI"){
                    create_multi_division_tournament_func(tournament);
                } else {
                    create_normal_tournament_func(tournament);
                }                
            };
            var create_multi_division_tournament_func = function(tournament){
                var on_success = function(data){

                    //$scope.post_results={};
                    //$scope.post_results.title="Tournament Created!";
                    //FIXME : this should use descriptions we got from backend
                    var results = [];
                    var item = data['multi_division_tournament'];
                    results.push(["name",item["multi_division_tournament_name"]]);
                    results.push(["type","Multi Division"]);
                    //$scope.post_results.results=results;                    
                    //$scope.disable_back_button();
                    //$scope.post_success = true;                        
                    $scope.post_success_handler("Tournament Created!",results,$scope);

                };
                var post_object = {multi_division_tournament_name:$scope.item.tournament_name,
                                   number_of_divisions:$scope.item.number_of_divisions};
                var prom = resourceWrapperService.get_wrapper_with_loading('post_create_multi_division_tournament',
                                                                       on_success,{event_name:$scope.event_name},
                                                                       post_object);
                
            };
            var create_normal_tournament_func = function(tournament){                                
                var on_success = function(data){                    
                    //$scope.post_results={};
                    //$scope.post_results.title="Tournament Created!";
                    //FIXME : this should use descriptions we got from backend
                    var results = [];                                        
                    var item = data['new_tournament'];
                    $scope.tournament_id=item.tournament_id;
                    results.push(["name",item["tournament_name"]]);
                    var description;
                    if(item["finals_style"]=="PAPA"){
                        description="Single Division";
                    }
                    if(item["finals_style"]=="PPO"){
                        description="Single Division with A/B finals";
                    }
                    results.push(["type",description]);                                        
                    //$scope.post_results.results=results;                    
                    //$scope.disable_back_button();
                    //$scope.post_success = true;
                    $scope.post_success_handler("Tournament Created!",results,$scope);
                    
                };
                console.log($scope.item);
                var prom = resourceWrapperService.get_wrapper_with_loading('post_create_tournament',
                                                                           on_success,
                                                                           {event_name:$scope.event_name},
                                                                           $scope.item);
            };
            var on_get_success = function(data){
                $scope.descriptions=data['descriptions'];
            };                        
            var prom =resourceWrapperService.get_wrapper_with_loading('get_tournament_descriptions',on_get_success,{event_name:$state.params.event_name},{});                        

            
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
                    //$scope.post_results={};
                    //$scope.post_results.title="MetaTournamet created!";
                    var results=[['MetaTournament Name',
                                  data['new_meta_tournament'].meta_tournament_name]];                    
                    //$scope.post_success = true;
                    //$scope.disable_back_button();
                    $scope.post_success_handler("MetaTournament Created!",results,$scope);
                    
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
                console.log($scope.items);
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
                    //$scope.post_results={};
                    //$scope.post_results.title="Player Added To Event!";
                    //$scope.post_results.results=[];
                    var results = [];
                    $scope.player=data['new_player'];
                    var player_name=data['new_player'].first_name+" "+data['new_player'].last_name;
                    if(data['new_player'].extra_title!=undefined){
                        player_name=player_name+" "+data['new_player'].extra_title;
                    }
                    results.push(['Player Name',player_name]);
                    results.push(['Player Number',data['new_player']['event_player']['event_player_id']]);
                    results.push(['Player Pin',data['new_player']['event_player']['event_player_pin']]);
                    //$scope.disable_back_button();
                    //$scope.post_success = true;
                    $scope.post_success_handler("Player Added To Event!",results,$scope);

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

angular.module('event').controller(
    'app.event.token_purchase_controller',[
        '$scope','$state','resourceWrapperService','credentialsService','$ionicNavBarDelegate','$rootScope','$filter',
        function($scope, $state,resourceWrapperService,credentialsService,$ionicNavBarDelegate,$rootScope,$filter ) {                        
            $scope.bootstrap({back_button:true});                        
            $scope.total_cost=0;
            $scope.filter_for={};
            $scope.filtered_player={};
            //$scope.player_id = $state.params.player_id;
            $scope.on_ticket_change = function(){                
                $scope.total_cost=0;
                _.map($scope.token_info.tournament_ticket_prices, function(i){
                    if(i.purchase!=undefined){
                        $scope.total_cost=$scope.total_cost+i.purchase.price;                        
                    }
                });
                _.map($scope.token_info.meta_tournament_ticket_prices, function(i){
                    if(i.purchase!=undefined){
                        $scope.total_cost=$scope.total_cost+i.purchase.price;
                    }
                });

            };
            $scope.on_change = function(){
                $scope.token_info_gotten=undefined;
                var filtered_players = _.filter($scope.players,function(p){
                    if(parseInt(p.event_player.event_player_id) == parseInt($scope.filter_for.filter_for)){
                        return true;
                    } else {
                        return false;
                    }
                });
                if(filtered_players.length==1){
                    $scope.filtered_player=filtered_players[0];
                }
                if(filtered_players.length==0){
                    $scope.filtered_player={};
                } 
                
            };
            $scope.purchase = function(){                
                var on_post_success = function(data){
                    //$scope.post_results={};
                    //$scope.post_results.title="Tickets Purchased!";
                    //$scope.post_results.results=[];                    
                    var results = [];
                    var total_purchase_cost = 0;
                    _.forEach(data.purchase_summary,function(i){
                        if(i[2].amount==undefined){
                            return;
                        }
                        total_purchase_cost=total_purchase_cost+i[2].price;
                        results.push([i[0],i[2].amount+" : $"+i[2].price]);
                    });
                    results.push(["Total Cost","$"+total_purchase_cost]);
                    //$scope.post_success = true;
                    $scope.post_success_handler("Tickets Purchased!",results,$scope);
                };                
                var token_purchases={'tournament_token_counts':[],
                                     'meta_tournament_token_counts':[]};
                _.map($scope.token_info.tournament_ticket_prices, function(i){
                    if(i.purchase!=undefined){
                        token_purchases.tournament_token_counts.push({token_count:i.purchase.amount,tournament_id:i.tournament_id});                        
                    }
                });
                _.map($scope.token_info.meta_tournament_ticket_prices, function(i){
                    if(i.purchase!=undefined){
                        token_purchases.meta_tournament_token_counts.push({token_count:i.purchase.amount,meta_tournament_id:i.meta_tournament_id});                        
                    }
                });                

                var purchase_token_prom = resourceWrapperService.get_wrapper_with_loading('post_token_purchase_desk',
                                                                                          on_post_success,
                                                                                          {event_name:$scope.event_name,player_id:$scope.filtered_player.player_id},
                                                                                          token_purchases);            
                
            };
            $scope.get_token_info_for_player_func = function(){
                var on_get_success = function(data){
                    $scope.token_info=data;
                    $scope.token_info_gotten=true;
                    
                };
                var get_token_info_prom = resourceWrapperService.get_wrapper_with_loading('get_token_info_for_player',
                                                                                          on_get_success,
                                                                                          {event_name:$scope.event_name,player_id:$scope.filtered_player.player_id},
                                                                                          {});            
                
            };
            $scope.purchase_tokens_func = function(){                
                                
                // var purchase_prom = resourceWrapperService.get_wrapper_with_loading('post_purchase_tokens',
                //                                                                     on_post_success,
                //                                                                     {event_name:$scope.event_name,player_id:$scope.filtered_player.player_id},
                //                                                                     $scope.tokens);            

            };
            if($state.params.player.player_id!=undefined){
                $scope.filtered_player=$state.params.player;
                $scope.filtered_players=[$scope.filtered_player];
                $scope.get_token_info_for_player_func();                
            } else {
                var token_prom = resourceWrapperService.get_wrapper_with_loading('get_event_players',
                                                                                 function(data){$scope.players=data['existing_event_players'];},
                                                                                 {event_name:$scope.event_name},
                                                                                 {});                                    
            }

        }
    ]);

angular.module('event').controller(
    'app.event.player_info_controller',[
        '$scope','$state','resourceWrapperService','credentialsService','$ionicNavBarDelegate','$rootScope','$filter',
        function($scope, $state,resourceWrapperService,credentialsService,$ionicNavBarDelegate,$rootScope,$filter ) {                        
            $scope.bootstrap({back_button:true});                        
            $scope.get_player_info_func = function(player_id){                
                var on_get_success = function(data){
                    $scope.player_info=data['existing_player'];
                    $scope.player_selected=true;
                };
                var get_token_info_prom = resourceWrapperService.get_wrapper_with_loading('get_event_player',
                                                                                          on_get_success,
                                                                                          {event_name:$scope.event_name,player_id:player_id},
                                                                                          {});            
                
            };
            var token_prom = resourceWrapperService.get_wrapper_with_loading('get_event_players',
                                                                             function(data){$scope.players=data['existing_event_players'];},
                                                                             {event_name:$scope.event_name},
                                                                             {});                                    
        }
    ]);
