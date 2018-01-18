import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { QueueSelectPlayerTournamentMachinePage } from './queue-select-player-tournament-machine';
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    QueueSelectPlayerTournamentMachinePage,
  ],
  imports: [
    IonicPageModule.forChild(QueueSelectPlayerTournamentMachinePage),
      CustomComponentsModule,
  ],
})
export class QueueSelectPlayerTournamentMachinePageModule {}
