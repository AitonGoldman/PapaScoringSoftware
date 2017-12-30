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
    machines:any;
    constructor(public http: HttpClient) {
        console.log('Hello AutoCompleteProvider Provider');
    }
    setMachines(machines){
        this.machines=machines;        
    }
    getResults(machineName:string){        
        let regex = new RegExp(machineName.toLowerCase());
        return this.machines.filter(
            (item) => {
                let matches = item.machine_name.toLowerCase().match(regex);
                return (matches!=null && matches.length > 0)
            }
        )
    }
}
