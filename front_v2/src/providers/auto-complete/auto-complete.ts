import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import {AutoCompleteService} from 'ionic2-auto-complete';

/*
  Generated class for the AutoCompleteProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class AutoCompleteProvider implements AutoCompleteService{
    labelAttribute:string = "machine_name";
    formValueAttribute = ""
    //machines:any;
    items:any;
    itemFieldToMatch:any;
    constructor(public http: HttpClient) {
        console.log('Hello AutoCompleteProvider Provider');
    }
    setMachines(machines){
        //this.machines=machines;
        this.items=machines;
        this.itemFieldToMatch='machine_name'
        this.labelAttribute = "machine_name";        
    }
    addUsers(user){
        this.items.push(user);
    }
    setUsers(users){
        this.items=users;
        this.itemFieldToMatch='full_user_name'        
        this.labelAttribute = "full_user_name";
    }
    getResults(name:string){        
        let regex = new RegExp(name.toLowerCase());
        return this.items.filter(
            (item) => {
                let matches = item[this.itemFieldToMatch].toLowerCase().match(regex);
                return (matches!=null && matches.length > 0)
            }
        )
    }
}
