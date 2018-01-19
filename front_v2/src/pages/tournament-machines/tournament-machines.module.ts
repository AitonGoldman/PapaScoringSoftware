import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { TournamentMachinesPage } from './tournament-machines';
import { AutoCompleteModule } from 'ionic2-auto-complete';
import { SimpleNotificationsModule } from 'angular2-notifications';
import { CustomComponentsModule } from '../../components/custom-components.module';
import { ImageUploadModule } from "angular2-image-upload";

@NgModule({
  declarations: [
    TournamentMachinesPage,
  ],
  imports: [
      IonicPageModule.forChild(TournamentMachinesPage),
      AutoCompleteModule,
      SimpleNotificationsModule.forRoot(),
      CustomComponentsModule,
      ImageUploadModule.forRoot()
  ],
})
export class TournamentMachinesPageModule {}
