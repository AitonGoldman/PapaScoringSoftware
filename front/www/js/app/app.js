angular.module('app',['event_select','pss_admin']);
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
                $ionicNavBarDelegate.title($state.current.data.title);                                
                $rootScope.header_links=$state.current.data.header_links;
                $rootScope.back_button=options.back_button==true;
                credentialsService.set_pss_user_credentials_from_cookies("pss_admin");
                $scope.credentials_for_event = credentialsService.get_credentials()['pss_admin'];                                
            };
            
            $rootScope.pss_admin_logout = function(){
                credentialsService.remove_credentials_on_logout("pss_admin");
                $state.go('app.pss_admin.login');
            };
            
            $scope.disable_back_button = function(){
                $rootScope.back_button=false;
            };
            
            $rootScope.go_back = function(){
                history = $ionicHistory.viewHistory();
                history.back();
            };

            var template = '<ion-popover-view><ion-header-bar> <h1 class="title">Quick Links</h1> </ion-header-bar> <ion-content> <div class="list"><div class="item" ng-click="popoverClick()">Event Select</div></div></ion-content></ion-popover-view>';

            var template_intro = '<ion-popover-view><ion-header-bar> <h1 class="title">Use Me!</h1> </ion-header-bar> <ion-content> Click on this icon to get quick links</ion-content></ion-popover-view>';            
            $scope.popover = $ionicPopover.fromTemplate(template, {                
                scope: $scope
            });
            $scope.popover_intro = $ionicPopover.fromTemplate(template_intro, {                
                scope: $scope
            });

            
            $rootScope.openPopover = function($event) {                
                for(i in $event){
                    console.log(i+":"+$event[i]);
                }                
                $scope.popover.show($event);
            };
            $rootScope.openPopoverOnLogin = function(){                
                $ionicPopup.alert({
                    title:"Use Quicklinks!",
                    template:"<center>use the papa icon<br> <img class='mobile_logo_small' src='http://papa.org/wp-content/uploads/PAPAmenulogo1.png'><br>for quick navigation</center>"
                });
                //var quickLinks = document.getElementById('desktopQuickLinks');
                //var test = ionic.DomUtil.getPositionInParent(quickLinks);
                //console.log(test);   
                //$scope.popover_intro.show(quickLinks);                
            };
            $rootScope.popoverClick = function(sref) {                                
                $scope.popover.hide();
                $state.go("app.event_select");                
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
