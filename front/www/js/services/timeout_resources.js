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
	                  rejection.data={};
	                  if(rejection.status == -1){                
		              rejection.data.message="Can not perform action requested.  The server is unreachable.";
		              rejection.data.debug="HTTP Timeout while getting<br>"+rejection.config.url;
	                  }
                          if(rejection.status == 400){                
		              rejection.data.message="The server did not accept the request.";
		              rejection.data.debug="";
                          }
                          if(rejection.status == 401){                
		              rejection.data.message="You are not authroized the do this.";
		              rejection.data.debug="";
                          }
                          if(rejection.status == 409){                
		              rejection.data.message="The server reports a conflict.";
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
                      console.log('in generate resource def');
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
                      if(url_params.host != undefined){
                          api_host.set_api_host('http://'+url_params.host+':8000/');
                      } else {
                          var ip_start = $location.absUrl().indexOf('//')+2;
                          var ip_end = $location.absUrl().indexOf(':',ip_start);
                          var ip = $location.absUrl().substr(ip_start,ip_end-ip_start); 
                          if(ip == undefined || ip == ""){
                              ip = "192.168.1.178";
                          }
                          api_host.set_api_host('http://'+ip+':8000/');
                      }
                  };

                  set_api_host();                                    
                  var loginResource = generate_resource_definition(':site/auth/login',
                                                               'PUT',{});    
                  var logoutResource = generate_resource_definition(':site/auth/logout',
                                                                'GET');                                                             
                  var currentUserResource = generate_resource_definition(':site/auth/current_user',
                                                                     'GET');
                  
                  return {
	              GetAllResources: function(){
	                  return resource_results;
	              },
                      _ResponseInterceptor: response_interceptor,
                      _GenerateResourceDefinition: generate_resource_definition,        
                      _GenerateCustomHttpExecutor: generate_custom_http_executor,
                      Login: generate_custom_http_executor(loginResource,'logged_in_user','post'),
                      Logout: generate_custom_http_executor(logoutResource,'logout_result','get'),        
                      CurrentUser: generate_custom_http_executor(currentUserResource,'current_user','get')
                  };
              }]);

