describe('timeout_resources tests', function() {
    var TimeoutResources;    
    var mock_modals;
    var mock_resource;
    var mock_api_host;
    var unreachable = "Can not perform action requested.  The server is unreachable.";
    var rejected = "The server did not accept the request.";
    var unauthorized = "You are not authroized the do this.";
    var conflict = "The server reports a conflict.";
    var puked = "WHOAH!  Server puked.";    
    var derp = "I have no earthly idea what the hell just happened.";
    var fake_api_host='http://hostname:8000/';    

    var test_http_request = function(status,message){
        var mock_response = {status:status,config:{url:'http://hostname/test/backend/route'}};
        var rejection = TimeoutResources._ResponseInterceptor.responseError(mock_response);        
        expect(mock_modals.error).toHaveBeenCalledWith(message,'test');
        expect(rejection.$$state.value.data.message).toEqual(message);        
    };    

    var test_resource_generation = function(method,interceptor){        
        var resource = TimeoutResources._GenerateResourceDefinition(':site/test/route',method, interceptor);                
        expect(mock_resource).toHaveBeenCalledWith(fake_api_host+':site/test/route',
                                                   {site:'@site'},
                                                   {'custom_http':{method:method,
                                                                   timeout: 15000,
                                                                   interceptor:interceptor
                                                                  }
                                                   }
                                                  );
    };
    
    
    beforeEach(function() {
        module(function($provide) {
            mock_modals = {error:jasmine.createSpy()};
            $provide.value('Modals', mock_modals);            
        });
        angular.mock.module('TD_services.api_host');
        angular.mock.module('TD_services.timeout_resources');
        module(function($provide) {
            mock_api_host = {};
            mock_api_host.api_host = jasmine.createSpy();        
            mock_api_host.api_host.and.returnValue(fake_api_host);            
            mock_api_host.set_api_host = jasmine.createSpy();
            $provide.value('api_host', mock_api_host);                    
        });        
        angular.mock.module('TD_services.utils');
        angular.mock.module('TD_services.user');
        module(function($provide) {
            mock_resource = jasmine.createSpy();
            $provide.value('$resource', mock_resource);            
        });
    });    
    
    beforeEach(inject(function(_TimeoutResources_,_$rootScope_) {                
        TimeoutResources = _TimeoutResources_;
        $rootScope=_$rootScope_;
    }));
    

    it('interceptor should handle timeout/unreachable http request', function() {
        
        test_http_request(-1,unreachable);
    });
    it('interceptor should handle rejected http request', function() {
        test_http_request(400,rejected);
    });
    it('interceptor should handle unauthorized http request', function() {
        test_http_request(401,unauthorized);        
    });
    it('interceptor should handle conflict http request', function() {
        test_http_request(409,conflict);        
    });
    it('interceptor should handle puked http request', function() {
        test_http_request(500,puked);        
    });
    it('interceptor should handle unknown http response', function() {
        test_http_request(999,derp);        
    });
    it('_GenerateResourceDefinition should generate a PUT resource',function(){
        //test_resource_generation('PUT',TimeoutResources._ResponseInterceptor);        
        test_http_request(-1,unreachable);
    });
    it('interceptor should handle rejected http request', function() {
        test_resource_generation('PUT',{});
        
    });
    it('_GenerateResourceDefinition should generate a POST resource',function(){
        //test_resource_generation('POST',TimeoutResources._ResponseInterceptor);
        test_resource_generation('POST',{});        
        
    });
    it('_GenerateResourceDefinition should generate a GET resource',function(){
        //test_resource_generation('GET',TimeoutResources._ResponseInterceptor);
        test_resource_generation('GET',{});        
        
    });
    it('_GenerateResourceDefinition should generate a DELETE resource',function(){
        //test_resource_generation('DELETE',TimeoutResources._ResponseInterceptor);
        test_resource_generation('DELETE',{});                
        
    });    
    it('_GenerateResourceDefinition should handle default responseinterceptor',function(){        
        var resource = TimeoutResources._GenerateResourceDefinition(':site/test/route','GET', undefined);        
        expect(mock_resource).toHaveBeenCalledWith(fake_api_host+':site/test/route',
                                                   {site:'@site'},
                                                   {'custom_http':{method:'GET',
                                                                   timeout: 15000,
                                                                   interceptor:TimeoutResources._ResponseInterceptor
                                                                  }
                                                   }
                                                  );        
    });            
    it('_GenerateCustomHttpExecutor should handle a POST/PUT resource',function(){        
        var fake_resource={'custom_http':jasmine.createSpy()};
        fake_resource.custom_http.and.returnValue({'$promise':jasmine.createSpy()});
        var custom_executor = TimeoutResources._GenerateCustomHttpExecutor(fake_resource,'test_resource','post');                
        var custom_executor_promise = custom_executor(undefined,{test_url_arg:'test_url_arg'},{test_post_arg:'test_post_arg'});
        $rootScope.$apply();
        expect(fake_resource.custom_http).toHaveBeenCalledWith({test_url_arg:'test_url_arg'},{test_post_arg:'test_post_arg'});
        expect(fake_resource.custom_http()['$promise']).toEqual(custom_executor_promise.$$state.value);
    });
    it('_GenerateCustomHttpExecutor should handle a GET/DELETE resource',function(){        
        var fake_resource={'custom_http':jasmine.createSpy()};
        fake_resource.custom_http.and.returnValue({'$promise':jasmine.createSpy()});
        var custom_executor = TimeoutResources._GenerateCustomHttpExecutor(fake_resource,'test_resource','get');                
        var custom_executor_promise = custom_executor(undefined,{test_url_arg:'test_url_arg'});
        $rootScope.$apply();
        expect(fake_resource.custom_http).toHaveBeenCalledWith({test_url_arg:'test_url_arg'});
        expect(fake_resource.custom_http()['$promise']).toEqual(custom_executor_promise.$$state.value);
    });
    it('testing GetAllResources gets all resources',function(){        
        var fake_resource={'custom_http':jasmine.createSpy()};
        fake_resource.custom_http.and.returnValue({'$promise':jasmine.createSpy()});
        var custom_executor = TimeoutResources._GenerateCustomHttpExecutor(fake_resource,'test_resource','get');                
        var custom_executor_promise = custom_executor(undefined,{test_url_arg:'test_url_arg'});
        $rootScope.$apply();
        expect(TimeoutResources.GetAllResources()).toEqual({test_resource: fake_resource.custom_http()});
    });
    
    
});
