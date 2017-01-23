app = angular.module(
	'TDApp',
    [
        'ionic',
        'ionic.cloud',
        'ionic.ion.imageCacheFactory',
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
    'app.remove_player',
    'app.ppo_qualifying_list',
    /*REPLACEMECHILD*/
	]
);

app.controller(
    'IndexController',    
    function($scope, $location, $http, 
             $state,Modals, User, Utils,$ionicPlatform, TimeoutResources, $rootScope, Camera) {
        //$scope.type_of_page = type_of_page;
        if(ionic.Platform.isWebView() == false){
            if ($location.absUrl().includes('player.html#')!=true){
                $scope.type_of_page = 'user';
            } else {
                $scope.type_of_page = 'player';                
            }            
        } else {
            $scope.type_of_page = type_of_page;            
        }
        $scope.slider={value:0, max:10};
        //FIXME : there has got to be a better place to put this, but I can't put it in
        //        Utils because it will cause a circular reference
        $scope.controller_bootstrap = function(scope, state, do_not_check_current_user){                        
            $scope.site=state.params.site;            
            User.set_user_site($scope.site);
            if (User.logged_in() == true) {
                if (User.login_time == undefined){
                    User.login_time = new Date();                    
                } else {
                    cur_time = new Date();
                    time_delta = cur_time - User.login_time;                                        
                    if((time_delta/1000) > (60)){
                        return TimeoutResources.GetDivisions(undefined,{site:$scope.site});                        
                    }
                }
                return Utils.resolved_promise();
            }             
            if(do_not_check_current_user == undefined && User.logged_in() == false){                
                
                check_user_promise = User.check_current_user();
                get_divisions_promise = check_user_promise.then(function(data){                    
                    if(TimeoutResources.GetAllResources().divisions==undefined){
                        //Modals.loading();
                        return TimeoutResources.GetDivisions(undefined,{site:$scope.site});
                    }
                });
                
                return get_divisions_promise.then(function(data){
                    //Modals.loaded();
                });
            }                                 
        };
        $scope.customBackButtonNav = function(){
            $state.go('^');
        };
        $scope.randomNumber = $rootScope.randomNumber;        
        if($state.current.name == "app"){
            $scope.controller_bootstrap($scope,$state);
        }        
        $scope.User = User;
        $scope.isIOS = ionic.Platform.isIOS();
        //FIXME : don't need this anymore
        if($scope.isIOS == true){
            $scope.menu_bar_title_style={'height':'100'};
        } else {
            $scope.menu_bar_title_style={'height':'120'};
        }
        $scope.is_native = false;
        $scope.uploaded_pic_name=undefined;
        $ionicPlatform.ready(function() {        
            dev_info = ionic.Platform.device();
            if (_.size(dev_info)!=0){
                $scope.is_native=true;
                //alert('on a native app');
            }
        });
        $scope.force_reload = function(){
            divisions_promise = TimeoutResources.GetDivisions(undefined,{site:$scope.site});            
            divisions_promise.then(function(data){
                $state.reload($state.current);
            });
        };
        $scope.server_ip_address=server_ip_address;
        $scope.take_pic_and_upload = function(type,info_object,site,id){            
            upload_pic_promise = Camera.take_user_pic_and_upload(type,site,id);
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
        /* 
         //example of how to use imagecache 
         // make sure module/function inserts $ImageCacheFactory
         image_cache_list = [];
         for(x=1;x<500;x++){
                    image_cache_list[x]="http://192.168.1.178/pics/player_"+x+".jpg";
                }
                $ImageCacheFactory.Cache(
                    image_cache_list
                ).then(function(){
                    console.log("Images done loading!");
                    Modals.loaded();
                },function(failed){
                    console.log("An image failed: "+failed);
                    Modals.loaded();
                });                

         */

        /*
         //THESE 3 HANDLE FILE UPLOADS
         //SEE COMMENTED SECTION OF FRONT.HTML
        $scope.uploadedFile = function(element) {
            console.log('in uploadedFiled');
            $scope.$apply(function($scope) {
                console.log('in uploadedFiled apply');
                $scope.files = element.files;         
            });
        };
        $scope.addFile = function() {
            console.log('in addfile');
            $scope.uploadfile($scope.files,
                                     function( msg ) // success
                              {
                                  console.log('in addfile - success');
                                  console.log('uploaded');
                              },
                              function( msg ) // error
                              {
                                  console.log('in addfile - failure');                                  
                                  console.log('error');
                              });
        };
        $scope.uploadfile = function(files,success,error){
 
            var url = 'http://192.168.1.178:8000/elizabeth/test/media_upload';

            for ( var i = 0; i < files.length; i++)
            {
                var fd = new FormData();
                fd.append("file", files[i]);
                console.log(files[i]);
                $http.post(url, fd, { 
                    withCredentials : false,
                    headers : {
                        'Content-Type' : undefined
                    },
                    transformRequest : angular.identity

                }).success(function(data){
                    console.log('success!');
                    console.log(data);
                    $scope.uploaded_pic_name=data.poop;

                }).error(function(data){
                    console.log('uh oh!');                    
                    console.log(data);
                });
            }
        };*/        
        //FIXME : rename this more logically
    }
);

app.run(function($ionicPlatform,$rootScope) {
  $ionicPlatform.ready(function() {
    // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
    // for form inputs)
    if(window.cordova && window.cordova.plugins.Keyboard) {

  //Change this to false to return accessory bar 
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(false);
    }
    if(window.StatusBar) {
      // org.apache.cordova.statusbar required
      StatusBar.styleDefault();
    }
  });
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

app.filter('rangeObject', function() {
    
    return function(input, total, start,increment) {            
        if(increment == undefined){
            increment=1;
        }
        if(start == undefined){
            start = 0;
        }
        total = parseInt(total);
        
        for (var i=start; i<total; i=i+increment) {
            input.push({"value":i});
        }                        
        return input;
    };
    
});

