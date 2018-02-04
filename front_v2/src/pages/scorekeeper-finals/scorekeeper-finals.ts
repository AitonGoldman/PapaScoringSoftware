import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the ScorekeeperFinalsPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'ScorekeeperFinals/:eventId/:finalId'
})
@Component({
  selector: 'page-scorekeeper-finals',
  templateUrl: 'scorekeeper-finals.html',
})
export class ScorekeeperFinalsPage  extends PssPageComponent{
    finalId:number=null;        
    
    ionViewWillLoad() {
        this.finalId=this.navParams.get('finalId');
        console.log('ionViewDidLoad ScorekeeperFinalsRoundPage');
    }

}
