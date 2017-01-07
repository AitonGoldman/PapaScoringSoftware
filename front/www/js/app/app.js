app = angular.module(
	'TDApp',
    [
        'ionic',
        'ionic.cloud',
        'ngCordova',
 	'ui.router',            
        'ngCookies',            
        'ngSanitize',
        'ngAnimate',
        'app.login',
        'TD_services',
        'app.login',        
    'app.logout',
    'app.user',
    'app.tournament',
    'app.player',
    'app.token',
        'app.scorekeeping',
        'app.login_player',    
    'app.queues',
    'app.results',
    'app.queue_view',
    'app.oops',
    'app.player_token',
    'app.teams',
    'app.queue_player_after_play',
    'app.jagoffs',
    /*REPLACEMECHILD*/
	]
);

app.controller(
    'IndexController',    
    function($scope, $location, $http, 
             $state,Modals, User, Utils,$ionicPlatform, TimeoutResources, $rootScope, Camera) {
        //$scope.type_of_page = type_of_page;
        $scope.type_of_page = 'player';                
        if(ionic.Platform.isWebView() == false){
            if ($location.absUrl().includes('player.html#')!=true){
                $scope.type_of_page = 'user';
            };
        } else {
                $scope.type_of_page = 'user';            
        }
        $scope.slider={value:0, max:10};
        //FIXME : there has got to be a better place to put this, but I can't put it in
        //        Utils because it will cause a circular reference
        $scope.controller_bootstrap = function(scope, state, do_not_check_current_user){
            $scope.site=state.params.site;            
            User.set_user_site($scope.site);            
            if(do_not_check_current_user == undefined && User.logged_in() == false){                
                
                check_user_promise = User.check_current_user();
                get_divisions_promise = check_user_promise.then(function(data){
                    Modals.loading();
                    return TimeoutResources.GetDivisions(undefined,{site:$scope.site});
                });
                
                return get_divisions_promise.then(function(data){
                    Modals.loaded();
                });
            } else {
                return Utils.resolved_promise();
            }                                 
        };
        $scope.customBackButtonNav = function(){
            $state.go('^');
        };
        $scope.randomNumber = $rootScope.randomNumber;        
        $scope.controller_bootstrap($scope,$state);
        $scope.User = User;
        $scope.isIOS = ionic.Platform.isIOS();
        //FIXME : don't need this anymore
        if($scope.isIOS == true){
            $scope.menu_bar_title_style={'height':'100'};
        } else {
            $scope.menu_bar_title_style={'height':'120'};
        }
        $scope.is_native = false;
        $ionicPlatform.ready(function() {        
            dev_info = ionic.Platform.device();
            if (_.size(dev_info)!=0){
                $scope.is_native=true;
                //alert('on a native app');
            }
        });
        $scope.server_ip_address=server_ip_address;
        $scope.take_pic_and_upload = function(type,info_object){            
            upload_pic_promise = Camera.take_user_pic_and_upload(type);
            upload_pic_promise.then(function(data){
                if(data.result == Camera.TRANSFER_SUCCESS){                    
                    //$scope.user_info.pic_file = data.file_name;
                    //$scope.user_info.has_picture=true;
                    info_object.pic_file = data.file_name;
                    info_object.has_picture=true;
                    $scope.random_img=_.random(0,99999);
                }                    
            });
        };        
        //FIXME : rename this more logically
    }
);

app.run(function($ionicPlatform,$rootScope) {
    $rootScope.$on('cloud:push:notification', function(event, data) {
        var msg = data.message;
        alert(msg.title + ': ' + msg.text);
    });


    $rootScope.$on('$stateChangeStart', 
                   function(event, toState, toParams, fromState, fromParams, options){
                       $rootScope.randomNumber=_.random(0,10);
                       var image = document.getElementById('side_menu_user_icon');                       
                       //FIXME : needs to be smarter about constructing this so it doesn't make a huge url
                       if(image != null){
                           image.src=image.src+"?"+$rootScope.randomNumber;
                       }                       
                   });
});
  

app.config(function($httpProvider,$ionicConfigProvider,$ionicCloudProvider) {
    $httpProvider.defaults.useXDomain = true;
    $httpProvider.defaults.withCredentials = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];
    $ionicConfigProvider.backButton.previousTitleText(false);
    $ionicConfigProvider.backButton.text(" ");
    $ionicConfigProvider.backButton.icon('ion-arrow-left-a');
 $ionicCloudProvider.init({
    "core": {
      "app_id": "a302e6bc"
    },
    "push": {
      "sender_id": "566222718762",
      "pluginConfig": {
        "ios": {
          "badge": true,
          "sound": true
        },
        "android": {
          "iconColor": "#343434"
        }
      }
    }
  });    
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

app.filter('range', function() {
    
    return function(input, total, start, increment) {    
        if(increment == undefined){
            increment=1;
        }
        if(start == undefined){
            start = 0;
        }
        total = parseInt(total);
        
        for (var i=start; i<total; i=i+increment) {
            input.push(i);
        }
    return input;
  };
});

