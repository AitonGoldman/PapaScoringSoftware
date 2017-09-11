angular.module('app',['event_select','pss_admin']);
angular.module('app').controller(
    'app_controller',[
        '$scope','$state','credentialsService','$ionicNavBarDelegate','$rootScope','$cookies','$ionicHistory',
        function($scope, $state,credentialsService,$ionicNavBarDelegate,$rootScope,$cookies,$ionicHistory) {
            if ($rootScope.credentials == undefined){
                $rootScope.credentials=credentialsService;
            }
            $scope.test_alert = function(message){
                alert(message);
            };
            $scope.bootstrap = function(back_button){
                //FIXME : rely on cookies to tell us if we are logged in after page reload                
                $scope.state = $state;
                $ionicNavBarDelegate.title($state.current.data.title);                                
                $rootScope.header_links=$state.current.data.header_links;
                $rootScope.back_button=(back_button==true||back_button==undefined);
                //$rootScope.back_button=true;                
            };
            $rootScope.test_back = function(){
                history = $ionicHistory.viewHistory();
                for(i in history){
                    console.log(i);    
                }
                history.back();
                //console.log(history.back());
                
                //$ionicHistory.goBack();
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
