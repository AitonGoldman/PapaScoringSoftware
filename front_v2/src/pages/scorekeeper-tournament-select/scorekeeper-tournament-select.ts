import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the ScorekeeperTournamentSelectPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
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
            let tournaments=result.data;
            tournaments.map((tournament)=>{
                tournament.expanded=false;
            })
            this.tournaments=tournaments.sort((n1,n2)=>{
                if(n1.tournament_name < n2.tournament_name){
                    return -1;
                }
                if(n1.tournament_name > n2.tournament_name){
                    return 1;
                }
                return 0;                
            })

        };
    }
    

  ionViewWillLoad() {
        if(this.eventId==null){
            this.pushRootPage('EventSelectPage')
            return;
        }

      this.pssApi.getAllTournaments(this.eventId)
          .subscribe(this.generateGetAllTournamentsProcessor())    

      console.log('ionViewDidLoad ScorekeeperTournamentSelectPage');
  }

}
