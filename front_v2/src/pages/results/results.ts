import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the ResultsPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

// results home : shows links for tournament and machines 
// -- need endpoint that will also get tournaments and machines I have played if I am logged in as a player
// -- shows tournaments I have played in first, then others
// -- allows for expanding the list of machines on this page?

@IonicPage({
    segment : "Results/:eventId/:eventName"
})
@Component({
  selector: 'page-results',
  templateUrl: 'results.html',
})
export class ResultsPage extends PssPageComponent {
    playerLoggedIn:boolean = false;
    tournaments:any = [];
    eventPlayer:any = null;    
    doneLoading:boolean = false;
    generateGetAllTournamentsAndMachinesAndEventPlayerProcessor(withPlayer=false){
        return (result) => {
            if(result == null){
                return;
            }
            if(withPlayer==true){
                this.eventPlayer=result.player;
            }
            console.log('in processor...')
            console.log(result)
            let tournaments=result.data.map((tournament)=>{
                tournament.expand_machines=false;
                tournament.tournament_machines = tournament.tournament_machines.sort((n1,n2)=>{
                    if(n1.tournament_machine_name < n2.tournament_machine_name){
                        return -1;
                    }
                    if(n1.tournament_machine_name > n2.tournament_machine_name){
                        return 1;
                    }
                    return 0;                                    
                })
                return tournament;
            });
            this.tournaments=tournaments.sort((n1,n2)=>{
                if(n1.tournament_name < n2.tournament_name){
                    return -1;
                }
                if(n1.tournament_name > n2.tournament_name){
                    return 1;
                }
                return 0;                
            })
            this.tournamentSettings.setTournaments(this.tournaments);
        }
    }

    expandMachines(tournament){
        tournament.expand_machines=tournament.expand_machines==false;
    }
    
    ionViewDidEnter() {
        this.doneLoading=true;
    }        
   
    ionViewWillEnter() {        
        
        if(this.playerLoggedIn==false){
            console.log('----------eventId is '+this.eventId)
            this.pssApi.getAllTournamentsAndMachines(this.eventId)            
                .subscribe(this.generateGetAllTournamentsAndMachinesAndEventPlayerProcessor())
        } else {
            let playerId=this.eventAuth.getEventPlayerId(this.eventId)
            console.log('player id is '+playerId+' and eventId is '+this.eventId)
            this.pssApi.getAllTournamentsAndMachinesAndEventPlayer(this.eventId,playerId)            
                .subscribe(this.generateGetAllTournamentsAndMachinesAndEventPlayerProcessor(true))
        }
      
      console.log('ionViewDidLoad ResultsPage');
  }

}
