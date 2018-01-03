import { ViewChild, Component } from '@angular/core';
import { PssPageComponent } from '../pss-page/pss-page'
import { AutoCompleteProvider } from '../../providers/auto-complete/auto-complete';
import { Platform, App, NavParams, NavController } from 'ionic-angular';
import { EventAuthProvider } from '../../providers/event-auth/event-auth';
import { PssApiProvider } from '../../providers/pss-api/pss-api';
import { ToastController } from 'ionic-angular';
import { ActionSheetController } from 'ionic-angular'
import { NotificationsService } from 'angular2-notifications';

/**
 * Generated class for the AddUserComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */
@Component({
  selector: 'add-user',
  templateUrl: 'add-user.html'
})
export class AddUserComponent extends PssPageComponent{
  
    @ViewChild('searchbar')  searchbar: any;
    @ViewChild('myForm')  myForm: any;
    existingUserFound:boolean = true;
    selectedUser:any = {};
    newUserName:string=null;    
    users:any;
    roles:any=[];
    selectedRole:any=null;
    
    constructor(public autoCompleteProvider:AutoCompleteProvider,
                public eventAuth: EventAuthProvider,
                public navParams: NavParams,
                public navCtrl: NavController,
                public appCtrl: App,
                public pssApi: PssApiProvider,
                public platform: Platform,
                private toastCtrl: ToastController,
                public actionSheetCtrl: ActionSheetController,
                public notificationsService: NotificationsService ){
        super(eventAuth,navParams,
              navCtrl,appCtrl,
              pssApi,platform,
              notificationsService)
    }
    generateGetAllUsersProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }
            this.users=result.data;
            this.autoCompleteProvider.setUsers(result.data);
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
            this.notificationsService.success("Success", message_string,{
                timeOut:0,
                position:["top","right"],
                theClass:'poop'
            })
            
            //toast here
        };
    }
    
    ionViewWillLoad() {
        console.log('ionViewDidLoad EventOwnerAddUserPage');
        this.pssApi.getAllUsers()
            .subscribe(this.generateGetAllUsersProcessor())            
    }
    onInput(event){        
        
        if(this.searchbar.suggestions.length==0){
            this.existingUserFound=false;
            this.newUserName=event;
        } else {
            this.existingUserFound=true;
        }
        console.log(this.selectedUser);
    }
    onSelect(event){
        console.log('in onselect...');
        console.log(this.eventId);
        if(this.selectedUser.events.includes(Number(this.eventId))){
            this.existingUserFound=true;
            let message_string=this.selectedUser.full_user_name+" is already registered for this event."
            this.notificationsService.warn("Warning", message_string,{
                timeOut:0,
                position:["top","right"],
                theClass:'poop'
            })

            return;
        }
        //FIXME : need to add new user to list of users searched
        if(!this.selectedUser.events.includes(Number(this.eventId))){
            this.existingUserFound=true;
            this.pssApi.addEventUsers({event_users:[this.selectedUser],
                                       event_role_ids:[this.selectedRole.event_role_id]},
                                      this.eventId)
                .subscribe(this.generateAddEventUsersProcessor(this.selectedUser.full_user_name,this.selectedRole.event_role_name));            
            return;
        }             

        this.existingUserFound=true
        
        
    }
    onFocus(){
        this.selectedUser={};        
        this.existingUserFound=true;
    }
    onSubmit(name_string){
        this.existingUserFound=true;
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
