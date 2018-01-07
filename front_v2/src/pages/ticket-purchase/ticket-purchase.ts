import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton';

/**
 * Generated class for the TicketPurchasePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'TicketPurchasePage/:eventId'
})
@Component({
  selector: 'page-ticket-purchase',
  templateUrl: 'ticket-purchase.html',
})
export class TicketPurchasePage extends PssPageComponent{
    ticketPriceLists:any=null;
    ticketCounts:any=null;
    eventPlayer:any={};
    player_id_for_event:number=null;
    totalCost:number=0;
    ionViewDidLoad() {
        console.log('ionViewDidLoad TicketPurchasePage');
    }
    generateGetEventPlayerProcessor(){
        return (result)=>{
            if(result==null){
                return
            }
            this.eventPlayer=result.data!=null?result.data:{};
            this.ticketPriceLists=result.tournament_calculated_lists;
            this.ticketCounts=result.tournament_counts;
            
            console.log(result);
        }
    }
    generatePurchaseTicketProcessor(purchaseSummary){
        return (result) => {
            if(result == null){
                return;
            }
            
            let success_title_string='Tickets Purchased!';
            let successSummary = new SuccessSummary(success_title_string,purchaseSummary.pop(),null);
            successSummary.setSummaryTable(purchaseSummary);
            let successButton = new SuccessButton('Go Home',
                                                  this.getHomePageString(this.eventId),                                                  
                                                  this.buildNavParams({}));            
            this.navCtrl.push("SuccessPage",            
                              this.buildNavParams({'successSummary':successSummary,
                                                   'successButtons':[successButton]}));
        };
    }
    
    clearValues(){
        this.ticketPriceLists=null;
        this.ticketCounts=null;
        this.eventPlayer={};
        //this.player_id_for_event=null;
        this.totalCost=0;

    }

    onInput(event){        
        if(this.player_id_for_event != null && this.player_id_for_event > 99 && this.player_id_for_event < 1000){
            console.log('in onInput')
            this.pssApi.getEventPlayer(this.eventId,this.player_id_for_event)
                .subscribe(this.generateGetEventPlayerProcessor())                                                  

        } else {
            this.clearValues();
        }        
    }
    onSelect(event){
        this.totalCost=0;
        console.log('in onSelect');
        for(let ticketPrice of this.ticketPriceLists){
            if(ticketPrice.selectedCount!=null){
                this.totalCost=this.totalCost+ticketPrice.selectedCount.price;
            }
            
        }       
    }
    ticketPurchase(){
        let ticketsToBuy={}
        ticketsToBuy['player_id']=this.eventPlayer.player_id;
        ticketsToBuy['tournament_token_counts']=[]
        let purchaseSummary = []
        for(let ticketsSelected of this.ticketPriceLists){
            if(ticketsSelected.selectedCount!=null){
                ticketsToBuy['tournament_token_counts'].push({token_count:ticketsSelected.selectedCount.amount,
                                                              tournament_id:ticketsSelected.tournament_id})
                purchaseSummary.push(ticketsSelected.tournament_name+" : "+ ticketsSelected.selectedCount.amount)
            }
        }
        purchaseSummary.push("total cost : "+this.totalCost);
        console.log(ticketsToBuy);
        this.pssApi.purchaseTicket(ticketsToBuy,this.eventId)
            .subscribe(this.generatePurchaseTicketProcessor(purchaseSummary))                                                  
        
//        post_dict={"player_id":player_id,
//                   "tournament_token_counts":[{"token_count":1,"tournament_id":tournament_id}],
//                   "meta_tournament_token_counts":[{"token_count":1,"meta_tournament_id":meta_tournament['data']['meta_tournament_id']}]}        
    }
}
