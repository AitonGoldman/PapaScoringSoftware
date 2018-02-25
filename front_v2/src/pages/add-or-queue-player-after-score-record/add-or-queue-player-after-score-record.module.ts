import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { AddOrQueuePlayerAfterScoreRecordPage } from './add-or-queue-player-after-score-record';
import { CustomComponentsModule } from '../../components/custom-components.module';
import { IonicImageLoader } from 'ionic-image-loader';

@NgModule({
  declarations: [
    AddOrQueuePlayerAfterScoreRecordPage,
  ],
  imports: [
      IonicPageModule.forChild(AddOrQueuePlayerAfterScoreRecordPage),
      CustomComponentsModule,
      IonicImageLoader
  ],
})
export class AddOrQueuePlayerAfterScoreRecordPageModule {}
