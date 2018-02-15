import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton'


/**
 * Generated class for the EventOwnerConfirmPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-event-owner-confirm',
  templateUrl: '../../pages/success/success.html',
})
export class EventOwnerConfirmPage extends PssPageComponent{    
    successSummary:any = null;
    successButtons:any = [];    
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

  ionViewWillLoad() {
      console.log('ionViewDidLoad EventOwnerConfirmPage');
      if(this.eventId==null){
          this.pushRootPage('EventSelectPage')
          return;
      }

      let encodedString:string = this.navParams.get('itsdangerousstring');
      this.successSummary = new SuccessSummary('Activating Account....',
                                               null,
                                               null);
            
      if(encodedString){
          this.pssApi.eventOwnerCreateConfirm({},encodedString)
              .subscribe(this.generatePssUserConfirm())            
          
      }else{
            
      }
      
  }

}
