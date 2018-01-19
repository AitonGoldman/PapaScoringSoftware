import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
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
    tournaments:any = null;
    eventPlayer:any = null;
    generateGetAllTournamentsAndMachinesAndEventPlayerProcessor(withPlayer=false){
        return (result) => {
            if(result == null){
                return;
            }
            if(withPlayer==true){
                this.eventPlayer=result.player;
            }
            this.tournaments=result.data;
        }
    }
    
    ionViewWillLoad() {        
        if(this.playerLoggedIn==false){                        
            this.pssApi.getAllTournamentsAndMachines(this.eventId)            
                .subscribe(this.generateGetAllTournamentsAndMachinesAndEventPlayerProcessor())
        } else {
            let playerId=this.eventAuth.getEventPlayerId(this.eventId)
            this.pssApi.getAllTournamentsAndMachinesAndEventPlayer(this.eventId,playerId)            
                .subscribe(this.generateGetAllTournamentsAndMachinesAndEventPlayerProcessor(true))
        }
      
      console.log('ionViewDidLoad ResultsPage');
  }

}
