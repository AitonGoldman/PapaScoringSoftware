import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import {AutoCompleteService} from 'ionic2-auto-complete';
import { PssApiProvider } from '../../providers/pss-api/pss-api';
import { SearchResults } from '../../classes/search-results';
import { Events } from 'ionic-angular';


/*
  Generated class for the AutoCompleteProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/

// need a playerSearchResults object
// players list
// indiv player
// type of request

// items : don't care
// search for player num or players : need to pass back player (or null) to loading func

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
    constructor(public http: HttpClient, public pssApi: PssApiProvider,public events: Events) {
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

    processSearchResults(typeOfSearch){
        return (result)=>{
            this.events.publish('autocomplete:done', {type:typeOfSearch, state:'DONE', data: result}, Date.now());
            if(result==null){
                return "";
            }
            if(typeOfSearch=="SEARCH_LIST"){
                return result.data;
            }
            if(typeOfSearch=="SEARCH_SINGLE"){
                return "";
            }
        }
        // return (result)=>{
            
        //     if(result==null){
        //         this.loadingCompleteFunc(searchResults)
        //         return ""
        //     };
        //     if(typeOfSearch=="list"){
        //         //            if(Array.isArray(result.data)){
        //         searchResults.resultList=result.data;
        //         this.loadingCompleteFunc(searchResults)
        //         return result.data
        //     } else {
        //         searchResults.individualResult=result;
        //         this.loadingCompleteFunc(searchResults)
        //         return ""
        //     }
        // }
    }
    
    getResults(name:string){
        //let searchResults = new SearchResults([],null,null);
        console.log(1);        
        if(this.currentValue!=name){
            this.currentValue=name;            
        }else{
            this.events.publish('autocomplete:done', {state:'SAME_INPUT'}, Date.now());
            //this.loadingCompleteFunc(searchResults)
            return [];
        }
        console.log(2);
        if(name.length<3){
            this.events.publish('autocomplete:done', {state:'NOT_ENOUGH_INPUT'}, Date.now());
            //this.loadingCompleteFunc(searchResults)
            return [];
        }
        console.log(3);
        let eventPlayerId:number = parseInt(name);
        if (Number.isNaN(eventPlayerId)==true && this.autocompleteType=="remote"){
            //this.itemFieldToMatch='player_full_name'        
            this.labelAttribute = "player_full_name";        
            //searchResults.typeOfSearch="list";
            console.log(4);
            if(this.eventId){
                console.log(5);
                console.log('going to event player search....')
                return this.pssApi.searchEventPlayers(this.eventId,name)['map'](this.processSearchResults('SEARCH_LIST'))                            
            } else {
                console.log(6);
                return this.pssApi.searchPlayers(name)['map'](this.processSearchResults('SEARCH_LIST'))

            }
            
        } 
        if (Number.isNaN(eventPlayerId)==false && this.autocompleteType=="remote"){
            console.log(7);
            //this.itemFieldToMatch='player_id_for_event'        
            this.labelAttribute = "player_id_for_event";
            //searchResults.typeOfSearch="single";            
            return this.pssApi.getEventPlayer(this.eventId,name)['map'](this.processSearchResults('SEARCH_SINGLE'))
        } 

        if(this.autocompleteType=="remote"){
            console.log('in getResults...');

        }
        let regex = new RegExp(name.toLowerCase());        
        //this.loadingCompleteFunc(searchResults);
        console.log('filtering items for ... '+name);
        this.events.publish('autocomplete:done', {type:'ITEMS_LIST', state:'DONE'}, Date.now());
        return this.items.filter(
            (item) => {
                //let matches = item[this.itemFieldToMatch].toLowerCase().match(regex);
                let matches = item[this.labelAttribute].toLowerCase().match(regex);
                return (matches!=null && matches.length > 0)
            }
        )
    }
}
