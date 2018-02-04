import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the FinalsBootstrapPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment: 'FinalsBootstrap/:eventId/:eventName/:tournamentId/:finalName'
})
@Component({
  selector: 'page-finals-bootstrap',
  templateUrl: 'finals-bootstrap.html',
})
export class FinalsBootstrapPage extends PssPageComponent{
    tournamentId:number=null
    tiebreakers:any=null;
    hasTiebreakers:boolean=false;
    hasUncompletedTiebreakers:boolean=true;
    finalsPlayers:any=null;
    numberQualifiers:number=null;
    dividerIndex:number=null;
    final:any=null;
    finalName:string=null;
    displayRollCall:boolean=true;
    
    getDividerIndex(){
        let dividerIndex=0;        
        let presentPlayerCount=0;
        this.finalsPlayers.forEach((fp,index)=>{
            console.log('hi there');
            if(fp.present==true){
                presentPlayerCount=presentPlayerCount+1;                
            }
            if(presentPlayerCount>this.numberQualifiers){
                return;
            }
            if(presentPlayerCount+1==this.numberQualifiers+1 && fp.present==false){
                return;
            }
            
            dividerIndex=dividerIndex+1;
            
        })
        this.dividerIndex = dividerIndex;
    }
    
    generateGetFinalsTiebreakersRollCallProcessor(){
        return (result)=>{
            if(result==null){
                return;
            }
            this.numberQualifiers = result.tournament_qualifiers;
            this.final=result.final;
            this.finalsPlayers=result.finals_players.sort((n1,n2)=>{
                if(n1.finals_rank < n2.finals_rank){
                    return -1;
                }
                if(n1.finals_rank > n2.finals_rank){
                    return 1;
                }
                return 0;                                
            })
            this.finalsPlayers.forEach((fp)=>{
                fp.present=true;
            })
            this.getDividerIndex()
            this.tiebreakers=result.data.sort((n1,n2)=>{
                if(n1.tiebreaker_id < n2.tiebreaker_id){
                    return -1;
                }
                if(n1.tiebreaker_id > n2.tiebreaker_id){
                    return 1;
                }
                return 0;                

            });
            this.tiebreakers.forEach((tiebreaker,idx)=>{
                tiebreaker.players = tiebreaker.players.sort((n1,n2)=>{
                    if(n1.player_name < n2.player_name){
                        return -1;
                    }
                    if(n1.player_name > n2.player_name){
                        return 1;
                    }
                    return 0;                                    
                })
            })
            let num_completed = this.tiebreakers.filter((tie)=>{
                if(tie.completed==true){
                    return true;
                } else {
                    return false;
                }
            }).length;
            if(num_completed == this.tiebreakers.length || this.tiebreakers.length == 0){
                this.hasUncompletedTiebreakers=false;
            } else {
                this.hasUncompletedTiebreakers=true;
            }
            console.log(result)
        }
    }
    generateGenerateFinalsBracketProcessor(){
        return (result)=>{
            if (result==null){
                return
            }
            this.final=result.data;
        }
    }    
    generateBrackets() {
        this.pssApi.generateFinalsBracket({description:this.finalName,data:this.finalsPlayers},this.eventId,this.tournamentId)
            .subscribe(this.generateGenerateFinalsBracketProcessor())                                                          
        
    }
    ionViewWillEnter() {
        console.log('ionViewDidLoad FinalsBootstrapPage');
        this.tournamentId=this.navParams.get('tournamentId')
        this.finalName=this.navParams.get('finalName')
        this.pssApi.getFinalsTiebreakersRollCall(this.eventId,this.tournamentId,this.finalName)
            .subscribe(this.generateGetFinalsTiebreakersRollCallProcessor())                                                          

    }
    absentPlayerCount(index){
        let count = 0;
        while(index>0){
            index=index-1;
            if(this.finalsPlayers[index].present==false){
                count=count+1;
            }            
        }        
        return count;
    }
}
