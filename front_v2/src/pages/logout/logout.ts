import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
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
    cssColors:string = null;
    ionViewWillLoad() {
        if(this.eventId==null){
            this.pushRootPage('EventSelectPage')
            return;
        }

        this.eventAuth.logout(this.eventId);
        let success_title_string='Logged out!';
        let targetTabIndex=null;
        if(this.platform.is('mobile')){
            console.log('going mobile')
            targetTabIndex=0;
        }                    
        this.successSummary = new SuccessSummary(success_title_string,null,null);
        if(this.platform.is('core')){
            this.successSummary.setCssColors('desktop');
        } else {
            this.successSummary.setCssColors('quick-links');
        }

        if(this.platform.is('core')){
            this.cssColors='desktop';
        } else {
            this.cssColors='quick-links';
            
        }
        
        this.cssColors='quick-links'
        this.successButtons = [new SuccessButton('Go Home',
                                                 this.getHomePageString(this.eventId),
                                                 this.buildNavParams({}),
                                                 targetTabIndex)];            
        
    }

}
