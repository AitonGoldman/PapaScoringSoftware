import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton';
import { PssApiProvider } from '../../providers/pss-api/pss-api';


/**
 * Generated class for the EventOwnerRequestPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-event-owner-request',
  templateUrl: 'event-owner-request.html',
})
export class EventOwnerRequestPage {
    userInfo:any={};
  constructor(public pssApi: PssApiProvider,
              public navCtrl: NavController,
              public navParams: NavParams              
             ) {
      
  }
    ionViewDidLoad() {
        
        console.log('ionViewDidLoad EventOwnerRequestPage');
    }
    generateEventOwnerCreateRequestProcessor(){
        return (result) => {
            if(result == null){
                return;
            }            
            let successSummary = new SuccessSummary('Request has been submitted.',
                                                    'You will recieve an email shortly with instructions',
                                                    'on how to activate your account.');
            
            let successButton = new SuccessButton('Go Home',
                                                  'EventSelectPage',
                                                  {},
                                                  null);                        
            this.navCtrl.push("SuccessPage",            
                              {'successSummary':successSummary,
                               'successButtons':[successButton]});
        };
    }    
    
    submitRequest(){
        this.pssApi.eventOwnerCreateRequest(this.userInfo)
            .subscribe(this.generateEventOwnerCreateRequestProcessor())            
    }

}
