import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'


/**
 * Generated class for the TournamentDirectorHomePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-tournament-director-home',
  templateUrl: 'tournament-director-home.html',
})
export class TournamentDirectorHomePage extends PssPageComponent {
    tournaments:any = [];

    generateGetAllTournamentsProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }
            this.tournaments=result.data;
            this.tournamentSettings.setTournaments(result.data);
            this.tournaments.map((tournament)=>{
                tournament.expanded=false;
            })

        };
    }
    

    ionViewWillEnter() {
        if(this.eventId==null){
            this.pushRootPage('EventSelectPage')
            return;
        }

        this.pssApi.getAllTournaments(this.eventId)
            .subscribe(this.generateGetAllTournamentsProcessor())    

        console.log('ionViewDidLoad TournamentDirectorHomePage');
    }
    ionViewWillUnload() {
        console.log('ionViewWillUnLoad TournamentDirectorHomePage');
    }

}
