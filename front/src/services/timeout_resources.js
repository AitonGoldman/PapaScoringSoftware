angular.module('TD_services.timeout_resources', ['ngResource']);
angular.module('TD_services.timeout_resources').factory('TimeoutResources',
                                                        ['$resource','$q', function($resource,$q) {
    var resource_results = {};

    global_timeout = 15000;
    
    var resolved_promise = function(){
	var defer = $q.defer();
	defer.resolve();
	return defer.promise;
    };
    
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
       
    var generate_resource_definition = function(url,http_method){        
        url_chunks = url.split("/");
        gen_post_args = {};
        for(url_chunk_index in url_chunks){
            url_chunk = url_chunks[url_chunk_index];
            if(url_chunk.indexOf(':')>=0){
                arg_name = url_chunk.substr(1);
                gen_post_args[arg_name]='@'+arg_name;
            };
        }
        return $resource('[APIHOST]/'+url,gen_post_args,
                         {                             
                             'custom_http':{method:http_method, timeout:global_timeout}
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

    loginResource = generate_resource_definition('/:site/auth/login',
                                                 'PUT');
    return {
	GetAllResources: function(){//killroy was here
	    return resource_results;
	},    
        Login: generate_custom_http_executor(loginResource,'logged_in_user','post')
    };
}]);

