import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { AddPlayerToQueuePage } from './add-player-to-queue';
import { AutoCompleteModule } from 'ionic2-auto-complete';
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    AddPlayerToQueuePage,
  ],
  imports: [
      AutoCompleteModule,
      IonicPageModule.forChild(AddPlayerToQueuePage),
      CustomComponentsModule,
  ],
})
export class AddPlayerToQueuePageModule {}
