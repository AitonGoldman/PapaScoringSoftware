//_ = require('underscore/underscore-min.js');
//_ = require('underscore');

angular = require('angular');
//we can load individual peices for lodash if needed
//FIXME : should be loading lodash properly - see http://www.jvandemo.com/how-to-properly-integrate-non-angularjs-libraries-in-your-angularjs-application/ or https://github.com/rockabox/ng-lodash
mylodash = require('lodash');
require('angular-ui-router');
require('angular-animate');
require('angular-aria');
//FIXME : should only take material components we need, or don't use material for player app
require('angular-material');
//require('angular-ui-bootstrap');
require('angular-resource');
require('angular-sanitize');
require('angular-cookies');
app = angular.module(
	'TDApp',
	[
 	    'ui.router',
            'ngMaterial',
            'ngCookies',
            'TD_services',
            'ngSanitize',
            'app.login',/*REPLACEMECHILD*/
	]
);


app.controller(
    'IndexController',    
    function($scope, $location, $http, 
             $state,$mdSidenav,User, Modals, Utils) {
        Utils.controller_bootstrap($scope,$state);
        $scope.User = User;
    }
);



app.controller(
    'TitleBarController',    
    function($scope, $location, $http, 
             $state,$mdSidenav) {
        
        $scope.toggle_sidenav=function(){            
            $mdSidenav('left_sidenav').toggle();
        };
        
    }
);

app.controller(
    'BackButtonController',    
    function($scope, $location, $http, 
             $state,$mdSidenav) {        
        $scope.back=function(){            
            $state.go("^");
        };
        
    }
);

app.controller(
    'SideBarController',    
    function($scope, $location, $http, 
             $state,User,$mdSidenav,Modals,TimeoutResources,$cookies) {
        $scope.User=User;
        //$scope.state=$state;
        $scope.close_sidebar = function(){
            $mdSidenav('left_sidenav').close();
        };
        $scope.logout = function(){            
            Modals.loading();
            $cookies.remove('session');
            User.log_out();                
            $scope.close_sidebar();
            
            $logout_promise = TimeoutResources.Logout(undefined,{site:$state.params.site});
            $logout_promise.then(function(data){
                Modals.loaded();
            }, function(data){                                
                Modals.loaded();                
            });
        };
    }
);

app.controller(
    'TestController',    
    function($scope, $location, $http, 
             $state,$mdSidenav) {        
        
    }
);

app.config(function($httpProvider) {
    $httpProvider.defaults.useXDomain = true;
    $httpProvider.defaults.withCredentials = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];
    //$httpProvider.interceptors.push('myHttpInterceptor');
});


// app.factory('myHttpInterceptor', function($q,$injector,$rootScope) {
//     return {
// 	'responseError': function(rejection) {
// 	    var Modal = $injector.get('Modal');
// 	    if(rejection.status == -1){
// 		rejection.data={};
// 		rejection.data.message="HTTP Timeout while getting "+rejection.config.url;
// 	    }
// 	    //$rootScope.loading = false;
//             console.log('HTTP problems encountered - stand by for more details');
// 	    console.log(rejection);
// 	    //StatusModal.http_error(rejection.data.message, rejection.data.state_go);	    
// 	    return $q.reject(rejection);
// 	}
//     };
// });


app.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);

    for (var i=0; i<total; i++) {
      input.push(i);
    }

    return input;
  };
});

app.filter('orderObjectBy', function() {
  return function(items, field, reverse) {
    var filtered = [];
      angular.forEach(items, function(item,index) {
          if(index == "$promise" || index == "$resolved"){
              
          } else {
              filtered.push(item);
          }
    });
    filtered.sort(function (a, b) {
      return (a[field] > b[field] ? 1 : -1);
    });
    if(reverse) filtered.reverse();
    return filtered;
  };
});

