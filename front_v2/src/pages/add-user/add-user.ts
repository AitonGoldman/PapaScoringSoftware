import { ViewChild, Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { AutoCompleteComponent } from '../../components/auto-complete/auto-complete'

/**
 * Generated class for the AddUserPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'AddUser/:eventId'
})
@Component({
  selector: 'page-add-user',
  templateUrl: '../../components/add-user/add-user.html',
})
export class AddUserPage extends AutoCompleteComponent {
    
    @ViewChild('searchbar')  searchbar: any;
    @ViewChild('myForm')  myForm: any;
    displayExistingUserNotFound:boolean = null;
    selectedUser:any = null;
    newUserName:string=null;    
    users:any;
    roles:any=[];
    selectedRole:any=null;
    loading:boolean = false;
    
    generateGetAllUsersProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }
            this.users=result.data;
            console.log('in GetAllUsersProcessor...');
            console.log(result);
            this.autoCompleteProvider.initializeAutoComplete('full_user_name',
                                                             this.users,
                                                             this.generateItemsLoadingFunction());      

            //this.autoCompleteProvider.setUsers(result.data);
            this.roles=result.roles;
        };
    }

    generateAddEventUsersProcessor(user_full_name,role_name){
        return (result) => {            
            if(result == null){
                return;
            }
            let user_already_exists = this.users.filter((user)=>{
                return user.pss_user_id==result.data.pss_user_id
            }).length;
            if(user_already_exists==0){                
                this.users.push(result.data[0]);                
            }
            let message_string=user_full_name+" is a "+role_name+" in the event."
                let toast = this.toastCtrl.create({
                    message:  message_string,
                    duration: 99000,
                    position: 'top',
                    showCloseButton: true,
                    closeButtonText: " ",
                    cssClass: "successToast"
                });
                toast.present();                

            
            //toast here
        };
    }
    
    ionViewWillLoad() {
        console.log('ionViewDidLoad EventOwnerAddUserPage');        
        this.pssApi.getAllUsers()
            .subscribe(this.generateGetAllUsersProcessor())        
    }
    onInput(event){        
        console.log('in oninput...')
        //this.onAutocompleteInput(event);
        if(this.searchbar.suggestions.length==0){                        
            this.newUserName=event;
        } 
        
    }
    doesEventRolesMatchEvent(eventId,roles){
        return roles.filter((role)=>{return Number(eventId)==role.event_id}).length>0
    }
    onSelect(event){
        console.log('in onselect...');
        
        //        if(this.doesEventRolesMatchEvent(this.eventId,this.selectedUser.event_roles)){
        if(this.doesEventRolesMatchEvent(this.eventId,this.selectedPlayer.event_roles)){        
            this.displayExistingUserNotFound=false;
            console.log('already there...');
            //            let message_string=this.selectedUser.full_user_name+" is already registered for this event."
            let message_string=this.selectedPlayer.full_user_name+" is already registered for this event."            
                let toast = this.toastCtrl.create({
                    message:  message_string,
                    duration: 99000,
                    position: 'top',
                    showCloseButton: true,
                    closeButtonText: " ",
                    cssClass: "dangerToast"
                });
                toast.present();                


            return;
        }
        //FIXME : need to add new user to list of users searched
        //        if(!this.doesEventRolesMatchEvent(this.eventId,this.selectedUser.event_roles)){
        if(!this.doesEventRolesMatchEvent(this.eventId,this.selectedPlayer.event_roles)){        
            this.displayExistingUserNotFound=false;
            //            this.pssApi.addEventUsers({event_users:[this.selectedUser],
            this.pssApi.addEventUsers({event_users:[this.selectedPlayer],            
                                       event_role_ids:[this.selectedRole.event_role_id]},
                                      this.eventId)
            //                .subscribe(this.generateAddEventUsersProcessor(this.selectedUser.full_user_name,this.selectedRole.event_role_name));
                .subscribe(this.generateAddEventUsersProcessor(this.selectedPlayer.full_user_name,this.selectedRole.event_role_name));                        
            return;
        }             

        this.displayExistingUserNotFound=false;
        
        
    }
    onFocus(){
        //this.selectedUser=null;
        this.selectedPlayer=null;        
        //this.existingUserFound=true;
    }
    onSubmit(name_string){
        this['existingUserFound']=true;
        this.pssApi.addEventUsers({event_users:[this.parseOutFirstLastNames(name_string)],event_role_ids:[this.selectedRole.event_role_id]},this.eventId)
           .subscribe(this.generateAddEventUsersProcessor(name_string,this.selectedRole.event_role_name))
            
        
    }
    parseOutFirstLastNames(name_string){
        let name_elements = name_string.split(" ");
        return {
            first_name:name_elements[0],
            last_name:name_elements[1],
            username:name_elements[0]+name_elements[1]
        };
    }   
}
