import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { CookieService } from 'ngx-cookie';

const roleToHomePageMap ={
    'eventowner':'EventOwnerHomePage',
    'tournamentdirector':'TournamentDirectorHomePage',
    'player':'PlayerHomePage'
}
/*
  Generated class for the EventAuthProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class EventAuthProvider {
    userEventRoles:any = {};  
    userLoggedInEvents:any = {};
    eventOwnerUserInfo:any = null;
    constructor(public http: HttpClient,
                public _cookieService:CookieService) {
        let userLoggedInEvents = _cookieService.getObject("userLoggedInEvents");
        let userEventRoles = _cookieService.getObject("userEventRoles");        
        let eventOwnerUserInfo = _cookieService.getObject("eventOwnerUserInfo");
        
        console.log('Hello EventAuthProvider Provider');
        if(userLoggedInEvents!=null){            
            this.userLoggedInEvents = userLoggedInEvents;                                    
        }
        if(userEventRoles!=null){
            this.userEventRoles = userEventRoles;
        }
        if(eventOwnerUserInfo!=null){
            console.log(eventOwnerUserInfo);
            this.eventOwnerUserInfo=eventOwnerUserInfo;
        } else {
            console.log('not a event owner');
        }
    }

    setEventUserLoggedIn(eventId,userInfo){
        console.log('in setEventUserLoggedIn');
        console.log(userInfo);
        if(eventId==null && userInfo.event_creator==true){
            this.eventOwnerUserInfo=userInfo;            
            this._cookieService.putObject("eventOwnerUserInfo",userInfo);
            return
        }        
        //this.userLoggedInEvents[eventId]=true;
        this.userLoggedInEvents[eventId]=userInfo;
        if(userInfo.player_id!=null){
            this.setEventRole(eventId,{event_role_name:'player'});
        }
        if(userInfo.pss_user_id!=null){
            this.setEventRole(eventId,userInfo.roles[0]);            
        }
        
        this._cookieService.putObject("userLoggedInEvents", this.userLoggedInEvents, {path:'/'});
        this._cookieService.putObject("userEventRoles", this.userEventRoles, {path:'/'});        
        console.log('setEventUserLoggedIn debug...');        
        
    }

    isEventUserLoggedIn(eventId){
        if (eventId in this.userLoggedInEvents){
            return true;//this.userLoggedInEvents[eventId];
        } else {
            return null;
        }       
    }
    
    setEventRole(eventId,role){
        if(eventId!=null){            
            this.userEventRoles[eventId] = role;
        }
        
    }

    getEventOwnerPssUserId(){
        if(this.eventOwnerUserInfo!=null){
            return this.eventOwnerUserInfo.pss_user_id;
        } else {
            return null;
        }
        
    }
    getEventPlayerId(eventId){
        return this.userLoggedInEvents[eventId].events[0].player_id_for_event;
    }
    
    getPssUserId(eventId){
        if(this.userLoggedInEvents[eventId]!=null){
            return this.userLoggedInEvents[eventId].pss_user_id;
        } else {
            return null;
        }
        
    }
        
    getRoleName(eventId:number){
        if (this.eventOwnerUserInfo!=null){
            return "eventowner";
        }
        if (eventId in this.userEventRoles){
            if(this.userEventRoles[eventId].event_role_name!=null){
                return this.userEventRoles[eventId].event_role_name;
            } else {
                return 'player';
            }
            
        } else {
            return null;
        }
    }
    getHomePage(eventId:number){
        if(this.eventOwnerUserInfo!=null){
            return roleToHomePageMap['eventowner'];
        }
        if(this.userEventRoles[eventId]){            
            return roleToHomePageMap[this.userEventRoles[eventId].event_role_name]
        }
    }
}
