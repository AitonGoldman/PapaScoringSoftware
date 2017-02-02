angular.module('TD_services.timeout_resources',
               ['ngResource']);
angular.module('TD_services.timeout_resources')
    .factory('TimeoutResources',
             ['$resource','$q',
              '$injector','Modals',
              'Utils','api_host'
              ,'$location',
              function($resource,
                       $q,
                       $injector,
                       Modals,
                       Utils,
                       api_host,
                       $location) {
                  var resource_results = {};
                  var reject_and_redirect = function(rejection,ui_route){
                      site = rejection.config.url.split('/')[3];
                      Modals.error(rejection.data.message,site,ui_route);
	              return $q.reject(rejection);
                  };
                  var generate_response_interceptor = function(custom_error){
                      if(custom_error == undefined){
                          ui_route='app';
                      } else {
                          ui_route=custom_error.ui_route;                          
                      }
                      var response_interceptor = {
	                  'responseError': function(rejection) {            
                              //FIXME : need error dialog to display
                              console.log('erroring out');
                              if(custom_error != undefined){
		                  rejection.data.message=custom_error.message;
                                  
                                  return reject_and_redirect(rejection,ui_route);
                              }
	                      if(rejection.status == -1){
                                  rejection.data = {};
		                  rejection.data.message="Can not perform action requested.  The server is unreachable.";
		                  rejection.data.debug="HTTP Timeout while getting<br>"+rejection.config.url;
	                      }
                              if(rejection.status == 400){                
                              }
                              if(rejection.status == 401){                
		                  rejection.data.message="You are not authroized to do this.";
                              }
                              if(rejection.status == 409){                
		                  rejection.data.debug="";
                              }
                              if(rejection.status == 500){                
		                  rejection.data.message="WHOAH!  Server puked.";
		                  rejection.data.debug="";
                              }
                              if(rejection.data.message == undefined){
                                  rejection.data.message="I have no earthly idea what the hell just happened.";
                              }
                              return reject_and_redirect(rejection,ui_route);
	                  }
                      };
                      return response_interceptor;

                  };
                  global_timeout = 15000;

                  
                  var execute_getdelete_resource = function(res,scope_name,args){
                      if(args == undefined){
	                  args={};
	              }
                      res=res['custom_http'];                
                      resource_results[scope_name] = res(args);
                      return resource_results[scope_name].$promise;	
                  };
                  
                  var execute_putpost_resource = function(res,scope_name,url_args,post_args){
                      
	              if(url_args == undefined){
	                  url_args={};
	              }
	              if(post_args == undefined){
	                  post_args={};
	              }        
                      new_res=res['custom_http'];                
                      resource_results[scope_name] = new_res(url_args, post_args);        
	              return resource_results[scope_name].$promise;	
                  };
                  
                  var generate_resource_definition = function(url,http_method,custom_interceptor_error,use_results_server){                                                    
                      url_chunks = url.split("/");
                      gen_post_args = {};
                      for(url_chunk_index in url_chunks){
                          url_chunk = url_chunks[url_chunk_index];
                          if(url_chunk.indexOf(':')>=0){
                              arg_name = url_chunk.substr(1);
                              gen_post_args[arg_name]='@'+arg_name;
                          };
                      }
                      response_interceptor_to_use = undefined;
                      if(custom_interceptor_error == undefined){
                          //response_interceptor_to_use = response_interceptor;
                          response_interceptor_to_use = generate_response_interceptor();
                      } else {
                          response_interceptor_to_use = generate_response_interceptor(custom_interceptor_error);
                          //response_interceptor_to_use = custom_interceptor;
                      }
                      if (use_results_server == undefined){
                          target_api_host = api_host.api_host();
                      } else {
                          target_api_host = api_host.results_host();
                      }
                      
                      
                      resource_to_return= $resource(target_api_host+url,gen_post_args,
                                                    {                             
                                                        'custom_http':{method:http_method, timeout:global_timeout,interceptor:response_interceptor_to_use}
                                                    }
                                                   );
                      return resource_to_return;
                  };

                  var generate_custom_http_executor = function(res,scope_name,type){                
	              return function(mypromise,url_args,post_args){            
	                  if(mypromise == undefined){                
                              mypromise = Utils.resolved_promise();                
	                  }            
	                  return mypromise.then(function(data){                                                
		              if(type == "get"){
	     	                  return execute_getdelete_resource(res,scope_name,url_args);
		              } else {                    
	     	                  return execute_putpost_resource(res,scope_name,url_args,post_args);
		              }
	                  });
	              };
                  };
                  
                  var set_api_host = function(){                                                             
                      var url_params = $location.search();
                      if(url_params.host != undefined){
                          api_url=http_prefix+'://'+url_params.host+':'+server_port+'/';
                          api_host.set_api_host(api_url);
                          api_host.set_results_host(api_url);                          
                      } else {
                          var ip_start = $location.absUrl().indexOf('//')+2;
                          var ip_end = $location.absUrl().indexOf(':',ip_start);
                          var ip = $location.absUrl().substr(ip_start,ip_end-ip_start); 
                          if(ip == undefined || ip == ""){
                              ip=server_ip_address;                              
                          }
                          api_url=http_prefix+'://'+ip+':'+server_port+'/';
                          api_host.set_api_host(api_url);                          
                          api_host.set_results_host(api_url);
                      }
                  };

                  set_api_host();                                    
                  var loginResource = generate_resource_definition(':site/auth/login',
                                                                   'PUT',{ui_route:'.^',message:'Incorrect login info.  Please try again.'});
                  var loginPlayerResource = generate_resource_definition(':site/auth/player_login',
                                                               'PUT',{ui_route:'.^',message:'Incorrect login info.  Please try again.'});    
                  
                  var logoutResource = generate_resource_definition(':site/auth/logout',
                                                                'GET');                                                             
                  var currentUserResource = generate_resource_definition(':site/auth/current_user',
                                                                     'GET');
                  var getRolesResource = generate_resource_definition(':site/role',
                                                                      'GET');
                  var getUserResource = generate_resource_definition(':site/user/:user_id',
                                                                     'GET');                                    
                  var addUserResource = generate_resource_definition(':site/user',
                                                                     'POST');
                  var addPlayerResource = generate_resource_definition(':site/player',
                                                                       'POST');
                  var addPreRegPlayerResource = generate_resource_definition(':site/pre_reg_player',
                                                                       'POST');                  
                  var addTeamResource = generate_resource_definition(':site/team',
                                                                       'POST');                  
                  var getPlayersWithTicketsForDivisionResource = generate_resource_definition(':site/test/players_with_tickets/:division_id',
                                                                                              'GET');
                  var getPlayersResource = generate_resource_definition(':site/player/:player_id',
                                                                        'GET');
                  var getPlayersFastResource = generate_resource_definition(':site/test/player_fast',
                                                                        'GET');
                  var getPlayersPreregFastResource = generate_resource_definition(':site/test/player_prereg_fast',
                                                                        'GET');
                  
                  var getTeamsResource = generate_resource_definition(':site/team/:player_id',
                                                                     'GET');                                                      
                  var updateUserResource = generate_resource_definition(':site/user/:user_id',
                                                                        'PUT');
                  var updatePlayerResource = generate_resource_definition(':site/player/:player_id',
                                                                        'PUT');                 
                  var updateDivisionResource = generate_resource_definition(':site/division/:division_id',
                                                                     'PUT');                  
                  var addTournamentResource = generate_resource_definition(':site/tournament',
                                                                           'POST');
                  var addDivisionResource = generate_resource_definition(':site/division',
                                                                         'POST');
                  var payRegistrationFeeResource = generate_resource_definition(':site/stripe_registration',
                                                                           'POST');                                    
                  var getTournamentResource = generate_resource_definition(':site/tournament/:tournament_id','GET');
                  var getEventsResource = generate_resource_definition('meta_admin/events',
                                                                           'GET');
                  var getTournamentDivisionsResource = generate_resource_definition(':site/tournament/:tournament_id/division',
                                                                                    'GET');
                  var getDivisionResource = generate_resource_definition(':site/division/:division_id',
                                                                         'GET');
                  var getStripePublicKeyResource = generate_resource_definition(':site/stripe/public_key',
                                                                         'GET');                  
                  var getDivisionsResource = generate_resource_definition(':site/division',
                                                                          'GET');
                  var getPlayerBestScoreForMachineResource = generate_resource_definition(':site/entry/player/:player_id/division_machine/:division_machine_id',
                                                                                          'GET');                                                                        
                  var addDivisionMachineResource = generate_resource_definition(':site/division/:division_id/division_machine',
                                                                                'POST');
                  var addTokensResource = generate_resource_definition(':site/token/paid_for/1',
                                                                       'POST');
                  var addPlayerTokensResource = generate_resource_definition(':site/token/paid_for/0',
                                                                             'POST');
                  var completePlayerTokensResource = generate_resource_definition(':site/stripe',
                                                                           'POST');                                     
                  var getDivisionMachinesResource = generate_resource_definition(':site/division/:division_id/division_machine',
                                                                                 'GET');
                  var getAllDivisionMachinesResource = generate_resource_definition(':site/division_machine',
                                                                                 'GET');                  
                  var getMachinesResource = generate_resource_definition(':site/machine',
                                                                         'GET');
                  var getPlayerTokensResource = generate_resource_definition(':site/token/player_id/:player_id',
                                                                         'GET');
                  
                  var getIfpaRankingResource = generate_resource_definition(':site/ifpa/:player_name',
                                                                           'GET');                                    
                  
                  var deleteDivisionMachineResource = generate_resource_definition(':site/division/:division_id/division_machine/:division_machine_id',
                                                                                   'DELETE');
                  var getQueuesResource = generate_resource_definition(':site/queue/division/:division_id',
                                                                       'GET');
                  var getPlayerQueueResource = generate_resource_definition(':site/queue/player_id/:player_id',
                                                                           'GET');                                                      
                  var bumpQueueResource = generate_resource_definition(':site/queue/division_machine/:division_machine_id/bump',
                                                                       'PUT');
                  var addPlayerToMachineResource = generate_resource_definition(':site/division/:division_id/division_machine/:division_machine_id/player/:player_id','PUT');
                  var addTeamToMachineResource = generate_resource_definition(':site/division/:division_id/division_machine/:division_machine_id/team/:team_id','PUT');

                  var addPlayerToMachineFromQueueResource = generate_resource_definition(':site/queue/division_machine/:division_machine_id','PUT');                  
                  var voidScoreResource = generate_resource_definition(':site/entry/division_machine/:division_machine_id/void','PUT');
                  var declareJagoffResource = generate_resource_definition(':site/entry/division_machine/:division_machine_id/jagoff','PUT');
                  var getJagoffsResource = generate_resource_definition(':site/jagoff','GET');                  
                  var addScoreResource = generate_resource_definition(':site/entry/division_machine/:division_machine_id/score/:score','POST');
                  var addToQueueResource = generate_resource_definition(':site/queue','POST');
                  var addOtherPlayerToQueueResource = generate_resource_definition(':site/queue/other_player','POST',{ui_route:'.^',message:'Incorrect player number and pin.  Please try again.'});                  
                  var getDivisionQualifyingResultsPPOResource = generate_resource_definition(':site/results/division/:division_id/ppo/qualifying/list','PUT');
                  
                  var removePlayerFromMachineResource = generate_resource_definition(':site/division_machine/:division_machine_id/player/:player_id','DELETE');
                  var removePlayerFromQueueResource = generate_resource_definition(':site/queue/player/:player_id','DELETE');
                  var getDivisionResultsResource = generate_resource_definition(':site/results/division/:division_id','GET',undefined,true);
                  var getDivisionMachineResultsResource = generate_resource_definition(':site/results/division_machine/:division_machine_id','GET',undefined,true);
                  var voidEntryResource = generate_resource_definition(':site/admin/entry_id/:entry_id/void/:void','DELETE');
                  var addEntryResource = generate_resource_definition(':site/admin/division_machine_id/:division_machine_id/score/:score/player_id/:player_id','POST');                                    
                  var getPlayerResultsResource = generate_resource_definition(':site/results/player/:player_id','GET',undefined,true);
                  var getTeamResultsResource = generate_resource_definition(':site/results/team/:team_id','GET',undefined,true);
                  
                  var getPlayerEntriesResource = generate_resource_definition(':site/entry/player/:player_id','GET');
                  var setScoreResource = generate_resource_definition(':site/admin/score_id/:score_id/score/:score','PUT');
                  var getAuditLogMissingTokensResource = generate_resource_definition(':site/admin/audit_log/where_all_my_tokens_at/player_id/:player_id','GET');
                  var getAuditLogMissingScoresResource = generate_resource_definition(':site/admin/audit_log/where_all_my_scores_at/player_id/:player_id/audit_log_id/:audit_log_id/time_delta/:time_delta','GET');
                  
                  var getPlayerPinResource = generate_resource_definition(':site/player/:player_id/pin','GET');                  
                  
                  return {
	              GetAllResources: function(){
	                  return resource_results;
	              },
                      _ResponseInterceptor: generate_response_interceptor,
                      _GenerateResourceDefinition: generate_resource_definition,        
                      _GenerateCustomHttpExecutor: generate_custom_http_executor,
                      Login: generate_custom_http_executor(loginResource,'logged_in_user','post'),
                      LoginPlayer: generate_custom_http_executor(loginPlayerResource,'logged_in_player','post'),
                      PayRegistrationFee: generate_custom_http_executor(payRegistrationFeeResource,'paid_pre_reg_player','post'),
                      Logout: generate_custom_http_executor(logoutResource,'logout_result','get'),        
                      CurrentUser: generate_custom_http_executor(currentUserResource,'current_user','get'),
                      GetRoles: generate_custom_http_executor(getRolesResource,'roles','get'),
                      GetUsers: generate_custom_http_executor(getUserResource,'users','get'),
                      GetEvents: generate_custom_http_executor(getEventsResource,'events','get'),
                      GetStripePublicKey: generate_custom_http_executor(getStripePublicKeyResource,'stripe_public_key','get'),
                      GetUser: generate_custom_http_executor(getUserResource,'user','get'),
                      GetPlayers: generate_custom_http_executor(getPlayersResource,'players','get'),
                      GetPlayersFast: generate_custom_http_executor(getPlayersFastResource,'players','get'),
                      GetPlayersPreregFast: generate_custom_http_executor(getPlayersPreregFastResource,'players','get'),
                      GetPlayersWithTicketsForDivision: generate_custom_http_executor(getPlayersWithTicketsForDivisionResource,'players_with_tickets','get'),
                      GetPlayerBestScoreForMachine: generate_custom_http_executor(getPlayerBestScoreForMachineResource,'player_best_score_for_machine','get'),
                      GetTeams: generate_custom_http_executor(getTeamsResource,'teams','get'),                      
                      GetPlayer: generate_custom_http_executor(getPlayersResource,'player','get'),                      
                      GetJagoffs: generate_custom_http_executor(getJagoffsResource,'jagoffs','get'),                                            
                      AddUser: generate_custom_http_executor(addUserResource,'added_user','post'),
                      AddTokens: generate_custom_http_executor(addTokensResource,'added_tokens','post'),
                      AddPlayerTokens: generate_custom_http_executor(addPlayerTokensResource,'added_player_tokens','post'),                      
                      AddPlayer: generate_custom_http_executor(addPlayerResource,'added_player','post'),
                      AddPreRegPlayer: generate_custom_http_executor(addPreRegPlayerResource,'added_pre_reg_player','post'),
                      AddTeam: generate_custom_http_executor(addTeamResource,'added_team','post'),                      
                      CompletePlayerTokens: generate_custom_http_executor(completePlayerTokensResource,'completed_player_tokens','post'),                                            
                      UpdateUser: generate_custom_http_executor(updateUserResource,'updated_user','post'),
                      UpdatePlayer: generate_custom_http_executor(updatePlayerResource,'updated_player','post'),
                      AddTournament: generate_custom_http_executor(addTournamentResource,'added_tournament','post'),
                      AddDivision: generate_custom_http_executor(addDivisionResource,'added_division','post'),
                      GetTournaments: generate_custom_http_executor(getTournamentResource,'tournaments','get'),
                      GetDivision: generate_custom_http_executor(getDivisionResource,'division','get'),
                      GetDivisionResults: generate_custom_http_executor(getDivisionResultsResource,'division_results','get'),
                      GetDivisionMachineResults: generate_custom_http_executor(getDivisionMachineResultsResource,'division_machine_results','get'),
                      GetDivisions: generate_custom_http_executor(getDivisionsResource,'divisions','get'),                      
                      GetTournamentDivisions: generate_custom_http_executor(getTournamentDivisionsResource,'tournament_divisions','get'),
                      AddDivisionMachine: generate_custom_http_executor(addDivisionMachineResource,'added_division_machine','post'),
                      AddPlayerToMachineFromQueue: generate_custom_http_executor(addPlayerToMachineFromQueueResource,'machine_added_to','post'),
                      DeleteDivisionMachine: generate_custom_http_executor(deleteDivisionMachineResource,'deleted_division_machine','get'),
                      GetDivisionMachines: generate_custom_http_executor(getDivisionMachinesResource,'division_machines','get'),
                      GetAllDivisionMachines: generate_custom_http_executor(getAllDivisionMachinesResource,'all_division_machines','get'), 
                      UpdateDivision: generate_custom_http_executor(updateDivisionResource,'updated_division','post'),
                      GetIfpaRanking: generate_custom_http_executor(getIfpaRankingResource,'ifpa_rankings','get'),                      
                      GetMachines: generate_custom_http_executor(getMachinesResource,'machines','get'),
                      GetPlayerTokens: generate_custom_http_executor(getPlayerTokensResource,'player_tokens','get'),
                      GetQueues: generate_custom_http_executor(getQueuesResource,'queues','get'),
                      GetPlayerQueue: generate_custom_http_executor(getPlayerQueueResource,'player_queue','get'),                      
                      BumpQueue: generate_custom_http_executor(bumpQueueResource,'queues','put'),
                      AddPlayerToMachine: generate_custom_http_executor(addPlayerToMachineResource,'machine_added_to','put'),
                      AddTeamToMachine: generate_custom_http_executor(addTeamToMachineResource,'machine_added_to','put'),                      
                      VoidScore: generate_custom_http_executor(voidScoreResource,'voided_score','put'),
                      DeclareJagoff: generate_custom_http_executor(declareJagoffResource,'jagoff','put'),
                      AddScore: generate_custom_http_executor(addScoreResource,'added_score','put'),
                      GetDivisionQualifyingResultsPPO: generate_custom_http_executor(getDivisionQualifyingResultsPPOResource,'ppo_qualifying_list','put'),
                      RemovePlayerFromQueue: generate_custom_http_executor(removePlayerFromQueueResource,'modified_queue','delete'),
                      RemovePlayerFromMachine: generate_custom_http_executor(removePlayerFromMachineResource,'machine_removed_from','delete'),
                      GetPlayerResults: generate_custom_http_executor(getPlayerResultsResource,'player_results','get'),
                      GetTeamResults: generate_custom_http_executor(getTeamResultsResource,'team_results','get'),                      
                      GetPlayerEntries: generate_custom_http_executor(getPlayerEntriesResource,'player_entries','get'),                      
                      AddToQueue: generate_custom_http_executor(addToQueueResource,'added_queue','put'),
                      AddOtherPlayerToQueue: generate_custom_http_executor(addOtherPlayerToQueueResource,'added_queue','put'),                      
                      SetScore: generate_custom_http_executor(setScoreResource,'score_set','put'),
                      VoidEntry: generate_custom_http_executor(voidEntryResource,'score_set','delete'),
                      AddEntry: generate_custom_http_executor(addEntryResource,'entry_added','get'),
                      GetAuditLogMissingTokens: generate_custom_http_executor(getAuditLogMissingTokensResource,'audit_log_missing_tokens','get'),
                      GetAuditLogMissingScores: generate_custom_http_executor(getAuditLogMissingScoresResource,'audit_log_missing_scores','get'),
                      
                      GetPlayerPin: generate_custom_http_executor(getPlayerPinResource,'player_pin','get')                      

                      
                  };
              }]);

