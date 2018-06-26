import { ViewChild, Component } from '@angular/core';
import { AutoCompleteComponent } from '../../components/auto-complete/auto-complete';
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton';
import { IonicPage } from 'ionic-angular';

/**
 * Generated class for the EditUserPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-edit-user',
  templateUrl: 'edit-user.html',
})
export class EditUserPage extends AutoCompleteComponent {
    @ViewChild('searchbar')  searchbar: any;    
    destPageAfterSuccess:any=null;
    users:any;
    roles:any=[];
    selectedRole:any=null;
    selectedUser:any=null;
    newPassword:any=null;
    // constructor(public autoCompleteProvider:AutoCompleteProvider,
    //             public eventAuth: EventAuthProvider,
    //             public navParams: NavParams,
    //             public navCtrl: NavController,
    //             public appCtrl: App,
    //             public pssApi: PssApiProvider,
    //             public platform: Platform,                
    //             public actionSheetCtrl: ActionSheetController,
    //             //public notificationsService: NotificationsService
    //             public toastCtrl: ToastController
    //            ){
    //     super(eventAuth,navParams,
    //           navCtrl,appCtrl,
    //           pssApi,platform,
    //           //notificationsService,
    //           toastCtrl,
    //           actionSheetCtrl);
    // }

    generateEditEventUserPasswordProcessor(){
        return (result) => {
            if(result == null){
                return;
            }
            let success_title_string='User '+this.selectedUser.full_user_name+' has been changed.';
            let successSummary = new SuccessSummary(success_title_string,null,null);            
            let successButton = new SuccessButton('Go Home',
                                                  this.getHomePageString(),
                                                  this.buildNavParams({}));            
            this.navCtrl.push("SuccessPage",            
                              this.buildNavParams({'successSummary':successSummary,
                                                   'successButtons':[successButton]}));
        };

    }
    
    generateEditEventUserRoleProcessor(removedEventUserFromEvent){
        return (result) => {
            if(result == null){
                return;
            }
            let success_title_string='User '+this.selectedUser.full_user_name+' has been changed.';
            let successSummary = new SuccessSummary(success_title_string,null,null);            
            let successButton = new SuccessButton('Go Home',
                                                  this.getHomePageString(),
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
        if(this.eventId==null){
            this.pushRootPage('EventSelectPage')
            return;
        }

        console.log('ionViewDidLoad EditUserPage');
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
        console.log('SELETED USER WHILE EDITING');
        console.log(this.selectedUser);
        this.pssApi.editEventUserRole({'event_user':this.selectedUser,'event_role_ids':modifiedRoles},this.eventId)
            .subscribe(this.generateEditEventUserRoleProcessor(removeEventUserFromEvent));
        
    }
    
    onSubmitPassword(){
        this.selectedUser.new_password=this.newPassword;
        this.pssApi.editEventUserPassword({'event_user':this.selectedUser},this.eventId)
            .subscribe(this.generateEditEventUserPasswordProcessor());
        
    }
    
    onFocus(){
        this.selectedUser=null;                
    }
}
