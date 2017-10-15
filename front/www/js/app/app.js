angular.module('app',['event_select','pss_admin','event','shared','register']);
angular.module('app').controller(
    'app_controller',[
        '$scope','$state','credentialsService','$ionicNavBarDelegate','$rootScope','$cookies','$ionicHistory','$ionicPopover','$ionicPopup','$http','toaster','$ionicScrollDelegate','$location',
        function($scope, $state,credentialsService,$ionicNavBarDelegate,$rootScope,$cookies,$ionicHistory,$ionicPopover,$ionicPopup,$http,toaster,$ionicScrollDelegate,$location) {
            if ($rootScope.credentials == undefined){
                $rootScope.credentials=credentialsService;
            }
            $scope.test_alert = function(message){
                alert(message);
            };
            $scope.check_for_hiding_based_on_wizard = function(){
                var wizard_mode = $cookies.get('wizard_mode');                
                if(wizard_mode != '666'){
                    $rootScope.hide_based_on_cookie=false;
                }
            };
            $scope.event_create_wizard_pop = function(site,key,increment){
                var pop_messages = {'no_events':'Wizard mode enabled!  Click on the Create Event button',
                                    '1_event_no_tournaments':'Event created!  Now click your event and the click QuickCreate Tournament',
                                    '1_event_and_tournaments':'Tournaments created!  You can now click on all the buttons to do stuff'};                                
                if(credentialsService.get_cookie_count(site,key)==1){
                    $scope.pop(pop_messages[key]);
                };                
                if(increment == true){
                    credentialsService.increment_cookie_count(site,key);
                }
            

            };
            // $scope.tournament_create_wizard_pop = function(tournaments){                                
            //     console.log($cookies.get("tournament_wizard_mode"));                
            //     if($rootScope.is_logged_in==true && $cookies.get('tournament_wizard_mode') == '"0 tournaments"'){                                        
            // $scope.pop("Click QuickCreate tournaments");
            //     }
            //     if($rootScope.is_logged_in==true && $cookies.get('tournament_wizard_mode') == "1 tournament unconfigured"){                    
            //         $scope.pop("You have finished setting up your event and tournament.  More text here about what to do next!");
            //         $cookies.put('tournament_wizard_mode','1 tournament configured');                                            
            //     }                
            // };
            
            $scope.post_success_handler = function(title,post_results_rows,scope,attention){
                var post_results={};
                post_results.title=title;
                post_results.results=post_results_rows;
                post_results.attention=attention;
                scope.post_results=post_results;
                scope.post_success = true;
                $ionicScrollDelegate.scrollTop();                
                return post_results;
            };
            $scope.bootstrap = function(options){               
                
                //FIXME : rely on cookies to tell us if we are logged in after page reload                                
                $ionicScrollDelegate.scrollTop();
                $scope.state = $state;
                if($state.current.name.indexOf('pss_admin')!=-1){
                    $state.params.event_name='pss_admin';
                }
                
                $scope.event_name = $state.params.event_name;
                $rootScope.event_name = $state.params.event_name;
                $ionicNavBarDelegate.title($state.current.data.title);                                                
                $rootScope.header_links=$state.current.data.header_links;
                //$rootScope.back_button=options.back_button==true;
                credentialsService.set_pss_user_credentials_from_cookies($scope.event_name);
                $scope.credentials_for_event = credentialsService.get_credentials()[$scope.event_name];                
                //if($scope.credentials_for_event==undefined){
                //    credentialsService.initialize_event_credentials($scope.event_name);
                //}
                $rootScope.is_logged_in=credentialsService.is_logged_in($scope.event_name);
                //var parent_state =                
                $rootScope.back_button_title=$state.get('^').data.back_title;
                $rootScope.is_android = ionic.Platform.isAndroid();
                if(ionic.Platform.isIOS()||ionic.Platform.isAndroid()){
                    $ionicNavBarDelegate.align('right');
                } else {
                    $ionicNavBarDelegate.align('center');
                }
                
                //$scope.append_header_links({icon:'ion-edit',label:'poop',link:'.'});                
            };

            $scope.add_header_links = function(links){
                $rootScope.header_links=links;                
            };
            $scope.append_header_links = function(links){
                $rootScope.header_links.push(links);                
            };
            
            $rootScope.pss_admin_logout = function(event){
                credentialsService.remove_credentials_on_logout(event);                
                $rootScope.is_logged_in=credentialsService.is_logged_in(event);
                if(event == "pss_admin"){
                    $state.go('app.pss_admin.login');    
                }else{
                    $state.go('app.event.login');
                }
                
                
            };
            
            $scope.disable_back_button = function(){
                $rootScope.back_button=false;
            };
            $scope.enable_back_button = function(){
                $rootScope.back_button=true;
            };
            
            
            $rootScope.go_back = function(){
                //history = $ionicHistory.viewHistory();
                //history.back();
                $state.go('.^');                
            };

            $rootScope.openHelpPopover = function($event) {                                                
                $scope.popover.hide();
                $scope.popover.remove();
                var confirmPopup = $ionicPopup.alert({
                    title: 'Help',
                    templateUrl: 'templates/help_alert_'+$state.current.name+'.html',
                    scope:$scope
                });                    
            };
            $rootScope.openFreestandingHelpPopover = function($event) {                                
                $ionicPopover.fromTemplateUrl('templates/help.html', {                
                    scope: $scope
                }).then(function(popover){                    
                    $scope.popover = popover;
                    $scope.popover.show($event);
                });
                
            };
            
            $rootScope.openPopover = function($event) {                                
                $ionicPopover.fromTemplateUrl($state.current.data.quick_links_url, {                
                    scope: $scope
                }).then(function(popover){
                    $scope.popover_event = $event;
                    $scope.popover = popover;
                    $scope.popover.show($event);
                });
                
            };
            
            $rootScope.popoverClick = function(sref) {                                
                $scope.popover.hide();
                $scope.popover.remove();                
                $state.go(sref);                
            };            
            
            $rootScope.popoverOtherSiteClick = function(site,event_name) {                                
                if(event_name==undefined){
                    $scope.popover.hide();
                    $scope.popover.remove();
                }
                if (site =='admin'){
                    if ($scope.is_event_dns()){
                        window.location="http://admin.inchglue.com/";
                    }
                    if ($scope.is_event_html()){
                        if(event_name!=undefined){                            
                            window.location="/admin.html#/app/event/"+event_name;                            
                        } else {
                            window.location="/admin.html";
                        }
                    }                    
                }
            };            
            

            $scope.uploadedFile = function(element) {                
                $scope.$apply(function($scope) {                    
                    $scope.files = element.files;         
                });
            };

            $scope.addFile = function(event_id) {                
                $scope.uploadfile($scope.files,
                                  event_id,
                                  function( msg ) // success
                                  {                                                                            
                                  },
                                  function( msg ) // error
                                  {                                      
                                  });
            };
            $scope.uploadfile = function(files,event_id,success,error){                
                var url = 'http://0.0.0.0:8000/pss_admin/media_upload/event/'+event_id+'/jpg_pic';
                
                for ( var i = 0; i < files.length; i++)
                {
                    var fd = new FormData();
                    fd.append("file", files[i]);                    
                    $http.post(url, fd, { 
                        withCredentials : false,
                        headers : {
                            'Content-Type' : undefined
                        },
                        transformRequest : angular.identity
                        
                    }).success(function(data){                                                
                        $rootScope.pic_uploaded=true;                        
                        
                    }).error(function(data){
                                                
                    });
                }
            };
            $scope.pop = function(text){
	        toaster.pop({type:'info',title:'title',body:text,timeout:0});
	    };
            $scope.is_admin_dns = function(){
                return $location.host().indexOf('admin') == 0;
            };
            $scope.is_event_dns = function(){
                return $location.host().indexOf('event') == 0;            
            };
            $scope.is_admin_html = function(){
                return $location.absUrl().indexOf('admin.html#') >=0;
            };
            $scope.is_event_html = function(){
                return $location.absUrl().indexOf('event.html#') >=0;
            };
        }
    ]
);

angular.module('app').directive('pssTextInputBasic', function($state) {
  return {
      restrict: 'AE',
      replace: 'true',
      scope:true,
      templateUrl: 'templates/directives/generic_text_input_basic.html',
      link: function(scope, elem, attrs) {
          scope.field = attrs.field;
          scope.basic = attrs.basic;
          scope.type = attrs.type;
          if(scope.type == undefined){
              scope.type="text";
          }
      }      
  };
});

angular.module('app').directive('pssBooleanInputBasic', function($state) {
  return {
      restrict: 'AE',
      replace: 'true',
      scope:true,
      templateUrl: 'templates/directives/generic_boolean_input_basic.html',
      link: function(scope, elem, attrs) {
          scope.field = attrs.field;
          scope.basic = attrs.basic;          
      }      
  };
});

angular.module('app').directive('pssBooleanInputAdvanced', function($state) {
  return {
      restrict: 'AE',
      replace: 'true',
      scope:true,
      templateUrl: 'templates/directives/generic_boolean_input_advanced.html',
      link: function(scope, elem, attrs) {
          scope.field = attrs.field;
          scope.basic = attrs.basic;
          scope.type = attrs.type;          
      }      
  };
});


angular.module('app').directive('pssTextInputAdvanced', function($state) {
  return {
      restrict: 'AE',
      replace: 'true',
      scope:true,
      templateUrl: 'templates/directives/generic_text_input_advanced.html',
      link: function(scope, elem, attrs) {
          scope.field = attrs.field;
          scope.basic = attrs.basic;          
      }      
  };
});

angular.module('app').directive('postSuccessMultipleButtons', function($state) {
  return {
      restrict: 'AE',
      replace: 'true',
      scope:{myValue: "@buttonsInfo"},
      templateUrl: 'templates/directives/generic_multi_button_post_success_buttons.html',
      link: function(scope, elem, attrs) {          
          //scope.buttonsInfo = scope.$eval(attrs.buttonsInfo);
          scope.buttonsInfo = scope.$eval(scope.myValue);          
          scope.num_buttons = scope.buttonsInfo.length;          
      }      
  };
});

angular.module('app').directive('postSuccessSingleButton', function($state) {
  return {
      restrict: 'AE',
      replace: 'true',
      scope:true,
      templateUrl: 'templates/directives/generic_goto_parent_post_success_buttons.html',
      link: function(scope, elem, attrs) {
      }      
  };
});

angular.module('app').directive('pssGenericBindingList', function($state,listGeneration,eventTournamentLib) {
  return {
      restrict: 'AE',
      replace: 'true',
      scope:{items_to_list: "=itemsToList",filter_to_apply:"@filterToApply",not_found_message:"@notFoundMessage",not_found_sref:"@notFoundSref",filter_for_string:"=filterForString"},
      templateUrl: 'templates/directives/generic_binding_list_directive.html',
      link: function(scope, elem, attrs) {          
          scope.toggle_view_item_actions = listGeneration.toggle_view_item_actions;
          scope.toggle_item_active = eventTournamentLib.toggle_item_active;
          scope.remove_item = eventTournamentLib.remove_item;
          
          //scope.buttonsInfo = scope.$eval(attrs.buttonsInfo);          
          //scope.buttonsInfo = scope.$eval(scope.myValue);
          //console.log(scope.buttonsInfo);
          //scope.num_buttons = scope.buttonsInfo.length;          
      }      
  };
});

angular.module('app').controller(
    'test_controller',[
        '$scope','$state','credentialsService','$ionicNavBarDelegate','$rootScope','$cookies','$ionicHistory',
        function($scope, $state,credentialsService,$ionicNavBarDelegate,$rootScope,$cookies,$ionicHistory) {
            
        }]);

angular.module('app').filter('useFilter', function($filter) {
    return function() {
        var filterName = [].splice.call(arguments, 1, 1)[0];
        return $filter(filterName).apply(null, arguments);
    };
});


angular.module('app').filter('eventSearch', function($state,credentialsService) {    
    return function(items,str_to_search_for,fields_to_match) {                 
        var creds=credentialsService.get_credentials()[$state.params.event_name];
        var regex = str_to_search_for;
        if(regex!=undefined){
            regex=regex.toLowerCase();
        }
        var re = new RegExp(regex,"g");

        return _.filter(items, function(item) {
            if(item.event_creator_pss_user_id==creds.pss_user_id){                
                if(item.event_name.toLowerCase().match(re)!=null){                    
                    return true;
                } else {
                    return false;
                }                
            } else {
                return false;
            }            
        });
    };
});

angular.module('app').filter('playerSearch', function() {

  // Create the return function
  // set the required parameter name to **number**
    return function(items,str_to_search_for,fields_to_match) {                 
        var regex = str_to_search_for;
        if(regex!=undefined){
            regex=regex.toLowerCase();
        }
        var re = new RegExp(regex,"g");
        return _.filter(items, function(item) {                                
            if(item.player_name.toLowerCase().match(re)!=null){                    
                return true;
            }
            if(item.player_id==str_to_search_for){                    
                return true;
            }                        
            return false;
        });
    };
});

angular.module('app').filter('userSearch', function() {

  // Create the return function
  // set the required parameter name to **number**
    return function(items,str_to_search_for) {                 
        var regex = str_to_search_for;
        if(regex!=undefined){
            regex=regex.toLowerCase();
        }
        var re = new RegExp(regex,"g");
        return _.filter(items, function(item) {                                
            if(item.full_user_name.toLowerCase().match(re)!=null){                    
                return true;
            }
            return false;
        });
    };
});


angular.module('app').filter('machineSearch', function() {

  // Create the return function
  // set the required parameter name to **number**
    return function(items,str_to_search_for) {                         
        var regex = str_to_search_for;
        if(regex!=undefined){
            regex=regex.toLowerCase();
        }
        var re = new RegExp(regex,"g");
        var filtered_values =  _.filter(items, function(item) {                                
            if( item.machine_name.toLowerCase().match(re)!=null){                    
                    return true;
                }
            // if(item.checked==true){                    
            //     return true;
            // }                        
            return false;
        });
        // if(regex!=undefined && regex.length > 0){
        //     return _.orderBy(filtered_values, ['checked'], ['desc']);
        // }        
        return filtered_values;
    };
});
