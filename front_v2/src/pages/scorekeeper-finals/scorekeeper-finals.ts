import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the ScorekeeperFinalsPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-scorekeeper-finals',
  templateUrl: 'scorekeeper-finals.html',
})
export class ScorekeeperFinalsPage  extends PssPageComponent{
    finalId:number=null;        
    
    ionViewWillLoad() {
        if(this.eventId==null){
            this.pushRootPage('EventSelectPage')
            return;
        }

        this.finalId=this.navParams.get('finalId');
        console.log('ionViewDidLoad ScorekeeperFinalsRoundPage');
    }

}
