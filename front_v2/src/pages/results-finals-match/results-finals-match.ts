import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { ScorekeeperFinalsMatchPage } from '../../pages/scorekeeper-finals-match/scorekeeper-finals-match'

/**
 * Generated class for the ResultsFinalsMatchPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-results-finals-match',
  templateUrl: 'results-finals-match.html',
})
export class ResultsFinalsMatchPage extends ScorekeeperFinalsMatchPage {

  ionViewDidLoad() {
    console.log('ionViewDidLoad ResultsFinalsMatchPage');
  }
    numToString(num){
        if(num==1){
            return "one";
        }
        if(num==2){
            return "two";
        }
        if(num==3){
            return "three";
        }
        if(num==4){
            return "four";
        }
        
    }
}
