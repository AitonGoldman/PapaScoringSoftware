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
                  var response_interceptor = {
	              'responseError': function(rejection) {            
                          //FIXME : need error dialog to display
                          poop = rejection;
                          console.log(rejection);                          
	                  //rejection.data={};
	                  if(rejection.status == -1){
                              rejection.data = {};
		              rejection.data.message="Can not perform action requested.  The server is unreachable.";
		              rejection.data.debug="HTTP Timeout while getting<br>"+rejection.config.url;
	                  }
                          if(rejection.status == 400){                
		              //rejection.data.message="The server did not accept the request.";
		              //rejection.data.debug="";
                          }
                          if(rejection.status == 401){                
		              rejection.data.message="You are not authroized to do this.";
		              //rejection.data.debug="";
                          }
                          if(rejection.status == 409){                
		              //rejection.data.message="The server reports a conflict.";
		              rejection.data.debug="";
                          }
                          if(rejection.status == 500){                
		              rejection.data.message="WHOAH!  Server puked.";
		              rejection.data.debug="";
                          }
                          if(rejection.data.message == undefined){
                              rejection.data.message="I have no earthly idea what the hell just happened.";
                          }
                          //console.log('HTTP problems encountered on request - stand by for more details');
	                  //console.log(rejection);
                          site = rejection.config.url.split('/')[3];
                          Modals.error(rejection.data.message,site);
	                  return $q.reject(rejection);
	              }
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
                  
                  var generate_resource_definition = function(url,http_method,custom_interceptor){                                                    
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
                      if(custom_interceptor == undefined){
                          response_interceptor_to_use = response_interceptor;
                      } else {
                          response_interceptor_to_use = custom_interceptor;
                      }
                      var target_api_host = api_host.api_host();
                      
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
                      // if (type_of_page == "player"){
                      //     server_port = "8001";
                      // } else {
                      //     server_port = "8000";
                      // }
                      if(url_params.host != undefined){
                          api_host.set_api_host('http://'+url_params.host+':'+server_port+'/');
                      } else {
                          var ip_start = $location.absUrl().indexOf('//')+2;
                          var ip_end = $location.absUrl().indexOf(':',ip_start);
                          var ip = $location.absUrl().substr(ip_start,ip_end-ip_start); 
                          if(ip == undefined || ip == ""){
                              //ip = "192.168.1.178";
                              //ip = "9.75.197.73";
                              //ip="9.75.197.135";
                              //ip="98.111.232.93";
                              ip=server_ip_address;                              
                          }
                          api_host.set_api_host('http://'+ip+':'+server_port+'/');
                      }
                  };

                  set_api_host();                                    
                  var loginResource = generate_resource_definition(':site/auth/login',
                                                                   'PUT',{});
                  var loginPlayerResource = generate_resource_definition(':site/auth/player_login',
                                                               'PUT',{});    
                  
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
                  var getPlayersResource = generate_resource_definition(':site/player/:player_id',
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
                  var getTournamentResource = generate_resource_definition(':site/tournament/:tournament_id',
                                                                           'GET');
                  var getTournamentDivisionsResource = generate_resource_definition(':site/tournament/:tournament_id/division',
                                                                                    'GET');
                  var getDivisionResource = generate_resource_definition(':site/division/:division_id',
                                                                         'GET');
                  var getDivisionsResource = generate_resource_definition(':site/division',
                                                                     'GET');                                                      
                  var addDivisionMachineResource = generate_resource_definition(':site/division/:division_id/division_machine',
                                                                                'POST');
                  var addTokensResource = generate_resource_definition(':site/token/paid_for/1',
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
                  var bumpQueueResource = generate_resource_definition(':site/queue/division_machine/:division_machine_id/bump',
                                                                       'PUT');
                  var addPlayerToMachineResource = generate_resource_definition(':site/division/:division_id/division_machine/:division_machine_id/player/:player_id','PUT');
                  var addPlayerToMachineFromQueueResource = generate_resource_definition(':site/queue/division_machine/:division_machine_id','PUT');                  
                  var voidScoreResource = generate_resource_definition(':site/entry/division_machine/:division_machine_id/void','PUT');                                                      
                  var addScoreResource = generate_resource_definition(':site/entry/division_machine/:division_machine_id/score/:score','POST');
                  var addToQueueResource = generate_resource_definition(':site/queue','POST');                                    
                  var removePlayerFromQueueResource = generate_resource_definition(':site/queue/player/:player_id','DELETE');
                  var getDivisionResultsResource = generate_resource_definition(':site/results/division/:division_id','GET');
                  var getDivisionMachineResultsResource = generate_resource_definition(':site/results/division_machine/:division_machine_id','GET');
                  var voidEntryResource = generate_resource_definition(':site/admin/entry_id/:entry_id/void/:void','DELETE');
                  var addEntryResource = generate_resource_definition(':site/admin/division_machine_id/:division_machine_id/score/:score/player_id/:player_id','POST');                                    
                  var getPlayerResultsResource = generate_resource_definition(':site/results/player/:player_id','GET');
                  var getPlayerEntriesResource = generate_resource_definition(':site/entry/player/:player_id','GET');
                  var setScoreResource = generate_resource_definition(':site/admin/score_id/:score_id/score/:score','PUT');
                  var getAuditLogMissingTokensResource = generate_resource_definition(':site/admin/audit_log/where_all_my_tokens_at/player_id/:player_id','GET');
                  var getAuditLogMissingScoresResource = generate_resource_definition(':site/admin/audit_log/where_all_my_scores_at/player_id/:player_id/audit_log_id/:audit_log_id/time_delta/:time_delta','GET');
                  
                  var getPlayerPinResource = generate_resource_definition(':site/player/:player_id/pin','GET');                  
                  
                  return {
	              GetAllResources: function(){
	                  return resource_results;
	              },
                      _ResponseInterceptor: response_interceptor,
                      _GenerateResourceDefinition: generate_resource_definition,        
                      _GenerateCustomHttpExecutor: generate_custom_http_executor,
                      Login: generate_custom_http_executor(loginResource,'logged_in_user','post'),
                      LoginPlayer: generate_custom_http_executor(loginPlayerResource,'logged_in_player','post'),                      
                      Logout: generate_custom_http_executor(logoutResource,'logout_result','get'),        
                      CurrentUser: generate_custom_http_executor(currentUserResource,'current_user','get'),
                      GetRoles: generate_custom_http_executor(getRolesResource,'roles','get'),
                      GetUsers: generate_custom_http_executor(getUserResource,'users','get'),
                      GetUser: generate_custom_http_executor(getUserResource,'user','get'),
                      GetPlayers: generate_custom_http_executor(getPlayersResource,'players','get'),
                      GetPlayer: generate_custom_http_executor(getPlayersResource,'player','get'),                                            
                      AddUser: generate_custom_http_executor(addUserResource,'added_user','post'),
                      AddTokens: generate_custom_http_executor(addTokensResource,'added_tokens','post'),
                      AddPlayer: generate_custom_http_executor(addPlayerResource,'added_player','post'),
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
                      BumpQueue: generate_custom_http_executor(bumpQueueResource,'queues','put'),
                      AddPlayerToMachine: generate_custom_http_executor(addPlayerToMachineResource,'machine_added_to','put'),
                      VoidScore: generate_custom_http_executor(voidScoreResource,'voided_score','put'),
                      AddScore: generate_custom_http_executor(addScoreResource,'added_score','put'),
                      RemovePlayerFromQueue: generate_custom_http_executor(removePlayerFromQueueResource,'modified_queue','delete'),
                      GetPlayerResults: generate_custom_http_executor(getPlayerResultsResource,'player_results','get'),                        GetPlayerEntries: generate_custom_http_executor(getPlayerEntriesResource,'player_entries','get'),                      
                      AddToQueue: generate_custom_http_executor(addToQueueResource,'added_queue','put'),
                      SetScore: generate_custom_http_executor(setScoreResource,'score_set','put'),
                      VoidEntry: generate_custom_http_executor(voidEntryResource,'score_set','delete'),
                      AddEntry: generate_custom_http_executor(addEntryResource,'entry_added','get'),
                      GetAuditLogMissingTokens: generate_custom_http_executor(getAuditLogMissingTokensResource,'audit_log_missing_tokens','get'),
                      GetAuditLogMissingScores: generate_custom_http_executor(getAuditLogMissingScoresResource,'audit_log_missing_scores','get'),
                      
                      GetPlayerPin: generate_custom_http_executor(getPlayerPinResource,'player_pin','get')                      

                      
                  };
              }]);

