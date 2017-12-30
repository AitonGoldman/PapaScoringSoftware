import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

/*
  Generated class for the EventAuthProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class EventAuthProvider {
    userEventRoles:any = {};  
    userLoggedInEvents:any = {};
    eventOwner:boolean = false;
    userName:string = null;
    constructor(public http: HttpClient) {
    console.log('Hello EventAuthProvider Provider');
    }

    setEventUserLoggedIn(eventId,userInfo){
        if(eventId==null){
            this.eventOwner=true;
            return;
        } 
        this.userLoggedInEvents[eventId]=true;
        this.userName=userInfo.username;
        this.setEventRole(eventId,userInfo.roles[0]);
        console.log('setEventUserLoggedIn debug...');
        console.log(userInfo);
    }

    isEventUserLoggedIn(eventId){
        if (eventId in this.userLoggedInEvents){
            return this.userLoggedInEvents[eventId];
        } else {
            return null;
        }
        //return this.userLoggedInEvents[eventId]!=null&&this.userLoggedInEvents[eventId]!=undefined;
    }
    
    setEventRole(eventId,role){
        if(eventId!=null){            
            this.userEventRoles[eventId] = role;
        }
        
    }
  
    getRoleName(eventId:number){
        if (this.eventOwner==true){
            return "eventowner";
        }
        if (eventId in this.userEventRoles){
            return this.userEventRoles[eventId].event_role_name;
        } else {
            return null;
        }
    }    
}
