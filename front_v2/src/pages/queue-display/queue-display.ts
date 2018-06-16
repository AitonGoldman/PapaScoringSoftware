import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the QueueDisplayPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'qd/:eventId/:eventName/:cols/:numPlayersPerQueue/:fontSize/:selectedMachines'
})
@Component({
  selector: 'page-queue-display',
  templateUrl: 'queue-display.html',
})
export class QueueDisplayPage extends PssPageComponent {
    fontSize:number = 38;
    machineFontSize = 0;
    nowPlayerFontSize:number = 0;
    playerFontSize:number = 0;
    avgTimeFontSize:number = 0;
    selectedQueues:any=[];
    selectedMachines:any=[];
    cols:any=4;
    numPlayersPerQueue:any=5;
    reload:boolean=true;
    urlString:string="url('/assets/imgs/small_backglass.jpeg')";
    tournaments:any=[];
    displaySettings:any = false;
    
    toggleSettings(){
        this.displaySettings=this.displaySettings==false;
    }
    
    generateGetAllTournamentsAndMachinesAndEventPlayerProcessor(withPlayer=false){
        return (result) => {            
            if(result == null){
                setTimeout(()=>{
                    if(this.reload!=true){
                        return;
                    }
                    this.pssApi.getAllTournamentsAndMachines(this.eventId)            
                        .subscribe(this.generateGetAllTournamentsAndMachinesAndEventPlayerProcessor())
                },5000)
                return;
            }
            this.tournaments=result.data;
            
            this.tournaments.forEach((tournament)=>{
                tournament.tournament_machines=tournament.tournament_machines.sort((n1,n2)=>{                    
                    if(n1.tournament_machine_name>n2.tournament_machine_name){
                        return 1;
                    } else {
                        return -1;
                    }
                })
            })
            this.selectedQueues=[];
            this.tournaments.forEach((tournament)=>{
                tournament.tournament_machines.forEach((tournamentMachine)=>{
                    let matchMachine = this.selectedMachines.filter((machine)=>{
                        if(machine.tournamentMachineId==tournamentMachine.tournament_machine_id){
                            return true;
                        }
                    }).length > 0;
                    console.log('matchMachine');
                    console.log(matchMachine);
                    if(matchMachine==true){
                        console.log(tournamentMachine);
                        tournamentMachine.avgPlayTime=Math.round((tournamentMachine.total_play_time/tournamentMachine.total_number_of_players)/60);
                        if(tournamentMachine.avgPlayTime>100){
                            tournamentMachine.avgPlayTime=0;
                        }
                        this.selectedQueues.push(tournamentMachine);
                    }
                })
            })
            console.log(this.selectedQueues);
            setTimeout(()=>{
                if(this.reload!=true){
                    return;
                }
                this.pssApi.getAllTournamentsAndMachines(this.eventId)            
                    .subscribe(this.generateGetAllTournamentsAndMachinesAndEventPlayerProcessor())
            },15000)
            
        };
    }
    ionViewWillLeave() {
        this.reload=false;
    }
    calcFontSizes(){
        this.machineFontSize = this.fontSize*.75;
        this.nowPlayerFontSize = this.fontSize*.4;
        this.playerFontSize = this.fontSize*.75;
        this.avgTimeFontSize = this.fontSize*.5
    }
    
    launchDialog(){
        let fakeThis=this;
        let alert = this.alertCtrl.create();
        alert.setTitle('Lightsaber color');
        
        alert.addInput({            
            type: 'text',
            name: 'fontSize',
            placeholder: 'fontSize'
        })
        alert.addInput({            
            type: 'text',
            name: 'cols',
            placeholder: 'cols'
        })
        alert.addInput({            
            type: 'text',
            name: 'numPlayersPerQueue',
            placeholder: 'numPlayersPerQueue'
        })        
        alert.addButton('Cancel');
        alert.addButton({
            text: 'OK',
            handler: data => {
                console.log(data);
                this.navCtrl.push('QueueDisplayPage',{eventId:this.eventId,eventName:'eventName',cols:data['cols'],numPlayersPerQueue:data['numPlayersPerQueue'],fontSize:data['fontSize'],selectedMachines:this.navParams.get('selectedMachines')})
                //segment: ':eventId/:baseFontSize/:scrollDelta/test'
                //this.baseFontSize=data['baseFontSize'];
                //this.scrollDelta=data['scrollDelta'];                
                //this.calcFontSizes(this.baseFontSize);
            }
        });
        alert.present();
    }
    
    ionViewWillEnter() {
        this.selectedMachines = JSON.parse(this.navParams.get('selectedMachines'));
        this.cols = this.navParams.get('cols');
        this.numPlayersPerQueue = this.navParams.get('numPlayersPerQueue')?this.navParams.get('numPlayersPerQueue'):8;
        this.fontSize = this.navParams.get('fontSize');        
        this.calcFontSizes();
        console.log(this.selectedMachines);
        this.pssApi.getAllTournamentsAndMachines(this.eventId)            
            .subscribe(this.generateGetAllTournamentsAndMachinesAndEventPlayerProcessor())
    }

}
