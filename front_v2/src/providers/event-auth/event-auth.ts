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
    pssUserId:number = null;
    constructor(public http: HttpClient) {
    console.log('Hello EventAuthProvider Provider');
    }

    setEventUserLoggedIn(eventId,userInfo){
        this.userName=userInfo.username;
        this.pssUserId=userInfo.pss_user_id;
        
        if(eventId==null){
            this.eventOwner=true;
            return
        }        
        this.userLoggedInEvents[eventId]=true;
        this.setEventRole(eventId,userInfo.roles[0]);
        console.log('setEventUserLoggedIn debug...');        
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
    getUserInfo(){
        return {userName:this.userName,
                pssUserId:this.pssUserId}
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
