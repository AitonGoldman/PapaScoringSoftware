angular.module('list_generation',[]);
angular.module('list_generation')
    .factory('listGeneration',
             [function() {
                 var toggle_view_item_actions = function(item){
                     if(item.display_actions==undefined){
                         item.display_actions=true;
                         return;
                     }
                     item.display_actions=item.display_actions==false;
                 };
                 var generate_set_list_items_ui_sref_and_args = function(sref,display_label_field){
                     var set_list_items_ui_sref_and_args = function(i) {                                     
                         i.ui_sref=sref;
                         i.label_to_display=i[display_label_field];                
                     };
                     return set_list_items_ui_sref_and_args;
                 };

                 var build_action_ui_sref = function(label,ui_sref){
                     return {label:label,ui_sref:ui_sref};
                 };
                 
                 var build_action_ng_click = function(label,ng_click){
                     return {label:label,ng_click:ng_click};
                 };

                 var add_action_ui_sref_to_item = function(item,action){
                     if(item.actions_ui_sref_list==undefined){
                         item.actions_ui_sref_list=[];
                     }
                     item.actions_ui_sref_list.push(action);
                 };
                 var add_action_ng_click_to_item = function(item,action){
                     if(item.actions_ng_click_list==undefined){
                         item.actions_ng_click_list=[];
                     }
                     item.actions_ng_click_list.push(action);
                 };

                 var generate_tournament_machine_actions = function(display_label_field){
                     var set_actions = function(i){
                         //i.actions_ui_sref_list=[];                         
                         i.label_to_display=i[display_label_field];
                         add_action_ng_click_to_item(i,
                                                     build_action_ng_click('Toggle Active','toggle_item_active(item,event_name)'));
                         add_action_ng_click_to_item(i,
                                                     build_action_ng_click('Remove Machine','remove_item(item,event_name)'));                         
                     };
                     return set_actions;
                 };
                 
                 //needs some cleaning up
                 var generate_set_list_items_actions_and_args = function(display_label_field,
                                                                         advanced_sref,
                                                                         basic_sref,                                                                         
                                                                         display_active_toggle) {
                     var set_list_items_actions_and_args = function(i) {                                                              
                         i.label_to_display=i[display_label_field];
                         if(display_active_toggle==undefined||display_active_toggle==true){
                             add_action_ng_click_to_item(i,
                                                         build_action_ng_click('Toggle Active','toggle_item_active(item,event_name)'));
                         }                                                  
                         //add_action_ui_sref_to_item(i,
                         //build_action_ui_sref('Advanced Editing',advanced_sref));
                         add_action_ui_sref_to_item(i,
                                                    build_action_ui_sref('Basic Editing',basic_sref));
                     };             
                     return set_list_items_actions_and_args;
                 };

                 var set_add_machine_action = function(i){                     
                     add_action_ui_sref_to_item(i,
                                                build_action_ui_sref('Add Machines','.add_tournament_machine({tournament_id:item.tournament_id})'));
                };                

                 
                 var set_active_inactive_icon = function(i){                     
                     if(i.active == undefined){                                                
                        return;                        
                    }
                    if(i.active == true){                        
                        //i.icon='ion-play';
                        i.material_icon='play_circle_outline';
                        i.icon_color='green';
                    } else {                        
                        //i.icon='ion-stop';
                        i.material_icon='pause_circle_filled';
                        i.icon_color='red';
                    }                     
                 };

                 return {
                     generate_set_list_items_ui_sref_and_args:generate_set_list_items_ui_sref_and_args,
                     toggle_view_item_actions:toggle_view_item_actions,
                     generate_set_list_items_actions_and_args:generate_set_list_items_actions_and_args,
                     set_active_inactive_icon:set_active_inactive_icon,
                     generate_tournament_machine_actions:generate_tournament_machine_actions,
                     set_add_machine_action:set_add_machine_action
                 };
             }
             ]
            );
