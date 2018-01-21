import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { CookieService } from 'ngx-cookie';

/*
  Generated class for the ListOrderStorageProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class ListOrderStorageProvider {

    constructor(public http: HttpClient, public _cookieService:CookieService) {
        console.log('Hello ListOrderStorageProvider Provider');
    }
    
    getList(pageName,listName){
        let listStorage = this._cookieService.getObject("listStorage");
        if(listStorage==null){
            listStorage={};            
        }
        if(listStorage[pageName]==null){
            listStorage[pageName]={};
        }
        return listStorage[pageName][listName];
    }
    
    updateList(pageName,listName, list){
        let listStorage = this._cookieService.getObject("listStorage");
        if(listStorage==null){
            listStorage={};            
        }
        if(listStorage[pageName]==null){
            listStorage[pageName]={};
        }
        listStorage[pageName][listName]=list;
        this._cookieService.putObject("listStorage",listStorage);
    }
    //FIXME : this should be in it's own service
    addFavoriteTournamentMachine(eventId,tournamentMachineId,tournamentMachineName){
        console.log('recording new favorite...');
        let favoriteMachines = this._cookieService.getObject("favoriteMachines");
        if(favoriteMachines==null){
            favoriteMachines={};            
        }
        if(favoriteMachines[eventId]==null){
            favoriteMachines[eventId]={};
        }
        favoriteMachines[eventId][tournamentMachineId]={tournamentMachineId:tournamentMachineId,tournamentMachineName:tournamentMachineName};
        this._cookieService.putObject("favoriteMachines",favoriteMachines);
    }
    getFavoriteTournamentMachines(eventId){        
        let favoriteMachines = this._cookieService.getObject("favoriteMachines");
        if(favoriteMachines==null){
            return null;
        }
        return favoriteMachines[eventId];
    }
    
    
}