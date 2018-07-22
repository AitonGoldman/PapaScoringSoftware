import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { ScorekeeperFinalsRoundPage } from '../../pages/scorekeeper-finals-round/scorekeeper-finals-round'

/**
 * Generated class for the ResultsFinalsRoundsPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-results-finals-rounds',
  templateUrl: 'results-finals-rounds.html',
})
export class ResultsFinalsRoundsPage extends ScorekeeperFinalsRoundPage{
    roundDescriptions:any = {1:'Round 1',2:'Round 2',3:'Semi Finals',4:'Quarter Finals',5:'Final 4'}  
  ionViewDidLoad() {
    console.log('ionViewDidLoad ResultsFinalsRoundsPage');
  }

}
