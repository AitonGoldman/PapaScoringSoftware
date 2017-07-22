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
        'prereg',
        'prereg.step1',
    'app.prereg_complete',
    'app.set_player_picture',
    'app.finals_scorekeeper',
    'app.generate_finals',
        'app.cycling_machine_results_view',
        'app.cycling_division_results_view',
        'ionicImgCache',
        'app.i_need_an_adult',
    'app.ticket_prices',
    'app.finals',
    /*REPLACEMECHILD*/
	]
);

app.controller(
    'EventSelectController',    
    function($scope, $location, $http, 
             $state,Modals, User, Utils,$ionicPlatform, TimeoutResources, $rootScope, Camera,$ionicHistory) {
        Modals.loading();
        $scope.random=Math.random();
        events_promise = TimeoutResources.GetEvents();
        events_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });
    }
);
app.controller(
    'NativeAppInstructionsController',    
    function($scope, $location, $http, 
             $state,Modals, User, Utils,$ionicPlatform, TimeoutResources, $rootScope, Camera,$ionicHistory) {        
        $scope.platform = ionic.Platform;
    }
);

app.controller(
    'FrontController',    
    function($scope, $location, $http, 
             $state,Modals, User, Utils,$ionicPlatform, TimeoutResources, $rootScope, Camera,$ionicHistory) {        
        $scope.url = $state.params.url;
        $scope.isWebView = ionic.Platform.isWebView();
        $scope.utils = Utils;
        
        $scope.site_display_name = $scope.site.replace(/_/g, " ");
    }
);

app.controller(
    'RedirectController',    
    function($scope, $location, $http, 
             $state,Modals, User, Utils,$ionicPlatform, TimeoutResources, $rootScope, Camera,$ionicHistory) {        
        $scope.url = $state.params.url;
        $scope.isWebView = ionic.Platform.isWebView();
        $scope.utils = Utils;
        $scope.site=$state.params.site;
        $scope.resources = {};
        //        insert_promise  = TimeoutResources.InsertPlayerIntoQueueEx({site:$scope.site,player_id:$scope.player_id_to_add,division_machine_id:$scope.division_machine_id},{},$scope.resources);
        Modals.loading();
        redirect_promise = TimeoutResources.GetExternalUrlEx({site:$scope.site,event_name:$scope.site},{},$scope.resources);
        redirect_promise.then(function(data){
            Modals.loaded();
        });
    }
);

app.controller(
    'IndexController',    
    function($scope, $location, $http, 
             $state,Modals, User, Utils,$ionicPlatform, TimeoutResources, $rootScope, Camera,$ionicHistory,$ionicSideMenuDelegate,ActionSheets) {
        //$scope.type_of_page = type_of_page;        
        $scope.utils = Utils;
        $scope.state = $state;        
        $scope.go_home = function(site){
            $state.go('app',{site:site,reload:true, inherit:true, notify:true});            
            $scope.force_reload();
        };

        
        if(ionic.Platform.isWebView() == false && type_of_page != 'prereg'){
            $scope.type_of_page = 'user';
            player_html_index = $location.absUrl().indexOf('player.html#');
            kiosk_html_index = $location.absUrl().indexOf('kiosk.html#');
            player_papa_org_index = $location.absUrl().indexOf('player.papa.org');
            results_papa_org_index = $location.absUrl().indexOf('results.papa.org');
            kiosk_papa_org_index = $location.absUrl().indexOf('kiosk.papa.org');
            
            if (player_html_index!=-1){
                $scope.type_of_page = 'player';
            }
            if (kiosk_html_index!=-1){
                $scope.type_of_page = 'kiosk';
            }
            if (player_papa_org_index!=-1){
                $scope.type_of_page = 'player';
            }
            if (results_papa_org_index!=-1){
                $scope.type_of_page = 'results';
            }                                                    
        } else {
            $scope.type_of_page = type_of_page;            
        }
        if(window.screen.availWidth < 600){
            $scope.menu_width = 250;
        } else {
            $scope.menu_width = 350;
        }
        
        //alert($scope.menu_width);
        //window.screen.availHeight
        
        $scope.slider={value:0, max:10};
        //FIXME : there has got to be a better place to put this, but I can't put it in
        //        Utils because it will cause a circular reference
        $scope.is_login_age_old = function(login_time){
            cur_time = new Date();
            time_delta = cur_time - login_time;                                        
            if((time_delta/1000) > (60)){
                return true;
            } else {
                return false;
            }            
        };
        $scope.check_not_in_confirm_screen = function(target){
            if($state.current.name.indexOf('confirm')!=-1 && $state.current.name.indexOf('confirm')+7 == $state.current.name.length){
                ActionSheets.choose_confirm_action(target);
            } else {
                $state.go(target);
            }
        };
        $scope.jump_up_results = function(){
            parent_state = $state.current.name.substring(0,$state.current.name.lastIndexOf('.'));            
            //console.log('jumping to '+new_state);
            //$ionicHistory.nextViewOptions({historyRoot:true});
            $ionicHistory.nextViewOptions({disableBack:true});            
            //$state.go('app.results.divisions');
            $state.go(parent_state);            
            $ionicSideMenuDelegate.toggleRight();            
        };
        $scope.is_results_page = function(){
            if($state.current.name.match(/app.results/) != undefined){                
                if($state.current.name == "app.results.division_machines.machines.machine"){
                    return "Division Machines";
                }
                if($state.current.name == "app.results.divisions.division"){
                    return "Divisions";
                }                
                if($state.current.name == "app.results.players.player"){
                    return "Players";
                }                
                
            } else {
                return undefined;
            }
        };
        $scope.jump_to_machine_list = function(){
            console.log($state.params.division_id);
            if($state.current.name.indexOf('confirm')!=-1 && $state.current.name.indexOf('confirm')+7 == $state.current.name.length){
                ActionSheets.choose_confirm_action('app.scorekeeping.machine_select');
            } else {
                $ionicHistory.nextViewOptions({disableBack:true});
                $state.go('app.scorekeeping.machine_select');
            }                        
            //$state.go('app.scorekeeping.machine_select',{site:$state.params.site,division_id:$state.params.division_id});
            $ionicSideMenuDelegate.toggleRight();            
        };
        
        $scope.is_scorekeeping_page = function(){
            if($state.current.name.match(/app.scorekeeping/) != undefined || $state.current.name.match(/app.queue_player_after_play/) != undefined){                
                return true;
            } else {
                return undefined;
            }
        };
        $scope.is_player_login_page = function(){
            if($state.current.name.match(/app.login_player/) != undefined){                
                return true;
            } else {
                return undefined;
            }
        };
                
        $scope.controller_bootstrap = function(scope, state, do_not_check_current_user){                        
            if(ionic.Platform.isWebView() == false && $scope.type_of_page != 'user' && $scope.type_of_page != 'results'){                
                if(ionic.Platform.isIOS() || ionic.Platform.isAndroid()){
                    $state.go('use_the_native_app');
                }
            }
            version_check_promise = Utils.resolved_promise();            
            $scope.site=state.params.site;            
            User.set_user_site($scope.site);
            
            if(ionic.Platform.isWebView() == true && $scope.type_of_page == 'player'){                
                 if(ionic.Platform.isIOS() || ionic.Platform.isAndroid()){
                     version_check_promise = TimeoutResources.VersionCheck(undefined,{site:$scope.site,version_string:"v2"});
                 }
            }
                
            prom = TimeoutResources.GetDivisions(undefined,{site:$scope.site});            
            
            if(do_not_check_current_user == undefined && User.logged_in() == false){
                return prom.then(function(data){
                    if($scope.type_of_page != "results"){
                        return check_user_promise = User.check_current_user();
                    } else {
                        return Utils.resolved_promise();
                    }                    
                });                
            }else{
                return prom;
            }                                 
        };
        $scope.customBackButtonNav = function(){
            if($state.current.name.match(/app.results/) != undefined){                
                console.log($ionicHistory.backView());
                
                $ionicHistory.goBack();           
            } else {
                $state.go('^');
            }
            
        };
        $scope.randomNumber = $rootScope.randomNumber;        
        if($state.current.name == "app"){
            $scope.controller_bootstrap($scope,$state);            
        }        
        $scope.User = User;
        $scope.isIOS = ionic.Platform.isIOS();
        $scope.isWebView = ionic.Platform.isWebView();        
        //FIXME : don't need this anymore
        if($scope.isIOS == true){
            $scope.menu_bar_title_style={'height':'100'};
        } else {
            $scope.menu_bar_title_style={'height':'120'};
        }
        $scope.uploaded_pic_name=undefined;
        $ionicPlatform.ready(function() {        
        });
        $scope.force_reload = function(){
            divisions_promise = TimeoutResources.GetDivisions(undefined,{site:$scope.site});            
            divisions_promise.then(function(data){
                $state.reload($state.current);
            });
        };
        $scope.server_ip_address=server_ip_address;
        $scope.http_prefix=http_prefix;
        $scope.server_port=server_port;

        //$scope.type_of_page=
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

    }
);

app.run(function($ionicPlatform,$rootScope,$ionicPopup,$state) {
    $ionicPlatform.ready(function() {

        ionic.Platform.showStatusBar(false);        
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
        if($state.current.name == 'app.queues.machine_select.machine_queue'){
            $state.go('app.queues.machine_select.machine_queue',{division_id:$state.params.division_id,division_machine_id:$state.params.division_machine_id,division_machine_name:$state.params.division_machine_id},{reload:true});
        }
        var alertPopup = $ionicPopup.alert({
            title: 'Papa Scoring Notification',
            template: msg.text
        });        
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
  

app.config(function($httpProvider,$ionicConfigProvider,$ionicCloudProvider,ionicImgCacheProvider) {
    $httpProvider.defaults.useXDomain = true;
    $httpProvider.defaults.withCredentials = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];
    $ionicConfigProvider.backButton.previousTitleText(false);
    $ionicConfigProvider.backButton.text(" ");        
    $ionicConfigProvider.backButton.icon('ion-arrow-left-a');
    ionicImgCacheProvider.debug(true);    
    if (!ionic.Platform.isIOS()) {
        $ionicConfigProvider.scrolling.jsScrolling(false);
    }
    $ionicCloudProvider.init({
        "core": {
            "app_id": secret_info_app_id
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

