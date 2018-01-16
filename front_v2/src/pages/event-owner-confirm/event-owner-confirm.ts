import { EventAuthProvider } from '../../providers/event-auth/event-auth';
import { NotificationsService } from 'angular2-notifications';
import { ToastController } from 'ionic-angular';
import { Component } from '@angular/core';
import { App, IonicPage, NavController, NavParams, Platform } from 'ionic-angular';
import { PssApiProvider } from '../../providers/pss-api/pss-api';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton'
import { ActionSheetController } from 'ionic-angular'

/**
 * Generated class for the EventOwnerConfirmPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'EventOwnerConfirm/:itsdangerousstring'
})
@Component({
  selector: 'page-event-owner-confirm',
  templateUrl: '../../pages/success/success.html',
})
export class EventOwnerConfirmPage extends PssPageComponent{    
    successSummary:any = null;
    successButtons:any = [];    
    constructor(public navCtrl: NavController,
                public navParams: NavParams,                
                public eventAuth: EventAuthProvider,
                public appCtrl: App,
                public pssApi: PssApiProvider,
                public platform: Platform,
                //public notificationsService: NotificationsService,
                public toastCtrl: ToastController,
               public actionSheetCtrl: ActionSheetController) {
        super(eventAuth,navParams,
              navCtrl,appCtrl,
              pssApi,platform,
              //notificationsService,
              toastCtrl,
              actionSheetCtrl);
        let encodedString:string = navParams.get('itsdangerousstring');
        this.successSummary = new SuccessSummary('Activating Account....',
                                                 null,
                                                 null);
            
        if(encodedString){
            this.pssApi.eventOwnerCreateConfirm({},encodedString)
                .subscribe(this.generatePssUserConfirm())            
            
        }else{
            
        }
    }
    generatePssUserConfirm(){
        return (result)=>{
            if(result==null){
                return;
            }
            this.successSummary = new SuccessSummary('Account Activated!',
                                                     'Click on the button below to go to the login screen',
                                                     null);
            
            this.successButtons = [new SuccessButton('Go To Login Page',
                                                     'EventOwnerLoginPage',
                                                     {},
                                                     null)];                        
        }
    }

  ionViewDidLoad() {
    console.log('ionViewDidLoad EventOwnerConfirmPage');
  }

}
