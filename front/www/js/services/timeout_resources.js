angular.module('TD_services.timeout_resources', ['ngResource']);
angular.module('TD_services.timeout_resources').factory('TimeoutResources',
                                                        ['$resource','$q',
                                                         '$injector','Modals',
                                                         function($resource,$q,$injector,Modals) {
    var resource_results = {};
    var response_interceptor = {
	'responseError': function(rejection) {            
            //FIXME : need error dialog to display            
	    if(rejection.status == -1){
		rejection.data={};
		rejection.data.message="Can not perform action requested<br>.  The server is unreachable.";
		rejection.data.debug="HTTP Timeout while getting<br>"+rejection.config.url;
	    }
            if(rejection.status == 400){
		rejection.data={};
		rejection.data.message="The server did not accept the request.";
		rejection.data.debug="";
            }
            if(rejection.status == 401){
		rejection.data={};
		rejection.data.message="You are not authroized the do this.";
		rejection.data.debug="";
            }
            if(rejection.status == 409){
		rejection.data={};
		rejection.data.message="The server reports a conflict.";
		rejection.data.debug="";
            }
            if(rejection.status == 500){
		rejection.data={};
		rejection.data.message="WHOAH!  Server puked.";
		rejection.data.debug="";
            }
            
            console.log('HTTP problems encountered on request - stand by for more details');
	    console.log(rejection);
            site = rejection.config.url.split('/')[3];
            Modals.error(rejection.data.message,site);
	    return $q.reject(rejection);
	}
    };                                                            
    global_timeout = 15000;

        //FIXME : THIS BELONGS IN UTILS
    var resolved_promise = function(){
	var defer = $q.defer();
	defer.resolve();
	return defer.promise;
    };
       //FIXME : THIS BELONGS IN UTILS    
    var rejected_promise = function(){
	var defer = $q.defer();
	defer.reject();
	return defer.promise;
    };
 
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
        res=res['custom_http'];                
        resource_results[scope_name] = res(url_args, post_args);
	return resource_results[scope_name].$promise;	
    };
       
        var generate_resource_definition = function(url,http_method,default_interceptor){        
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
        if(default_interceptor == undefined){
            response_interceptor_to_use = response_interceptor;
        }
        
        return $resource(api_host+url,gen_post_args,
                         {                             
                             'custom_http':{method:http_method, timeout:global_timeout,interceptor:response_interceptor_to_use}
                         }
                        );
    };

    var generate_custom_http_executor = function(res,scope_name,type){        
	return function(promise,url_args,post_args){
	    if(promise == undefined){
                promise = resolved_promise();
	    }	    
	    return promise.then(function(data){
		if(type == "get"){
	     	    return execute_getdelete_resource(res,scope_name,url_args);
		} else {
	     	    return execute_putpost_resource(res,scope_name,url_args,post_args);
		}
	    });
	};
    };    
    loginResource = generate_resource_definition(':site/auth/login',
                                                 'PUT',false);
    logoutResource = generate_resource_definition(':site/auth/logout',
                                                 'GET',false);                                                             
    currentUserResource = generate_resource_definition(':site/auth/current_user',
                                                       'GET',false);
                                                             
    return {
	GetAllResources: function(){
	    return resource_results;
	},    
        Login: generate_custom_http_executor(loginResource,'logged_in_user','post'),
        Logout: generate_custom_http_executor(logoutResource,'logout_result','get'),        
        CurrentUser: generate_custom_http_executor(currentUserResource,'current_user','get')
    };
}]);

