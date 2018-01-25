import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { PssApiProvider } from '../../providers/pss-api/pss-api';

/*
  Generated class for the TournamentSettingsProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class TournamentSettingsProvider {
    tournaments:any = null;
    tournamentMachines:any = null;
    
    constructor(public http: HttpClient, public pssApi: PssApiProvider) {
        console.log('Hello TournamentSettingsProvider Provider');
    }
    setTournaments(tournaments){
        this.tournaments=tournaments;
    }
    getTournaments(eventId){
        return this.tournaments;        
    }
    getTournament(tournamentId){
        return this.tournaments.filter((tournament)=>{
            if(tournament.tournament_id==tournamentId){
                return true;
            } else {
                return false;
            }
        })
    }
 
}
