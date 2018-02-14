import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the ResultsFinalsPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-results-finals',
  templateUrl: 'results-finals.html',
})
export class ResultsFinalsPage extends PssPageComponent{
    finalId:number=null;        
    
    ionViewWillLoad() {
        if(this.eventId==null){
            this.pushRootPage('EventSelectPage')
            return;
        }

        this.finalId=this.navParams.get('finalId');        
    }
}
