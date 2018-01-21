import { Component } from '@angular/core';
import { ViewController } from 'ionic-angular';
import { NavParams } from 'ionic-angular';
/**
 * Generated class for the TopThreePopoverComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */

@Component({
  template: `    
    <ion-list>
      <ion-list-header>Top 3 machines</ion-list-header>
      <button (click)="close(machine.tournament_machine_id,machine.tournament_machine_name)" ion-item  *ngFor="let machine of machines">#{{machine.rank}} on {{machine.abbreviation}} </button>
       <!-- [navPush]="'ResultsMachinePage'" [navParams]="addMachineIdName(machine.tournament_machine_id,'poopMachine',linkParams)" -->
    </ion-list>
  `
})
export class TopThreePopoverComponent {
    machines:any= null;
    linkParams:any = null;
    tabCtrl:any = null;
    constructor(public viewCtrl: ViewController, public navParams: NavParams) {
        console.log(this.navParams.data);
        this.machines = this.navParams.get('machines');
        this.linkParams = this.navParams.get('linkParams');
        this.tabCtrl = this.navParams.get('tabNavCtrl');
    }
    addMachineIdName(machineId,machineName,linkParams){
        linkParams.tournamentMachineId=machineId;
        linkParams.tournamentMachineName=machineName;
        return linkParams;
    }
    close(tournamentMachineId,tournamentMachineName) {
        this.linkParams.tournamentMachineId=tournamentMachineId;
        this.linkParams.tournamentMachineName=tournamentMachineName;
        
        this.viewCtrl.dismiss();
        this.tabCtrl.push('ResultsMachinePage',this.linkParams)
  }
}
