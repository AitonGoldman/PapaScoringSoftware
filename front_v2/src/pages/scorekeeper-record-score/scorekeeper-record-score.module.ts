import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ScorekeeperRecordScorePage } from './scorekeeper-record-score';
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    ScorekeeperRecordScorePage,
  ],
  imports: [
      IonicPageModule.forChild(ScorekeeperRecordScorePage),
      CustomComponentsModule
  ],
})
export class ScorekeeperRecordScorePageModule {}
