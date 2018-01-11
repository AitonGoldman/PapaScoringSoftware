import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { QueueSelectPlayerTournamentMachinePage } from './queue-select-player-tournament-machine';

@NgModule({
  declarations: [
    QueueSelectPlayerTournamentMachinePage,
  ],
  imports: [
    IonicPageModule.forChild(QueueSelectPlayerTournamentMachinePage),
  ],
})
export class QueueSelectPlayerTournamentMachinePageModule {}
