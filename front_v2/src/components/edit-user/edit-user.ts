import { ViewChild, Component } from '@angular/core';
import { PssPageComponent } from '../pss-page/pss-page'
import { AutoCompleteProvider } from '../../providers/auto-complete/auto-complete';
import { Platform, App, NavParams, NavController } from 'ionic-angular';
import { EventAuthProvider } from '../../providers/event-auth/event-auth';
import { PssApiProvider } from '../../providers/pss-api/pss-api';

import { ActionSheetController } from 'ionic-angular'
import { NotificationsService } from 'angular2-notifications';
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton';

/**
 * Generated class for the EditUserComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */
@Component({
  selector: 'edit-user',
  templateUrl: 'edit-user.html'
})
export class EditUserComponent extends PssPageComponent{
    @ViewChild('searchbar')  searchbar: any;    
    destPageAfterSuccess:any=null;
    users:any;
    roles:any=[];
    selectedRole:any=null;
    selectedUser:any=null;

    constructor(public autoCompleteProvider:AutoCompleteProvider,
                public eventAuth: EventAuthProvider,
                public navParams: NavParams,
                public navCtrl: NavController,
                public appCtrl: App,
                public pssApi: PssApiProvider,
                public platform: Platform,                
                public actionSheetCtrl: ActionSheetController,
                public notificationsService: NotificationsService){
        super(eventAuth,navParams,
              navCtrl,appCtrl,
              pssApi,platform,
              notificationsService);
    }
    generateEditEventUserRoleProcessor(removedEventUserFromEvent){
        return (result) => {
            if(result == null){
                return;
            }
            let success_title_string='User '+this.selectedUser.full_user_name+' has been changed.';
            let successSummary = new SuccessSummary(success_title_string,null,null);            
            let successButton = new SuccessButton('Go Home',
                                                  this.destPageAfterSuccess,
                                                  this.buildNavParams({}));            
            this.navCtrl.push("SuccessPage",            
                              this.buildNavParams({'successSummary':successSummary,
                                                   'successButtons':[successButton]}));
        };
    }

    filterUsersForEvent = (user)=>{
        if(user.event_roles.length==0){
            return false;
        }
        let valid_roles=user.event_roles.filter((event_role)=>{
            return event_role.event_id==this.eventId
        })
        if(valid_roles.length==0){
            return false;
        }
        return true;
    }
    
    generateGetAllUsersProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }
            this.users=result.data.filter(this.filterUsersForEvent);
            this.autoCompleteProvider.setUsers(this.users);
            this.roles=result.roles;            
        };
    }
    
    ionViewWillLoad() {
        console.log('ionViewDidLoad EventOwnerAddUserPage');
        this.pssApi.getAllUsers()
            .subscribe(this.generateGetAllUsersProcessor())            
    }
    onSelect(event){
        
        this.selectedRole=this.selectedUser.event_roles[0].event_role_id
        //this.pssApi.getEventUser(this.eventId,this.selectedUser.pss_user_id)
        //    .subscribe(this.generateGetEventUserProcessor());            

    }
    onSubmit(removeEventUserFromEvent){
        let modifiedRoles=[]
        if(removeEventUserFromEvent!=true){            
            modifiedRoles.push(this.selectedRole)            
        }
        
        this.pssApi.editEventUserRole({'event_user':this.selectedUser,'event_role_ids':modifiedRoles},this.eventId)
            .subscribe(this.generateEditEventUserRoleProcessor(removeEventUserFromEvent));
        
    }
    onFocus(){
        this.selectedUser=null;                
    }
    
}
