angular.module('TD_services.action_sheets',[]);
angular.module('TD_services.action_sheets')
    .factory('ActionSheets',
             ['$state','$timeout',
              '$ionicLoading','$ionicModal',
              '$rootScope', '$ionicActionSheet',
              function($state,$timeout,
                       $ionicLoading,$ionicModal,
                       $rootScope,$ionicActionSheet) {        
                  
                  var choose_action = function(division_id,tournament,dest_route){            
                      var hideSheet = $ionicActionSheet.show({
                          buttons: [
                              { text: 'Edit Tournament' },
                              { text: 'Activate/Deactivate Tournament' }
                          ],                    
                          titleText: 'Tournament Actions',
                          cancelText: 'Cancel',
                          cancel: function() {
                              // add cancel code..
                          },
                          buttonClicked: function(index) {
                              if(index == 0){
                                  $state.go(dest_route,{division_id:division_id});
                              }
                              if(index == 1){
                                  if(tournament.active == true){
                                      new_tournament_status=false;
                                      tournament.active=false;
                                  } else {                                
                                      new_tournament_status=true;
                                      tournament.active=true;
                                  }
                                  Modals.loading();
                                  active_promise = TimeoutResources.UpdateDivision(undefined,{site:$scope.site},{division_id:division_id,active:new_tournament_status});
                                  active_promise.then(function(data){
                                      Modals.loaded();
                                  });
                              }
                              return true;
                          }
                      });
                  };
                  var choose_change_div = function(player_info){            
                      var hideSheet = $ionicActionSheet.show({
                          buttons: [
                              { text: 'Continue' }                              
                          ],                    
                          titleText: '<h1>This will void all tickets in the old division!  Are you sure you want to do this?</h1>',
                          cancelText: 'Cancel',
                          cancel: function() {
                              player_info.linked_division_id = player_info.old_linked_division_id;
                              // add cancel code..
                          },
                          buttonClicked: function(index) {
                              return true;
                          }
                      });
                  };                  
                  var choose_player_action = function(player_id){            
                      var hideSheet = $ionicActionSheet.show({
                          buttons: [
                              { text: 'Edit Player' },
                              { text: 'View Player Info' }
                          ],                    
                          titleText: 'Player Actions',
                          cancelText: 'Cancel',
                          cancel: function() {
                              // add cancel code..
                          },
                          buttonClicked: function(index) {
                              if(index == 0){
                                  $state.go('.edit_player',{player_id:player_id});
                              }
                              if(index == 1){
                                  $state.go('.edit_player',{player_id:player_id});
                              }
                              return true;
                          }
                      });
                  };
                  var choose_ifpa_lookup_action = function(ifpa_search_results,result){            
                      buttons = [];
                      console.log(ifpa_search_results);
                      if(ifpa_search_results == "No players found"){
                          title_text = "No results returned!";
                          ifpa_search_results=[];
                      }
                      if(ifpa_search_results.length > 4){
                          title_text = "Too many results returned! Refine your search.";
                      }
                      if(ifpa_search_results.length > 0 && ifpa_search_results.length <=4){
                          for(i in ifpa_search_results){
                              button_text = ifpa_search_results[i].first_name+" "+ifpa_search_results[i].last_name+" : "+ifpa_search_results[i].wppr_rank;
                              buttons.push({result:ifpa_search_results[i],text: button_text});
                          }
                          title_text = "Choose correct player";
                      }
                      var hideSheet = $ionicActionSheet.show({
                          buttons: buttons,                    
                          titleText: title_text,
                          cancelText: 'Cancel',
                          cancel: function() {
                              // add cancel code..
                          },
                          buttonClicked: function(index) {
                              //result.rank = buttons[index].result.wppr_rank;
                              console.log(buttons[index].result.wppr_rank);
                              result.result = buttons[index].result;
                              return true;
                          }
                      });
                  };
                  
                  return {
                      choose_action:choose_action,
                      choose_player_action:choose_player_action,
                      choose_ifpa_lookup_action:choose_ifpa_lookup_action,
                      choose_change_div:choose_change_div
                  };
              }]);
