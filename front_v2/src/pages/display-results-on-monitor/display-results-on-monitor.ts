import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, AlertController } from 'ionic-angular';
import { trigger, stagger, state, style, transition, animate  } from '@angular/animations'
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the DisplayResultsOnMonitorPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage(
    {
    segment: ':eventId/:baseFontSize/:scrollDelta/:typeOfResults/test'
})
@Component({
  selector: 'page-display-results-on-monitor',
    templateUrl: 'display-results-on-monitor.html',
    animations: [
        trigger('scrollAnim', [
            state('inactive', style({opacity: 1, transform: 'translateY(0)'})),
            state('active',   style({opacity: 1 })),
            
            state('void',   style({opacity: 0, display: 'none', transform: 'translateY(0) scale(1)'})),
            transition('* => inactive', [                
                animate('1000ms', style({
                    opacity: 1,
                    //transform: 'translateY(-{{amountToScroll}}00%)'
                    transform: 'translateY(-{{amountToScroll}}00%)'
                }))
            ])
            
        ])
    ],    
})
export class DisplayResultsOnMonitorPage extends PssPageComponent {
    tournaments:any=[];
    currentTournament:any={};
    currentTournamentMachine:any={};    
    currentTournamentMachineCount:any=0;
    currentResults:any=[];
    tournament_machines:any=[];
    tournament_machines_for_chip_display:any=[];
    scrollDelta:any = 10;
    killTimer:any = false;
    
    baseFontSize:any = 12
    tournamentMachineChipFontSize:any = 0;
    titleFontSize:any = 0;
    columnTitleFontSize:any = 0;
    columnContentFontSize:any = 0;
    topMachineFontSize:any = 0;
    loading_instance:any = null;
    
    typeOfResults:any = "tournament";
    
    genResults(){
        for (let i = 0; i < 100; i++) {            
        }

    }

    getNextTournament(){        
        this.currentTournament = this.tournaments.shift();
        this.tournaments.push(this.currentTournament);
        this.tournament_machines_for_chip_display=[];
        for(let machine of this.currentTournament.tournament_machines){
            
            this.tournament_machines_for_chip_display.push(machine);
        }
        
    }

    getNextTournamentMachine(){        
        this.currentTournamentMachineCount=this.currentTournamentMachineCount+1        
        if(this.currentTournamentMachineCount>=this.currentTournament.tournament_machines.length){
            this.currentTournamentMachineCount=1;
            this.getNextTournament();
        }
        this.currentTournamentMachine = this.currentTournament.tournament_machines.shift();
        this.currentTournament.tournament_machines.push(this.currentTournamentMachine);                
    }
    

    getTournamentResults(){

        if(this.killTimer==true){
            return;
        }
        this.loading_instance = this.loadingCtrl.create({content: 'Please wait...'});        
        this.loading_instance.present();        
        this.pssApi.getTournamentResultsHidden(this.eventId,this.currentTournament.tournament_id)            
            .subscribe((results)=>{
                if(results==null){
                    setTimeout(()=>{
                        this.loading_instance.dismiss();
                        this.getTournamentResults();
                    },1000)                    
                    return 
                }
                this.loading_instance.dismiss();                
                this.currentResults=results.data;
                this.currentResults.push({})                
                console.log(this.currentResults);
                setTimeout(()=>{
                    this.scrollAnimationTest();
                },7000)
                
            })
    }

    getTournamentMachineResults(){
        if(this.killTimer==true){
            return;
        }                         
        this.loading_instance = this.loadingCtrl.create({content: 'Please wait...'});        
        this.loading_instance.present();        

        this.pssApi.getTournamentMachineResultsHidden(this.eventId,this.currentTournament.tournament_id,this.currentTournamentMachine.tournament_machine_id)           
            .subscribe((results)=>{                
                if(results==null){
                    setTimeout(()=>{
                        this.loading_instance.dismiss();
                        this.getTournamentMachineResults();
                    },1000)
                    
                    return 
                }
                this.currentResults=results.data;
                this.currentResults.push({})                
                this.loading_instance.dismiss();
                setTimeout(()=>{
                    this.scrollAnimationTest();
                },7000)
                
            })
    }
    
    ionViewDidLoad() {
        //this.genResults();        
        this.eventId = this.navParams.get("eventId");
        this.baseFontSize = this.navParams.get("baseFontSize");
        this.scrollDelta = this.navParams.get("scrollDelta");
        this.typeOfResults = this.navParams.get("typeOfResults");        
        this.calcFontSizes(this.baseFontSize);
        console.log('ionViewDidLoad DisplayResultsOnMonitorPage');
        //this.loading_instance = this.loadingCtrl.create({content: 'Please wait...'});
        this.pssApi.getAllTournamentsAndMachinesHidden(this.eventId)            
            .subscribe((tournaments)=>{
                this.tournaments=tournaments.data;
                
                this.getNextTournament();
                this.getNextTournamentMachine();
                if(this.typeOfResults=="tournament"){
                    this.getTournamentResults();
                } else {               
                    this.getTournamentMachineResults();
                }
                
                
            })

        
    }
    
    ionViewDidEnter(){        
        // pop first tournament off list, and then add to end of tournament lists
        // go through each result in tournament
        // grab next tournament off list
                
    }
    ionViewDidLeave(){        
        //alert('bye now');
        this.killTimer=true;
        // pop first tournament off list, and then add to end of tournament lists
        // go through each result in tournament
        // grab next tournament off list
                
    }
    
    animationCallBack(event){                        
        if(event.toState=="inactive"){                                                
            for(let y = 0; y<this.scrollDelta;y++){
                this.currentResults.shift();
            }                        
            for(let x = 0;x<this.currentResults.length;x++){
                this.currentResults[x].deleted='active';            
            }
            if(this.killTimer==true){
                //return;
            }
            setTimeout(()=>{
                if(this.currentResults.length==0 || this.currentResults.length < this.scrollDelta){
                    if(this.typeOfResults=="tournament"){
                        this.getNextTournament();
                        this.getTournamentResults();
                    } else {
                        this.getNextTournamentMachine();
                        this.getTournamentMachineResults();                
                    }                    
                    return
                }                
                this.scrollAnimationTest()
            },7000)
            
        }
    }
    
    scrollAnimationTest(){        
        for(let x = 0;x<this.currentResults.length;x++){
            this.currentResults[x].deleted='inactive';            
        }
    }
    
    launchDialog(){
        let fakeThis=this;
        let alert = this.alertCtrl.create();
        alert.setTitle('Lightsaber color');
        
        alert.addInput({            
            type: 'text',
            name: 'baseFontSize',
            placeholder: 'baseFontSize'
        })
        alert.addInput({            
            type: 'text',
            name: 'scrollDelta',
            placeholder: 'scrollDelta'
        })
        alert.addInput({            
            type: 'text',
            name: 'typeOfResults',
            placeholder: 'typeOfResults'
        })        
        alert.addButton('Cancel');
        alert.addButton({
            text: 'OK',
            handler: data => {
                console.log(data);
                this.navCtrl.push('DisplayResultsOnMonitorPage',{eventId:this.eventId,baseFontSize:data['baseFontSize'],scrollDelta:data['scrollDelta'],typeOfResults:data['typeOfResults']})
                //segment: ':eventId/:baseFontSize/:scrollDelta/test'
                //this.baseFontSize=data['baseFontSize'];
                //this.scrollDelta=data['scrollDelta'];                
                //this.calcFontSizes(this.baseFontSize);
            }
        });
        alert.present();
    }
    calcFontSizes(baseFontSize){
        this.baseFontSize=baseFontSize;
        this.tournamentMachineChipFontSize = this.baseFontSize/2;
        this.titleFontSize = this.baseFontSize*2;    
        this.columnTitleFontSize = this.baseFontSize*.75;    
        this.columnContentFontSize = this.baseFontSize;    
        this.topMachineFontSize = this.baseFontSize*.75;        
    }
}
