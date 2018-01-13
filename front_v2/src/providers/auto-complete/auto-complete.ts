import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import {AutoCompleteService} from 'ionic2-auto-complete';
import { PssApiProvider } from '../../providers/pss-api/pss-api';


/*
  Generated class for the AutoCompleteProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/

// make initilialize function, handles seting up/cleaning up previous
// rename observable, make it able to set loading without passing info around
// fix player-info
// - move common elements to psspage - check
// fix add-users
// fix add-machines
// fix add-players
// add to ticket-purchase

@Injectable()
export class AutoCompleteProvider implements AutoCompleteService{
    labelAttribute:string = "";
    formValueAttribute = ""    
    items:any;    
    url:string=null;
    allPlayersUrl:string="http://192.168.1.178:8000/players/"    
    eventId:any=null;
    //itemFieldToMatch:any;
    //loadingObservable:any;
    loadingCompleteFunc:any=null;
    autocompleteType:string=null;
    currentValue:string=null;    
    constructor(public http: HttpClient, public pssApi: PssApiProvider) {
        console.log('Hello AutoCompleteProvider Provider');
    }
    
    initializeAutoComplete(labelAttribute?, items?, loadingCompleteFunc?, eventId?){        
        this.autocompleteType=items==null?"remote":"local";        
        this.items=items;
        this.eventId=eventId;
        this.labelAttribute=labelAttribute;
        this.loadingCompleteFunc=loadingCompleteFunc
        console.log(this.autocompleteType)
    }

    // getItemLabel(returnedItem){
    //     console.log('in getItemLabel')
    //     console.log(returnedItem)        
    //     return returnedItem
    // }
    setMachines(machines){
        this.url=null;
        this.items=machines;
        //this.itemFieldToMatch='machine_name'
        this.labelAttribute = "machine_name";        
    }
    addUsers(user){        
        this.items.push(user);
    }
    setUsers(users){
        this.url=null;
        this.items=users;
        //this.itemFieldToMatch='full_user_name'        
        this.labelAttribute = "full_user_name";
    }
    setEndpoint(typeOfEndpoint){
        if(typeOfEndpoint=="allPlayers"){
            
        }
    }

    setPlayerSearchType(typeOfSearch,observable){        
        this.items=null;
//        this.loadingObservable=observable
    }
    
    // setPlayers(allPlayers){
    //     this.url=null;
    //     if(allPlayers==true){
    //         this.pssApi.getAllPlayers()
    //             .subscribe((result)=>{this.players=result.data;this.items=this.players})            
            
    //     }
    // }

    processSearchResults(){
        return (result)=>{

        if(result==null){
            this.loadingCompleteFunc()
            return ""
        };
        if(Array.isArray(result.data)){
            this.loadingCompleteFunc()
            return result.data
        } else {
            this.loadingCompleteFunc(result)
            return ""
        }
    }
        }
    
    getResults(name:string){
        if(this.currentValue!=name){
            this.currentValue=name;
        }else{
            return [];
        }

        if(name.length<3){
            return [];
        }
        let eventPlayerId:number = parseInt(name);
        if (Number.isNaN(eventPlayerId)==true && this.autocompleteType=="remote"){
            //this.itemFieldToMatch='player_full_name'        
            this.labelAttribute = "player_full_name";        
            if(this.eventId){
                console.log('going to event player search....')
                return this.pssApi.searchEventPlayersHidden(this.eventId,name)['map'](this.processSearchResults())                            
            } else {
                return this.pssApi.searchPlayersHidden(name)['map'](this.processSearchResults())            

            }
            
        } 
        if (Number.isNaN(eventPlayerId)==false && this.autocompleteType=="remote"){
            
            //this.itemFieldToMatch='player_id_for_event'        
            this.labelAttribute = "player_id_for_event";
            return this.pssApi.getEventPlayerHidden(this.eventId,name)['map'](this.processSearchResults())            
        } 

        if(this.autocompleteType=="remote"){
            console.log('in getResults...');

            // return this.http.get(this.url+name)['map'](result=>{if(Array.isArray(result.data)){
            //     this.loadingCompleteFunc()
            //     return result.data
            // } else {
            //     this.loadingCompleteFunc(result)
            //     return ""//[result.data]
            // }})
            //

            // ['do']((input)=>{
            // this.loadingObservable(input)
            // });
            
            //return this.pssApi.searchPlayers(name)
        }
        let regex = new RegExp(name.toLowerCase());
        return this.items.filter(
            (item) => {
                //let matches = item[this.itemFieldToMatch].toLowerCase().match(regex);
                let matches = item[this.labelAttribute].toLowerCase().match(regex);
                return (matches!=null && matches.length > 0)
            }
        )
    }
}
