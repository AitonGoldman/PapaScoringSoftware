import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the SuccessPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-success',
  templateUrl: 'success.html',
})
export class SuccessPage extends PssPageComponent{
    successSummary:any = null;
    successButtons:any = null;
    postAddPlayerSuccess:boolean = false;
    // pushPageWithNoBackButton(pageName,navParams){        
    //     this.navCtrl.getActive().willLeave.subscribe(
    //         ()=>{
    //             this.navCtrl.last().showBackButton(false);
    //         }
    //     )        
    //     this.navCtrl.push(pageName,this.buildNavParams(navParams));
    // }
  ionViewWillLoad() {
        if(this.eventId==null){
            this.pushRootPage('EventSelectPage')
            return;
        }

      this.successSummary = this.navParams.get('successSummary');
      this.successButtons = this.navParams.get('successButtons');
      console.log('ionViewDidLoad SuccessPage');
  }
    goToEventSelectOnPageReload(){
      this.appCtrl.getRootNav().push('EventSelectPage');        
    }
}
