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
  roles:any = {};
  constructor(public http: HttpClient) {
    console.log('Hello EventAuthProvider Provider');
  }
  
  setRoles(roles){
    this.roles=roles;
  }

  setEventRole(eventId,role){
   this.userEventRoles[eventId] = role;
  }
  
  getRoleName(eventId:number){
    if (eventId in this.userEventRoles){
     return this.userEventRoles[eventId].roleName;
    } else {
     return null;
    }

  }    
}
