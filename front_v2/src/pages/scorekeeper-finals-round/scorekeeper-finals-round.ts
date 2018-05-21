import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the ScorekeeperFinalsRoundPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-scorekeeper-finals-round',
  templateUrl: 'scorekeeper-finals-round.html',
})
export class ScorekeeperFinalsRoundPage extends PssPageComponent{

    finalId:number=null;
    finalName:string=null;
    final:any=null;
    round:number=null;
    totalRounds:number=null;
    roundCompleted:boolean=false;
    finalsPlayers:any = null;

    generateGetEventPlayerProcessor(){
        return (result)=>{
            if(result==null){
                return
            }
            this.finalName=result.final_name;
            console.log('in finals rounds...');
            console.log(result.data)
            this.final=result.data[this.round];
            this.finalsPlayers=result.finals_players;
            
            let completedCount=0;            
            this.final.forEach((round)=>{
                console.log(round);
                if(round.completed==true){
                    completedCount=completedCount+1;
                }
            })
            if(completedCount==this.final.length){
                this.roundCompleted=true;
            }
            this.final.map((match)=>{
                if(match.bye_player_one_name!=null && match.player_one_name==null){
                    match.player_one_name=match.bye_player_one_name;
                }
                if(match.bye_player_two_name!=null && match.player_two_name==null){
                    match.player_two_name=match.bye_player_two_name;
                }
                match.player_one_points=match.player_one_points_1+match.player_one_points_2+match.player_one_points_3
                match.player_two_points=match.player_two_points_1+match.player_two_points_2+match.player_two_points_3
                match.player_three_points=match.player_three_points_1+match.player_three_points_2+match.player_three_points_3
                match.player_four_points=match.player_four_points_1+match.player_four_points_2+match.player_four_points_3
                
                if(match.one_completed!=true && match.machine_1){
                    match.current_machine=match.machine_1;                    
                }
                if(match.two_completed!=true && match.machine_2){
                    match.current_machine=match.machine_2;                    
                }
                if(match.three_completed!=true && match.machine_3){
                    match.current_machine=match.machine_3;
                }                                
                return match
            })
            console.log('generateGetEventPlayer')
            console.log(this.final);            
        }
    }

    reloadResults(){
        this.pssApi.getFinal(this.eventId,this.finalId)
            .subscribe(this.generateGetEventPlayerProcessor());        
    }
    
    ionViewWillEnter() {
        if(this.eventId==null){
            this.pushRootPage('EventSelectPage')
            return;
        }

        this.finalId=this.navParams.get('finalId');
        this.round=this.navParams.get('round');
        this.pssApi.getFinal(this.eventId,this.finalId)
            .subscribe(this.generateGetEventPlayerProcessor())                                                          
      console.log('ionViewDidLoad ScorekeeperFinalsRoundPage');
    }

    generateCompleteRoundProcessor(){
        return (result)=>{
            if(result==null){
                return;
            }
        }
    }
    completeRound(){
        this.pssApi.completeRound({},this.eventId,this.finalId,this.round)
            .subscribe(this.generateCompleteRoundProcessor())                                                          
    }
    
}
