import { Component } from '@angular/core';
import { AutoCompleteComponent } from '../../components/auto-complete/auto-complete'
import { IonicPage } from 'ionic-angular';


/**
 * Generated class for the PlayerInfoPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */


// 
//
//
//
@IonicPage()
@Component({
  selector: 'page-player-info',
  templateUrl: 'player-info.html',
})
export class PlayerInfoPage extends AutoCompleteComponent {
//    loading:boolean=false;
//    ticketCounts:any=null;
//    selectedPlayer:any=null;    
    player_id_for_event:number=null;
    playerId:number=null;
    hideAutoComplete:boolean=false;
    playerLoadStatus:string='notStarted';
    infoOnly:boolean=false;
//    @ViewChild('searchbar')  searchbar: any;    
    singleUser:any=null;
    displayExistingUserNotFound:boolean = false;
    loaded:boolean=false;
    //    playerNotFoundMessage = null;
    
    // onKeyUp(event){        
    //     this.playerNotFoundMessage=null        
    //     if(this.searchbar.keyword.length>2){
    //         this.loading=true;
    //     } else {
    //         this.loading=false;
    //     }
    //     if(this.searchbar.keyword.length==0){
    //         this.selectedPlayer=null;
    //     }
        
    // }
     ionViewWillUnload() {
         console.log('unloading player info...');
     }
    ionViewWillEnter() {
        if(this.eventId==null){
            this.pushRootPage('EventSelectPage')
            return;
        }
        // this.imageLoader.clearCache();
        // for(let x = 0; x<100;x++){
        //     this.imageLoader.preload('http://admin.inchglue.com/assets/imgs/'+x+'.jpg').then((data)=>{
        //         console.log("got "+x);
        //         console.log(data);
        //     })
        // }
        // this.testLoading('poop')();
        if(this.loaded==false){
            console.log('entering player info....'+this.loaded)
            
            let player_id_for_event = this.navParams.get('player_id_for_event');
        let playerId = this.navParams.get('playerId');
        this.infoOnly = this.navParams.get('infoOnly')!=null;
            
        if(player_id_for_event==null && playerId==null){          
            return;            
        }
        this.hideAutoComplete=true;
        this.player_id_for_event=player_id_for_event
        this.playerId=playerId
            if(player_id_for_event!=null){
                console.log('player id - loading...')
            this.pssApi.getEventPlayerResults(this.eventId,this.player_id_for_event)
                .subscribe(this.generateGetEventPlayerProcessor())                                                          
        } else {
                console.log('event player id - loading...'+this.eventId+" "+this.playerId)

            this.pssApi.getEventPlayerResultsByPlayerId(this.eventId,this.playerId)
                .subscribe(this.generateGetEventPlayerProcessor())                                                                      
        }
            
        }
        this.loaded=true;
        
    }
    onReload(){
        if(this.selectedPlayer!=null)
            this.pssApi.getEventPlayerResultsByPlayerId(this.eventId,this.selectedPlayer.player_id)
                .subscribe(this.generateGetEventPlayerProcessor())                                                                                  
    }
    
    ionViewWillLoad() {
        console.log('ionViewDidLoad PlayerInfoPage');
        this.autoCompleteProvider.initializeAutoComplete(null,
                                                         null,
                                                         this.generatePlayerLoadingFunction(),
                                                         this.eventId,
                                                         true);      
      
        // let player_id_for_event = this.navParams.get('player_id_for_event');
        // let playerId = this.navParams.get('playerId');
        // this.infoOnly = this.navParams.get('infoOnly')!=null;
            
        // if(player_id_for_event==null && playerId==null){          
        //     return;            
        // }
        // this.hideAutoComplete=true;
        // this.player_id_for_event=player_id_for_event
        // this.playerId=playerId
        // if(player_id_for_event!=null){
        //     this.pssApi.getEventPlayerResults(this.eventId,this.player_id_for_event)
        //         .subscribe(this.generateGetEventPlayerProcessor())                                                          
        // } else {
        //     this.pssApi.getEventPlayerResultsByPlayerId(this.eventId,this.playerId)
        //         .subscribe(this.generateGetEventPlayerProcessor())                                                                      
        // }
    }
    generateGetEventPlayerProcessor(){
        return (result)=>{
            if(result==null){
                return;
            }
            console.log(result);
            this.selectedPlayer=result.data;            
            this.ticketCounts=this.generateListFromObj(result.tournament_counts);                        
            this.results=result.data.values;

        }
    }
    onFocus(){
        console.log('in onFocus..')
        this.selectedPlayer=null;
        this.ticketCounts=null;
        //this.selectedPlayer={player_full_name:null,player_id_for_event:null,first_name:null,last_name:null};
    }
    
    onInput(event){        
        console.log('in onInput...')
        console.log(event);
        
    }

    onItemsShown(){
        console.log('in onItemsShown');
    }
        
        
    clearValues(){
        this.selectedPlayer={};
        //this.eventPlayer={};
        //this.player_id_for_event=null;        
    }

}
