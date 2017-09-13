angular.module('resource_wrapper',['ngResource']);
angular.module('resource_wrapper')
    .factory('resourceWrapperService',
             ['$resource','$q','$ionicLoading','$ionicPopup','$state','$timeout',
              function($resource, $q, $ionicLoading,$ionicPopup, $state, $timeout) {
                  //FIXME : this should be in it's own service, but I'm being lazy
                  var on_failure= function(data,new_state){                          
                      var error_message;                          
                      if (data!=undefined && data.message != undefined){
                          error_message = data.message;
                      }                               
                      var alertPopup = $ionicPopup.alert({
                          title: 'Error Encountered',
                          template: error_message
                      });
                      
                      alertPopup.then(function(res) {
                          $state.go(new_state);                              
                      });                
                  };                      
                  

                  var generate_response_interceptor = function(new_state,custom_error){
                      //FIXME: actually do something with custom error (i.e. if all these errors fail, use it)
                      var response_interceptor = {
	                  'responseError': function(rejection) {                                                                        
                              
                              console.log('erroring out with rejection status of '+rejection.status);
	                      if(rejection.status == -1){                                  
                                  rejection.data = {};
		                  rejection.data.message="Can not perform action requested.  The server is unreachable.";
		                  rejection.data.debug="HTTP Timeout while getting<br>"+rejection.config.url;
                                  on_failure(rejection.data,'.');
	                      }
                              if(rejection.status == 401 || rejection.status == 403){                
		                  rejection.data.message="You are not authorized to do this.";
                                  on_failure(rejection.data,'.');                                  
                              }                              
                              if(rejection.status == 409 || rejection.status == 400){                
		                  rejection.data.debug="";
                                  on_failure(rejection.data,'.');
                              }
                              if(rejection.status == 500){                
		                  rejection.data.message="WHOAH!  Server puked.";
		                  rejection.data.debug="";
                                  on_failure(rejection.data,'app');
                              }
                              if(custom_error != undefined){                                  
                                  if(custom_error.message != undefined){
                                      rejection.data.message=custom_error.message;
                                  }                                                                    
                              }                                                            
                              
                              return $q.reject(rejection);                              
	                  }
                      };
                      return response_interceptor;
                  };
                  
                  var get_wrapper_with_loading = function(api_name,on_success,url_parameters,post_parameters){
                      var method = api_name.substring(0,api_name.indexOf('_'));                                                                                        
                      return $ionicLoading.show({
                          template: 'Loading...'                         
                      }).then(function(){                          
                          //new_res = rest_api[api_name][method](url_parameters,post_parameters,on_success,on_error);
                          new_res = rest_api[api_name][method](url_parameters,post_parameters,on_success);
                          return new_res.$promise;
                      }).then(function(){
                          $timeout($ionicLoading.hide,250);
                      }, function(){
                          $timeout($ionicLoading.hide,250);
                      });
                  };
                  var rest_api = {};
                  var rest_server = "http://192.168.1.178:8000";
                  //var rest_server = "http://0.0.0.0:8000";                  
                  var timeout=5000;
                  rest_api['get_events'] = $resource(rest_server+'/pss_admin/event',
                                                     {},
                                                     {'get':{timeout:timeout,interceptor:generate_response_interceptor('.')}});
                  rest_api['get_event'] = $resource(rest_server+'/pss_admin/event/:event_id',
                                                    {},
                                                    {'get':{timeout:timeout,interceptor:generate_response_interceptor('.')}});                  
                  
                  rest_api['post_pss_admin_login'] = $resource(rest_server+'/pss_admin/auth/pss_user/login',
                                                               {},
                                                               {'post':{method:"POST",timeout:timeout,interceptor:generate_response_interceptor('.')}});
                  rest_api['post_create_event'] = $resource(rest_server+'/pss_admin/event',
                                                            {},
                                                            {'post':{method:"POST",timeout:timeout,interceptor:generate_response_interceptor('.')}});
                  rest_api['put_edit_event'] = $resource(rest_server+'/pss_admin/event/:event_id',
                                                            {},
                                                            {'put':{method:"PUT",timeout:timeout,interceptor:generate_response_interceptor('.')}});
                  
                  return {'get_wrapper':function(api_name){return rest_api[api_name];},
                          'get_wrapper_with_loading':get_wrapper_with_loading
                         };
              }
             ]
            );
