angular.module('app',['event_select','pss_admin','event','shared']);
angular.module('app').controller(
    'app_controller',[
        '$scope','$state','credentialsService','$ionicNavBarDelegate','$rootScope','$cookies','$ionicHistory','$ionicPopover','$ionicPopup','$http',
        function($scope, $state,credentialsService,$ionicNavBarDelegate,$rootScope,$cookies,$ionicHistory,$ionicPopover,$ionicPopup,$http) {
            if ($rootScope.credentials == undefined){
                $rootScope.credentials=credentialsService;
            }
            $scope.test_alert = function(message){
                alert(message);
            };
            $scope.bootstrap = function(options){               
                //FIXME : rely on cookies to tell us if we are logged in after page reload                
                $scope.state = $state;
                if($state.current.name.indexOf('pss_admin')!=-1){
                    $state.params.event_name='pss_admin';
                }
                $scope.event_name = $state.params.event_name;
                $rootScope.event_name = $state.params.event_name;
                $ionicNavBarDelegate.title($state.current.data.title);                                
                $ionicNavBarDelegate.align('right');
                $rootScope.header_links=$state.current.data.header_links;
                //$rootScope.back_button=options.back_button==true;
                credentialsService.set_pss_user_credentials_from_cookies($scope.event_name);
                $scope.credentials_for_event = credentialsService.get_credentials()[$scope.event_name];                
                $rootScope.is_logged_in=credentialsService.is_logged_in($scope.event_name);
                //var parent_state = 
                $rootScope.back_button_title=$state.get('^').data.back_title;
                
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
                //                $ionicPopover.fromTemplateUrl('templates/'+$state.current.name+'-help.html', {
                $ionicPopover.fromTemplateUrl('templates/help.html', {                
                    scope: $scope
                }).then(function(popover){
                    $scope.popover.hide();
                    $scope.popover.remove();                    
                    $scope.popover = popover;
                    $scope.popover.show($scope.popover_event);
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
            
            $scope.uploadedFile = function(element) {
                console.log('in uploadedFiled');
                $scope.$apply(function($scope) {
                    console.log('in uploadedFiled apply');
                    $scope.files = element.files;         
                });
            };

            $scope.addFile = function(event_id) {
                console.log('in addfile');
                $scope.uploadfile($scope.files,
                                  event_id,
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
            $scope.uploadfile = function(files,event_id,success,error){                
                var url = 'http://0.0.0.0:8000/pss_admin/media_upload/event/'+event_id+'/jpg_pic';
                console.log(url);
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
                        $rootScope.pic_uploaded=true;                        
                        
                    }).error(function(data){
                        console.log('uh oh!');                    
                        console.log(data);                        
                    });
                }
            };            
        }
    ]
);

angular.module('app').directive('pssTextInputBasic', function($state) {
  return {
      restrict: 'AE',
      replace: 'true',
      scope:true,
      templateUrl: 'templates/generic_text_input_basic.html',
      link: function(scope, elem, attrs) {
          scope.field = attrs.field;
          scope.basic = attrs.basic;          
      }      
  };
});

angular.module('app').directive('pssBooleanInputBasic', function($state) {
  return {
      restrict: 'AE',
      replace: 'true',
      scope:true,
      templateUrl: 'templates/generic_boolean_input_basic.html',
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
      templateUrl: 'templates/generic_boolean_input_advanced.html',
      link: function(scope, elem, attrs) {
          scope.field = attrs.field;
          scope.basic = attrs.basic;          
      }      
  };
});


angular.module('app').directive('pssTextInputAdvanced', function($state) {
  return {
      restrict: 'AE',
      replace: 'true',
      scope:true,
      templateUrl: 'templates/generic_text_input_advanced.html',
      link: function(scope, elem, attrs) {
          scope.field = attrs.field;
          scope.basic = attrs.basic;          
      }      
  };
});

angular.module('app').directive('pssGenericList', function($state) {
  return {
      restrict: 'AE',
      replace: 'true',
      scope:true,
      templateUrl: 'templates/generic_list_directive.html',
      link: function(scope, elem, attrs) {
          console.log(attrs);
          scope.itemsToList=attrs.itemsToList;          
          scope.filter_to_apply = attrs.filterToApply;
          scope.fake_scope=scope;
          scope.not_found_message=attrs.notFoundMessage;
      }      
  };
});


//REMEMBER ME : for later
// angular.module('app').filter('genericSearch', function () {
//   return function (items) {
//   };
// });

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

angular.module('app').filter('playerSearch', function() {

  // Create the return function
  // set the required parameter name to **number**
    return function(items,str_to_search_for,fields_to_match) {                 
        var regex = str_to_search_for;
        var re = new RegExp(regex,"g");
        return _.filter(items, function(item) {                                
                if(item.player_name.match(re)!=null){                    
                    return true;
                }
                if(item.player_id==str_to_search_for){                    
                    return true;
                }                        
            return false;
        });
  };
});
