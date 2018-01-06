import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import {AutoCompleteService} from 'ionic2-auto-complete';
import { PssApiProvider } from '../../providers/pss-api/pss-api';
import { Http } from '@angular/http';

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
    players:any=null;
    url:string=null;
    itemFieldToMatch:any;
    loadingObservable:any;
    constructor(public http: HttpClient, public pssApi: PssApiProvider) {
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
    setEndpoint(typeOfEndpoint){
        if(typeOfEndpoint=="allPlayers"){
            
        }
    }

    setPlayerSearchType(typeOfSearch,observable){        
        let url = ""
        if(typeOfSearch=="allPlayers"){
            url="http://192.168.1.178:8000/players/"
        }
        this.itemFieldToMatch='player_full_name'        
        this.labelAttribute = "player_full_name";        
        this.url=url;
        this.loadingObservable=observable
    }
    
    setPlayers(allPlayers){
        if(allPlayers==true){
            this.pssApi.getAllPlayers()
                .subscribe((result)=>{this.players=result.data;this.items=this.players})            
            
        }
    }
    getResults(name:string){        
        if(this.url!=null){
            console.log('in getResults...');
            return this.http.get(this.url+name)['map'](result=>{return result.data})['do']((input)=>{this.loadingObservable(input)});
            //return this.pssApi.searchPlayers(name)
        }
        let regex = new RegExp(name.toLowerCase());
        return this.items.filter(
            (item) => {
                let matches = item[this.itemFieldToMatch].toLowerCase().match(regex);
                return (matches!=null && matches.length > 0)
            }
        )
    }
}
