angular.module('app',['event_select','pss_admin','event']);
angular.module('app').controller(
    'app_controller',[
        '$scope','$state','credentialsService','$ionicNavBarDelegate','$rootScope','$cookies','$ionicHistory','$ionicPopover','$ionicPopup',
        function($scope, $state,credentialsService,$ionicNavBarDelegate,$rootScope,$cookies,$ionicHistory,$ionicPopover,$ionicPopup) {
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
                $rootScope.header_links=$state.current.data.header_links;
                $rootScope.back_button=options.back_button==true;
                credentialsService.set_pss_user_credentials_from_cookies($scope.event_name);
                $scope.credentials_for_event = credentialsService.get_credentials()[$scope.event_name];                
                $rootScope.is_logged_in=credentialsService.is_logged_in($scope.event_name);
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
                history = $ionicHistory.viewHistory();
                history.back();
            };

            
            $rootScope.openPopover = function($event) {                                
                $ionicPopover.fromTemplateUrl($state.current.data.quick_links_url, {                
                    scope: $scope
                }).then(function(popover){
                    $scope.popover = popover;
                    $scope.popover.show($event);
                });
                
            };
            
            $rootScope.popoverClick = function(sref) {                                
                $scope.popover.hide();
                $scope.popover.remove();                
                $state.go(sref);                
            };            
            
            //REMEMBER ME : for later
            // $scope.generic_search = function(list_to_search,name_field_of_item,id_field_of_item,value_to_filter_for){
            //     $scope.search_results = _.filter(list_to_search,
            //              function(item) {
                             
            //                  if(_.startsWith(item[name_field_of_item],value_to_filter_for)){
            //                      return true; 
            //                  }
            //                  if(/^\d+$/.test(value_to_filter_for)){
            //                      if(item[id_field_of_item] == value_to_filter_for){
            //                          return true; 
            //                      }                                                                  
            //                  }                             
            //                  return false;
            //              });
            // };

            //REMEMBER ME : for later            
            // $scope.generic_search = function(item,index,complete_list){
            //     var name_field_of_item='';
            //     var id_field_of_item='';
            //     if(_.startsWith(item[name_field_of_item],value_to_filter_for)){
            //         return true; 
            //     }
            //     if(/^\d+$/.test(value_to_filter_for)){
            //         if(item[id_field_of_item] == value_to_filter_for){
            //             return true; 
            //         }                                                                  
            //     }                             
            //     return false;
            // };
            
        }
    ]
);

//REMEMBER ME : for later
// angular.module('app').directive('pssHeader', function($state) {
//   return {
//       restrict: 'AE',
//       replace: 'true',
//       templateUrl: 'templates/generic_header.html',
//       link: function(scope, elem, attrs) {
//           for(i in $state.current){
//               alert($state.current.name);
//           }          
//           scope.header_links = $state.data.header_links;
//     }      
//   };
// });

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
