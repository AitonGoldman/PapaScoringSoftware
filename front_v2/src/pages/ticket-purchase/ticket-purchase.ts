import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton';
import { AutoCompleteComponent } from '../../components/auto-complete/auto-complete'

declare var StripeCheckout: any;
/**
 * Generated class for the TicketPurchasePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'TicketPurchasePage/:eventId/:eventName'
})
@Component({
  selector: 'page-ticket-purchase',
  templateUrl: 'ticket-purchase.html',
})
export class TicketPurchasePage  extends AutoCompleteComponent {
    ticketPriceLists:any=null;
    ticketCounts:any=null;
    //selectedPlayer:any={};
    //player_id_for_event:number=null;
    totalCost:number=0;
    hideSearchbar:boolean=false;
    comped:boolean=false;
    stripePublicKey:any=null;
    ionViewWillLoad() {
        console.log('ionViewDidLoad TicketPurchasePage');
        this.autoCompleteProvider.initializeAutoComplete(null,
                                                         null,
                                                         this.generatePlayerLoadingFunction(),
                                                         this.eventId);      

        let player_id_for_event = this.navParams.get('player_id_for_event');
        if(player_id_for_event==null){
            return;            
        }
        this.hideSearchbar=true;
        //this.player_id_for_event=player_id_for_event
        this.pssApi.getEventPlayer(this.eventId,player_id_for_event)
            .subscribe(this.generateGetEventPlayerProcessor())                                                  
        
    }
    generateGetEventPlayerProcessor(){
        return (result)=>{
            if(result==null){
                return
            }
            this.selectedPlayer=result.data!=null?result.data:null;
            this.ticketPriceLists=result.tournament_calculated_lists;
            this.ticketCountsDict=result.tournament_counts;
            this.stripePublicKey=result.stripe_public_key
        }
    }
    gotoSuccessPage(purchaseSummary){
            let success_title_string='Tickets Purchased!';
            let successSummary = new SuccessSummary(success_title_string,purchaseSummary.pop(),null);
            successSummary.setSummaryTable(purchaseSummary);
            let successButton = new SuccessButton('Go Home',
                                                  this.getHomePageString(this.eventId),                                                  
                                                  this.buildNavParams({}));            
            this.navCtrl.push("SuccessPage",            
                              this.buildNavParams({'successSummary':successSummary,
                                                   'successButtons':[successButton]}));

    }
    generatePurchaseTicketProcessor(purchaseSummary){
        return (result) => {
            if(result == null){
                return;
            }
            console.log('in generatePurchaseTicketProccesor')            
            if(result.new_token_purchase.completed_purchase==true){
                this.gotoSuccessPage(purchaseSummary)
                return
            } 
            this.launchStripe(result.new_token_purchase.token_purchase_id,purchaseSummary)
            
            

        };
    }
    generateCompleteTicketPurchaseProcessor(purchaseSummary){
        return (result) => {
            if(result == null){
                return;
            }
            console.log('in result')            
            this.gotoSuccessPage(purchaseSummary)
        };
    }
    
    clearValues(){
        this.ticketPriceLists=null;
        this.ticketCounts=null;
        this.selectedPlayer=null;
        //this.player_id_for_event=null;
        this.totalCost=0;

    }

    // onInput(event){        
    //     if(this.player_id_for_event != null && this.player_id_for_event > 99 && this.player_id_for_event < 1000){
    //         console.log('in onInput')
    //         this.pssApi.getEventPlayer(this.eventId,this.player_id_for_event)
    //             .subscribe(this.generateGetEventPlayerProcessor())                                                  

    //     } else {
    //         this.clearValues();
    //     }        
    // }
    onSelect(event){
        this.totalCost=0;
        console.log('in onSelect');
        for(let ticketPrice of this.ticketPriceLists){
            if(ticketPrice.selectedCount!=null){
                this.totalCost=this.totalCost+ticketPrice.selectedCount.price;
            }
            
        }       
    }
    launchStripe(tokenPurchaseId, purchaseSummary){        
        let handler = StripeCheckout.configure({
            key: this.stripePublicKey,
            image: 'https://stripe.com/img/documentation/checkout/marketplace.png',
            locale: 'auto',
            //            token: function(token) {
            token : (token)=>{
                this.pssApi.completeTicketPurchase({stripe_token:token.id,email:token.email},this.eventId,tokenPurchaseId)
                    .subscribe(this.generateCompleteTicketPurchaseProcessor(purchaseSummary))                                                  

                // You can access the token ID with `token.id`.
                // Get the token ID to your server-side code for use.
            }
        });
        handler.open({
            name: 'Stripe.com',
            description: '2 widgets',
            zipCode: true,
            amount: this.totalCost*100
        });
    }
    ticketPurchase(){
        let ticketsToBuy={}
        ticketsToBuy['player_id']=this.selectedPlayer.player_id;
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
        if(this.comped==true){
            ticketsToBuy['comped']=true;
        }
        
        this.pssApi.purchaseTicket(ticketsToBuy,this.eventId)
            .subscribe(this.generatePurchaseTicketProcessor(purchaseSummary))                                                  
        
    }
}
