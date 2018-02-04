import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

import { trigger, style, transition, animate } from '@angular/animations'

/**
 * Generated class for the ScorekeeperFinalsMatchPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'ScorekeeperFinalsMatch/:eventId/:finalId/:round/:matchId'
})
@Component({
  selector: 'page-scorekeeper-finals-match',
    templateUrl: 'scorekeeper-finals-match.html',
    animations: [
        trigger('myvisibility', [
            transition(':enter', [
                style({transform: 'translateX(100%)', opacity: 0}),
                animate('500ms', style({transform: 'translateX(0)', opacity: 1}))
            ]),
            transition(':leave', [
                style({transform: 'translateX(0)', opacity: 1}),
                animate('500ms', style({transform: 'translateX(100%)', opacity: 0}))
            ])            
        ])
  ]    
})
export class ScorekeeperFinalsMatchPage extends PssPageComponent {
    match:any=null;
    finalId:any=null;
    round:number=null;
    matchId:number=null;
    takenOrderPosition:any=[];
    gameOrderLists:any=null;
    gameOrderListsDisplay:any=null;
    gameDisplay:any=null;
    playerOrderInGame:any={};
    scoreOrderLists:any=null;
    visibleState = 'visible';

    //game_one_player_order_display:boolean=false;
    //game_one_player_order_list:any=null;
    toggleVisible() {
        this.visibleState = (this.visibleState == 'visible') ? 'invisible' : 'visible';
    }    
    setPlayerOrder(order,player,game){        
        let player_string=player.player;
        player.order=order;
        this.takenOrderPosition.push(order);
        this.match[player_string+'_order_'+game]=order;
        this.pssApi.editFinalsMatch(this.match,this.eventId,this.matchId)
            .subscribe((result)=>{
                if(result==null){
                    return;
                }
                this.match=result;
                if (this.checkAllPlayerOrderSet(game)){
                    this.gameDisplay[game]=true;
                    this.scoreOrderLists[game]=this.generateListForOrderPicking(game,"order")                    
                }                
            })                                                          
        
    }
    checkAllPlayerOrderSet(machineNum){
        if(this.match["player_one_order_"+machineNum]==null){
            return false;
        }
        if(this.match["player_two_order_"+machineNum]==null){
            return false;
        }
        if(this.match["player_three_order_"+machineNum]==null){
            return false;
        }
        if(this.match["player_four_order_"+machineNum]==null){
            return false;
        }
        return true;
    }
    showPlayerOrder(machineNum){
        //this.toggleVisible()
        this.gameOrderListsDisplay[machineNum]=this.gameOrderListsDisplay[machineNum]==false
        this.takenOrderPosition=[];
    }
    generateListForOrderPicking(machineNum,type){
        let orderList=[];
        //this.takenOrderPosition=[];
        ['player_one','player_two','player_three','player_four'].forEach((player_string)=>{
            let player_info = {name:this.match[player_string+"_name"],
                               player:player_string,
                               rank:this.match[player_string+"_rank"],
                               score:null,
                               order:null
                              }
            if(machineNum>1){
                player_info.score=this.match[player_string+"_score_"+(machineNum-1)]                
            }
            if(this.match[player_string+"_order_"+machineNum]!=null){
                player_info.order=this.match[player_string+"_order_"+machineNum];
            }
            orderList.push(player_info)
        })
        //let sortBy=machineNum==1?"rank":"points"
        let sortBy=type
        orderList=orderList.sort((n1,n2)=>{
            if(n1[sortBy] < n2[sortBy]){
                return -1;
            }
            if(n1[sortBy] > n2[sortBy]){
                return 1;
            }
            return 0;                                                            
        })
       return orderList 
    }
    saveScores(){
        this.pssApi.editFinalsMatch(this.match,this.eventId,this.matchId)
            .subscribe((result)=>{
                if(result==null){
                    return;
                }
                this.match=result;
                this.gameOrderLists[1]=this.generateListForOrderPicking(1,"rank");            
                this.gameOrderLists[2]=this.generateListForOrderPicking(2,"score");
                this.gameOrderLists[3]=this.generateListForOrderPicking(3,"score");
                
            })                                                          
    }
    
    generateGetFinalProcessor(){
        return (result)=>{
            if(result==null){
                return
            }
            let final=result.data[this.round];
            this.match = final.filter((match)=>{
                if(match.finals_match_id==this.matchId){
                    return true;
                }
                return false;
            })[0];
            console.log(this.match);
            console.log(final);
            this.gameOrderLists={}                        
            this.gameOrderLists[1]=this.generateListForOrderPicking(1,"rank");
            
            this.gameOrderLists[2]=this.generateListForOrderPicking(2,"score");
            this.gameOrderLists[3]=this.generateListForOrderPicking(3,"score");
            this.gameOrderListsDisplay={};
            this.gameOrderListsDisplay[1]=false;            
            this.gameOrderListsDisplay[2]=false;            
            this.gameOrderListsDisplay[3]=false;            
            this.gameDisplay={};
            this.gameDisplay[1]=false;
            this.gameDisplay[2]=false;
            this.gameDisplay[3]=false;            
            [1,2,3,4].forEach((game)=>{
                if (this.checkAllPlayerOrderSet(game)){
                    this.gameDisplay[game]=true;
                }                
            })
            this.scoreOrderLists={}
            this.scoreOrderLists[1]=this.generateListForOrderPicking(1,"order")
            this.scoreOrderLists[2]=this.generateListForOrderPicking(2,"order")
            this.scoreOrderLists[3]=this.generateListForOrderPicking(3,"order")
            
            console.log('generateGetEventPlayer')
            
        }
    }
    debug(thing_to_debug){
        console.log(thing_to_debug);
    }
    ionViewWillEnter() {
        this.finalId=this.navParams.get('finalId');
        this.round=this.navParams.get('round');
        this.matchId=this.navParams.get('matchId')        
        this.pssApi.getFinal(this.eventId,this.finalId)
            .subscribe(this.generateGetFinalProcessor())                                                          
      console.log('ionViewDidLoad ScorekeeperFinalsRoundPage');
    }

    ionViewDidLoad() {
        console.log('ionViewDidLoad ScorekeeperFinalsMatchPage');
    }
    saveTiebreakerScores(){
        this.pssApi.saveFinalsMatchTiebreakersScore(this.match,this.eventId,this.match.tiebreaker.tiebreaker_id,this.match.finals_match_id)
            .subscribe(this.generateSaveFinalsBootstrapTiebreakersScoreProcessor())                                                          
    }
    generateSaveFinalsBootstrapTiebreakersScoreProcessor(){
        return (result)=>{
            if(result==null){
                return;
            }
            //this.tiebreaker=result.data;
            console.log(result)
            let msg="Score Saved";
            if(result.tiebreaker.completed){
                msg="Tiebreaker Completed";
            }
            let toast = this.toastCtrl.create({
                message:  msg,
                duration: 99000,
                position: 'top',
                showCloseButton: true,
                closeButtonText: " ",
                cssClass: "successToast"
            });            
            toast.present();                                                                
        }
    }
}
