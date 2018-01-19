import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the ResultsTournamentPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment : "Results/:eventId/:eventName/:tournamentId"
})

@Component({
  selector: 'page-results-tournament',
  templateUrl: 'results-tournament.html',
})

export class ResultsTournamentPage extends PssPageComponent {
    tournamentId:number = null;
    results:any = null;
    generateGetTournamentResultsProcessor(){
        return (result) => {
            if(result == null){
                return;
            }
            this.results=result.data;
        }
    }
 
    
    ionViewWillLoad() {
        console.log('ionViewDidLoad ResultsTournamentPage');
        this.tournamentId=this.navParams.get('tournamentId');
        this.pssApi.getTournamentResults(this.eventId,this.tournamentId)            
            .subscribe(this.generateGetTournamentResultsProcessor())        
    }

}
