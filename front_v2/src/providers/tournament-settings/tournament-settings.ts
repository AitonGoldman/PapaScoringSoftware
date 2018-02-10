import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { PssApiProvider } from '../../providers/pss-api/pss-api';
import { CookieService } from 'ngx-cookie';

/*
  Generated class for the TournamentSettingsProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class TournamentSettingsProvider {
    tournaments:any = null;
    tournamentMachines:any = null;
    events:any=null;
    
    constructor(public http: HttpClient, public pssApi: PssApiProvider,public _cookieService:CookieService) {
        console.log('Hello TournamentSettingsProvider Provider');
    }
    setTournaments(tournaments){
        console.log(tournaments)
        this.tournaments=tournaments;
        let cookieTournaments = []
        tournaments.forEach((tournament)=>{
            cookieTournaments.push({tournament_id:tournament.tournament_id,
                                    tournament_name:tournament.tournament_name,
                                    number_of_signifigant_scores:tournament.number_of_signifigant_scores})
        })
        this._cookieService.putObject("tournaments",cookieTournaments)
    }
    setEvents(events){
        this.events=events;
        this._cookieService.putObject("events",this.events)
    }
    getEvents(){
        if(this.events!=null){
            return this.events;
        }
        this.events = this._cookieService.getObject("events")
    }
    getEvent(eventId){
        if(this.events==null){
            this.events = this._cookieService.getObject("events")
        }
        
        return this.events.filter((event)=>{
            if(event.event_id==eventId){
                return true;
            } else {
                return false;
            }
        })
    }
    getTournaments(eventId){
        if(this.tournaments==null){
            this.tournaments = this._cookieService.getObject("tournaments")
        }        
        return this.tournaments;        
    }
    getTournament(tournamentId){
        if(this.tournaments==null){
            this.tournaments = this._cookieService.getObject("tournaments")
        }        

        return this.tournaments.filter((tournament)=>{
            if(tournament.tournament_id==tournamentId){
                return true;
            } else {
                return false;
            }
        })[0]
    }
 
}
