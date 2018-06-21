import { Component } from '@angular/core';
import { AutoCompleteComponent } from '../../components/auto-complete/auto-complete'
import { IonicPage } from 'ionic-angular';
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton';
import { TakePicComponent } from '../../components/take-pic/take-pic'



/**
 * Generated class for the AddPlayerPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-add-player',
  templateUrl: 'add-player.html',
})
export class AddPlayerPage extends AutoCompleteComponent {
    //selectedPlayer:any={player_full_name:""};
    addPlayerAutoComplete:boolean=true;
    ifpaLookup:boolean=false;

    generateAddEventPlayersProcessor(){
        return (result) => {
            if(result == null){
                return;
            }
            console.log('in generateAddEventPlayerProcessor')
            
            let success_title_string='Player '+result.data[0].player_full_name+' has been added to event.';
            let success_line_one_string='Player Pin is '+result.data[0].pin;
            let success_line_two_string='Player Number is '+result.data[0].events[0].player_id_for_event;
            let successSummary = new SuccessSummary(success_title_string,success_line_one_string,success_line_two_string);            
            let successButtonHome = new SuccessButton('Go Home',
                                                  this.getHomePageString(this.eventId),
                                                      this.buildNavParams({}));
            let successButtonTickets = new SuccessButton('Purchase Tickets',
                                                         'TicketPurchasePage',
                                                         this.buildNavParams({player_id_for_event:result.data[0].events[0].player_id_for_event}));            
            
            this.navCtrl.push("PostPlayerAddSuccessPage",            
                              this.buildNavParams({'requirePic':result['require_pic'],
                                                   'successSummary':successSummary,
                                                   'successButtons':[successButtonHome,successButtonTickets],
                                                   'playerId':result.data[0].player_id}));
        };
    }
    
    generateSearchPlayerProcessor(){
        return (result)=>{
            console.log('in generateSearchPlayerProcessor')
            
        }
    }
    takePicture(){
        let profileModal = this.modalCtrl.create(TakePicComponent, { userId: 8675309 });
        profileModal.onDidDismiss(data => {
            console.log('in modal...');            
            if(data!=null){
                this.selectedPlayer.has_pic=true;
                this.selectedPlayer.img_file=data;
            }
        });
        profileModal.present();
    }
    
    generateGetIfpaRankingProcessor(){
        return (result)=>{
            console.log('in generateGetIfpaRankingProcessor')
            if(result==null){
                return;
            }            
            this.ifpaLookup=true;
            if(result.ifpa_ranking.search.length==0){
                let alert = this.alertCtrl.create();
                alert.setTitle('No IFPA Players Found');
                alert.setMessage('No players found with the name specified.  Please change the name and try again.')
                alert.addButton('Ok');
                alert.present();                                
            }
            if(result.ifpa_ranking.search.length==1){
                this.selectedPlayer.ifpa_ranking=result.ifpa_ranking.search[0].wppr_rank
            }
            if(result.ifpa_ranking.search.length>1){
                let alert = this.alertCtrl.create();
                alert.setTitle('Multiple IFPA Players Found');
                alert.setSubTitle('Select Correct Player');
                for(let ifpaPlayer of result.ifpa_ranking.search){
                    alert.addInput({
                        type: 'radio',
                        label: ifpaPlayer.first_name+" (rank : "+ifpaPlayer.wppr_rank+")",
                        value: ifpaPlayer.wppr_rank                        
                    });

                }

                alert.addButton('Cancel');
                alert.addButton({
                    text: 'OK',
                    handler: data => {
                        this.selectedPlayer.ifpa_ranking=data;                        
                    }
                });
                alert.present();                                
            }
        }
    }
    
    onFocus(){        
        this.selectedPlayer={player_full_name:null};
    }

    onSelected(){
        this.getIfpaRanking(this.selectedPlayer.first_name+" "+this.selectedPlayer.last_name)
    }
    
    
    getIfpaRanking(playerName){
        this.ifpaLookup=true;
        this.pssApi.getIfpaRanking(playerName)
            .subscribe(this.generateGetIfpaRankingProcessor())                    
    }

    getIfpaRankingMobile(playerName,slidingItem){
        this.ifpaLookup=true;
        slidingItem.close();
        this.getIfpaRanking(playerName);
    }
    
    onChange(event){
        console.log('in onChange...')
        
    }
    
    onInput(event){        

        console.log('in onInput...')
    }
    
    onItemsShown(event){
        console.log('onItemsShown...')
    }

    generateLoadingFunction(){
        return (searchResults)=>{
            console.log('in loading function');
            
            if (searchResults.typeOfSearch=="list" && searchResults.resultList.length==0){
                if(this.searchbar.keyword.length > 2){
                    console.log(this.searchbar.keyword)
                    let nameElements=this.searchbar.keyword.split(' ');
                    if(nameElements.length>0){
                        this.selectedPlayer.first_name=nameElements[0];
                    }
                    if(nameElements.length>1){
                        this.selectedPlayer.last_name=nameElements[1];
                    }
                }
            } else {
            }
            setTimeout(()=>{this.loading=false;},500)
            
        }
    }
  ionViewWillLoad() {
      console.log('ionViewDidLoad AddPlayerPage');
      if(this.eventId==null){
          this.pushRootPage('EventSelectPage')
          return;
      }
       this.eventId = this.navParams.get('eventId')
       this.autoCompleteProvider.initializeAutoComplete("player-full-name",
                                                        null,
                                                        this.generateLoadingFunction());

      
  }
    onSubmit(){
        if(this.selectedPlayer.ifpa_ranking=='not ranked'){
            this.selectedPlayer.ifpa_ranking=99999;
        }
        this.pssApi.addEventPlayers({players:[this.selectedPlayer]},this.eventId)
            .subscribe(this.generateAddEventPlayersProcessor())                                                  

    }
    
}
