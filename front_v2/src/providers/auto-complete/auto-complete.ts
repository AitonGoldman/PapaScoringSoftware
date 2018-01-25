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

// fix add-users - check
// fix add-machines  - check
// fix add-players - check
// queue players - check
// add to ticket-purchase
// edit user

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
        this.currentValue=null;
        
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
            console.log('in processSearchResults');
            
            if(result==null){                
                return "";
            }
            if(typeOfSearch=="SEARCH_LIST"){
                if(result.data.length>0){
                    this.events.publish('autocomplete:done', {type:typeOfSearch, state:'DONE', data: result}, Date.now());
                } else {
                    this.events.publish('autocomplete:done', {type:typeOfSearch, state:'NONE', data: result}, Date.now());
                }
                return result.data;
            }
            if(typeOfSearch=="SEARCH_SINGLE"){
                if(result.data!=null){
                    this.events.publish('autocomplete:done', {type:typeOfSearch, state:'DONE', data: result}, Date.now());
                } else {
                    this.events.publish('autocomplete:done', {type:typeOfSearch, state:'NONE', data: result}, Date.now());
                }                
                return "";
            }
        }
    }
    
    getResults(name:string){
        //let searchResults = new SearchResults([],null,null);
        
        if(this.currentValue!=name){
            this.currentValue=name;            
        }else{
            this.events.publish('autocomplete:skip', {state:'SAME_INPUT'}, Date.now());
            //this.loadingCompleteFunc(searchResults)
            return [];
        }
        
        if(name.length<3){
            this.events.publish('autocomplete:skip', {state:'NOT_ENOUGH_INPUT'}, Date.now());
            //this.loadingCompleteFunc(searchResults)
            return [];
        }
        
        let eventPlayerId:number = parseInt(name);
        if (Number.isNaN(eventPlayerId)==true && this.autocompleteType=="remote"){
            //this.itemFieldToMatch='player_full_name'        
            this.labelAttribute = "player_full_name";        
            //searchResults.typeOfSearch="list";
            
            if(this.eventId){
                
                
                return this.pssApi.searchEventPlayersHidden(this.eventId,name)['map'](this.processSearchResults('SEARCH_LIST'))                            
            } else {
                
                return this.pssApi.searchPlayersHidden(name)['map'](this.processSearchResults('SEARCH_LIST'))

            }
            
        } 
        if (Number.isNaN(eventPlayerId)==false && this.autocompleteType=="remote"){
            
            //this.itemFieldToMatch='player_id_for_event'        
            this.labelAttribute = "player_id_for_event";
            //searchResults.typeOfSearch="single";            
            //return this.pssApi.getEventPlayerHidden(this.eventId,name)['map'](this.processSearchResults('SEARCH_SINGLE'))
            return this.pssApi.getEventPlayerResultsHidden(this.eventId,name)['map'](this.processSearchResults('SEARCH_SINGLE'))
        } 

        if(this.autocompleteType=="remote"){
            console.log('in getResults...');

        }
        let regex = new RegExp(name.toLowerCase());        
        //this.loadingCompleteFunc(searchResults);
                
        let items_to_return = this.items.filter(
            (item) => {                
                let matches = item[this.labelAttribute].toLowerCase().match(regex);
                return (matches!=null && matches.length > 0)
            }
        )
        if(items_to_return.length>0){
            this.events.publish('autocomplete:done', {type:'ITEMS_LIST', state:'DONE', data: items_to_return}, Date.now());
        } else {
            this.events.publish('autocomplete:done', {type:'ITEMS_LIST', state:'NONE', data: null}, Date.now());
        }
        return items_to_return;
    }
}
