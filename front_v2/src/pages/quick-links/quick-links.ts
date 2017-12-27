import { Component } from '@angular/core';
import { App, IonicPage, NavController, NavParams } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { EventAuthProvider } from '../../providers/event-auth/event-auth';

/**
 * Generated class for the QuickLinksPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-quick-links',
  templateUrl: 'quick-links.html',
})
export class QuickLinksPage extends PssPageComponent {  
  constructor(public navCtrl: NavController,
              public navParams: NavParams,
              public appCtrl: App,              
              public eventAuth: EventAuthProvider) {
      super(eventAuth,navParams);      
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad QuickLinksPage');
  }
    goToPage(page,tabIndex) {
        if (page){
            let params = this.buildNavParams({});
            console.log(params);
            this.appCtrl.getRootNav().push(page, params);
        } else {
            this.navCtrl.parent.select(tabIndex);
        }
        
    }
}
