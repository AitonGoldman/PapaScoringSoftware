angular.module('event_tournament_lib',[]);
angular.module('event_tournament_lib')
    .factory('eventTournamentLib',
             ['resourceWrapperService','$state','$ionicActionSheet',function(resourceWrapperService,$state,$ionicActionSheet) {
                 var on_get_tournament_event_success = function(data){                    
                     var item=data['item'];
                     var orig_item_fields=[];
                     for(i in item){
                         orig_item_fields.push(i);
                     }
                     item.bobo={};
                     for(idx in orig_item_fields){
                         field_name = orig_item_fields[idx];
                         item.bobo[field_name]=item[field_name];
                     }
                     var descriptions=data['descriptions'];                                          
                     return [descriptions,item];
                 };
                 //FIXME : toggle_item_active and remove_item should be in listGeneration
                 var toggle_item_active = function(item,event_name){
                     var id;
                     var rest_route;
                     event_name=$state.params.event_name;
                     //FIXME : building the rest_route and getting the appropriate id needs to be done better
                     if(item.tournament_id==undefined){
                         id=item.event_id;
                         rest_route='put_edit_event';                         
                     }
                     if(item.tournament_id!=undefined && item.tournament_machine_id==undefined){
                         id=item.tournament_id;
                         rest_route='put_edit_tournament';                         
                     }
                     if(item.tournament_id!=undefined && item.tournament_machine_id!=undefined){
                         id=item.tournament_machine_id;
                         rest_route='put_edit_tournament_machine';                         
                     }
                     
                     var on_success = function(data){
                         item.active=data['item'].active;
                         if(item.active == true){                        
                             //item.icon='ion-play';
                             item.material_icon='play_circle_outline';
                             item.icon_color='green';
                         } else {                        
                             //item.icon='ion-stop';
                             item.material_icon='pause_circle_filled';
                             item.icon_color='red';                             
                         }                                              
                     };
                     
                     var new_state=item.active!=true;
                     var prom =resourceWrapperService.get_wrapper_with_loading(rest_route,on_success,{id:id,event_name:event_name},{active:new_state});                        
                     
                 };
                 var remove_item = function(item){
                     var hideSheet = $ionicActionSheet.show({
                         destructiveText: 'Remove Machine',
                         titleText: 'Are you SURE you want to remove this machine?',
                         cancelText: 'Cancel',
                         cancel: function() {
                             // add cancel code..
                         },
                         buttonClicked: function(index) {                    
                             return true;
                         },
                         destructiveButtonClicked: function(index){
                             rest_remove_item(item,$state.params.event_name);
                             hideSheet();
                         }
                     });
                 
                     var rest_remove_item = function(item,event_name){
                         var id;
                         var rest_route;
                         event_name=$state.params.event_name;
                         //FIXME : building the rest_route and getting the appropriate id needs to be done better
                         if(item.tournament_id!=undefined && item.tournament_machine_id!=undefined){
                             id=item.tournament_machine_id;
                             rest_route='put_edit_tournament_machine';                         
                         }
                     
                         var on_success = function(data){
                             item.actions_ui_sref_list=undefined;
                             item.actions_ng_click_list=undefined;                         
                         };
                                          
                         var prom =resourceWrapperService.get_wrapper_with_loading(rest_route,on_success,{id:id,event_name:event_name},{removed:true});                                             
                     };
                 };                 
                 return {
                     toggle_item_active:toggle_item_active,
                     on_get_tournament_event_success:on_get_tournament_event_success,
                     remove_item:remove_item
                 };
             }
             ]
            );
