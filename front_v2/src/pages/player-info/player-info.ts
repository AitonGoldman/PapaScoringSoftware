import { ViewChild, Component } from '@angular/core';
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
@IonicPage({
    segment:'PlayerInfo/:eventId'
})
@Component({
  selector: 'page-player-info',
  templateUrl: 'player-info.html',
})
export class PlayerInfoPage extends AutoCompleteComponent {
//    loading:boolean=false;
//    ticketCounts:any=null;
//    selectedPlayer:any=null;    
    player_id_for_event:number=null;
    playerLoadStatus:string='notStarted';
//    @ViewChild('searchbar')  searchbar: any;    
    singleUser:any=null;
    displayExistingUserNotFound:boolean = false;
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
//        super.ionViewWillLoad();
        console.log('ionViewDidLoad PlayerInfoPage');
      //this.autoCompleteProvider.setPlayerSearchType("allPlayers",
      //                                              this.generateLoadingFunction());      
        // this.events.subscribe('autocomplete:skip', (autocompleteInfo, time) => {            
        //     this.loading=false;
        // })

        // this.events.subscribe('autocomplete:done', (autocompleteInfo, time) => {
        //     // user and time are the same arguments passed in `events.publish(user, time)`
        //     this.loading=false;            
        //     if(autocompleteInfo.state=='DONE'){
        //         console.log(autocompleteInfo);
        //         if(autocompleteInfo.type=='SEARCH_SINGLE'){
        //             this['selectedPlayer']=autocompleteInfo.data.data;
        //             this['ticketCounts']=this.generateListFromObj(this['selectedPlayer'].tournament_counts);                
        //         }                
        //     }
        //     if(autocompleteInfo.state=='NONE'){
        //         console.log(autocompleteInfo);
        //         console.log(this.searchbar);
        //         this.playerNotFoundMessage = "Player not found";
                
        //         // let toast = this.toastCtrl.create({
        //         //     message:  "No Such Player in Event",
        //         //     duration: 99000,
        //         //     position: 'top',
        //         //     showCloseButton: true,
        //         //     closeButtonText: " ",
        //         //     cssClass: "dangerToast"
        //         // });
        //         // toast.present();                                                    
        //     }            
        // });
        this.autoCompleteProvider.initializeAutoComplete(null,
                                                         null,
                                                         this.generatePlayerLoadingFunction(),
                                                         this.eventId,
                                                         true);      
      
        let player_id_for_event = this.navParams.get('player_id_for_event');
        if(player_id_for_event==null){          
            return;            
        }      
        this.player_id_for_event=player_id_for_event
        //this.tournamentSettings.getTournament(result.tournament_id)        
      //this.pssApi.getEventPlayer(this.eventId,this.player_id_for_event)
      //    .subscribe(this.generateGetEventPlayerProcessor())                                                          
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
