import { ViewChild, Component } from '@angular/core';
import { AutoCompleteComponent } from '../../components/auto-complete/auto-complete'
import { IonicPage } from 'ionic-angular';


/**
 * Generated class for the PlayerInfoPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'PlayerInfo/:eventId'
})
@Component({
  selector: 'page-player-info',
  templateUrl: 'player-info.html',
})
export class PlayerInfoPage extends AutoCompleteComponent {
    loading:boolean=false;
    ticketCounts:any=null;
    selectedPlayer:any=null;    
    player_id_for_event:number=null;
    playerLoadStatus:string='notStarted';
    @ViewChild('searchbar')  searchbar: any;    
    singleUser:any=null;
    
    
    // generateGetEventPlayerProcessor(){
    //     return (result)=>{
    //         if(result==null){                
    //             return
    //         }
    //         this.selectedPlayer=result.data;
    //         this.ticketCounts=this.generateListFromObj(this.selectedPlayer.tournament_counts);            
    //     }
    // }
  
  ionViewWillLoad() {
      console.log('ionViewDidLoad PlayerInfoPage');
      //this.autoCompleteProvider.setPlayerSearchType("allPlayers",
      //                                              this.generateLoadingFunction());      
      this.autoCompleteProvider.initializeAutoComplete(null,
                                                       null,
                                                       this.generatePlayerLoadingFunction(),
                                                       this.eventId);      
      
      let player_id_for_event = this.navParams.get('player_id_for_event');
      if(player_id_for_event==null){          
          return;            
      }      
      this.player_id_for_event=player_id_for_event
      //this.pssApi.getEventPlayer(this.eventId,this.player_id_for_event)
      //    .subscribe(this.generateGetEventPlayerProcessor())                                                  
        
  }
    onFocus(){
        console.log('in onFocus..')
        this.selectedPlayer=null;
        this.ticketCounts=null;
        //this.selectedPlayer={player_full_name:null,player_id_for_event:null,first_name:null,last_name:null};
    }

    // onSelected(){
    //     console.log(this.selectedPlayer);
    //     this.pssApi.getEventPlayer(this.eventId,this.selectedPlayer.player_id_for_event)
    //         .subscribe(this.generateAutoCompleteGetEventPlayerProcessor())
    // }
    
    onInput(event){        
        console.log('in onInput...')
        console.log(event);
        this.loading=true;        
        //if(event.length==3){
            //this.searchbar.select(100);
        //}
        
    }

    onItemsShown(){
        console.log('in onItemsShown');        
//        console.log(event);
//        console.log(this.searchbar);
//        this.searchbar.select(null);
        //this.searchbar._showList=false;
//        console.log("-----------");        
//        console.log(this.searchbar.getItems());
//        console.log("-----------");        
    }
    // generateLoadingFunction(){
    //     return (input?)=>{
    //         if(input!=null){
    //             console.log(input)
    //             this.selectedPlayer=input.data;
    //             console.log(this.selectedPlayer);
    //             this.ticketCounts=this.generateListFromObj(this.selectedPlayer.tournament_counts);
    //         }            
    //         setTimeout(()=>{this.loading=false;},500)            
    //     }
    // }

    // generateListFromObj(obj){
    //     if(obj==null){
    //         return []
    //     }
    //     return Object.keys(obj).map(function(key){
    //         let objValue =obj[key];
    //         // do something with person
    //         return objValue
    //     });
    // }
    // onInput(event){        
    //     this.playerLoadStatus='notStarted';
    //     if(this.player_id_for_event != null && this.player_id_for_event > 99 && this.player_id_for_event < 1000){
    //         console.log('in onInput')
    //         this.pssApi.getEventPlayer(this.eventId,this.player_id_for_event)
    //             .subscribe(this.generateGetEventPlayerProcessor())                                                  

    //     } else {
    //         this.clearValues();
    //     }        
    // }
    clearValues(){
        this.selectedPlayer={};
        //this.eventPlayer={};
        //this.player_id_for_event=null;        
    }

}
