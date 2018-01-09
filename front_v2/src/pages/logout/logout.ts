import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton';


/**
 * Generated class for the LogoutPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-logout',
  templateUrl: '../success/success.html',
})
export class LogoutPage extends PssPageComponent {
    successSummary:any = null;
    successButtons:any = null;
    
    ionViewWillLoad() {
        this.eventAuth.logout(this.eventId);
        let success_title_string='Logged out!';        
        this.successSummary = new SuccessSummary(success_title_string,null,null);            
        this.successButtons = [new SuccessButton('Go Home',
                                                this.getHomePageString(this.eventId),
                                                this.buildNavParams({}))];            
        
    }

}
