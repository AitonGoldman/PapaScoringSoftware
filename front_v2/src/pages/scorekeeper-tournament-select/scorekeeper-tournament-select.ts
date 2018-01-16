import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the ScorekeeperTournamentSelectPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:"ScorekeeperTournamentSelect/:eventId"
})
@Component({
  selector: 'page-scorekeeper-tournament-select',
  templateUrl: 'scorekeeper-tournament-select.html',
})
export class ScorekeeperTournamentSelectPage extends PssPageComponent{
    tournaments:any = null;
    
    generateGetAllTournamentsProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }
            this.tournaments=result.data;
            this.tournaments.map((tournament)=>{
                tournament.expanded=false;
            })

        };
    }
    

  ionViewWillLoad() {
      this.pssApi.getAllTournaments(this.eventId)
          .subscribe(this.generateGetAllTournamentsProcessor())    

      console.log('ionViewDidLoad ScorekeeperTournamentSelectPage');
  }

}
