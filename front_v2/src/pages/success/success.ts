import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { EventAuthProvider } from '../../providers/event-auth/event-auth';

/**
 * Generated class for the SuccessPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({    
    segment: 'Success/:eventId'
})
@Component({
  selector: 'page-success',
  templateUrl: 'success.html',
})
export class SuccessPage extends PssPageComponent{
    successSummary:any = null;
    successButtons:any = null;
    constructor(public navCtrl: NavController, public navParams: NavParams,
                public eventAuth: EventAuthProvider) {
       super(eventAuth,navParams);             
        this.successSummary = navParams.get('successSummary');
        this.successButtons = navParams.get('successButtons');
    }

    pushPageWithNoBackButton(pageName,navParams){        
        this.navCtrl.getActive().willLeave.subscribe(
            ()=>{
                this.navCtrl.last().showBackButton(false);
            }
        )        
        this.navCtrl.push(pageName,this.buildNavParams(navParams));
    }
  ionViewDidLoad() {
    console.log('ionViewDidLoad SuccessPage');
  }

}
