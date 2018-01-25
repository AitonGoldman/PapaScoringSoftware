import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { AddOrQueuePlayerAfterScoreRecordPage } from './add-or-queue-player-after-score-record';
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    AddOrQueuePlayerAfterScoreRecordPage,
  ],
  imports: [
      IonicPageModule.forChild(AddOrQueuePlayerAfterScoreRecordPage),
      CustomComponentsModule,
  ],
})
export class AddOrQueuePlayerAfterScoreRecordPageModule {}
