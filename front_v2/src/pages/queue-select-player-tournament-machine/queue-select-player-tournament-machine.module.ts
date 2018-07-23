import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { QueueSelectPlayerTournamentMachinePage } from './queue-select-player-tournament-machine';
import { CustomComponentsModule } from '../../components/custom-components.module';
import { ExpandableModule } from '../../components/expandable/expandable.module'

@NgModule({
  declarations: [
    QueueSelectPlayerTournamentMachinePage,
  ],
  imports: [
    IonicPageModule.forChild(QueueSelectPlayerTournamentMachinePage),
      ExpandableModule,
      CustomComponentsModule,
  ],
})
export class QueueSelectPlayerTournamentMachinePageModule {}
