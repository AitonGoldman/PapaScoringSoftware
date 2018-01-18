import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { TournamentMachinesPage } from './tournament-machines';
import { AutoCompleteModule } from 'ionic2-auto-complete';
import { SimpleNotificationsModule } from 'angular2-notifications';
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    TournamentMachinesPage,
  ],
  imports: [
      IonicPageModule.forChild(TournamentMachinesPage),
      AutoCompleteModule,
      SimpleNotificationsModule.forRoot(),
      CustomComponentsModule     
  ],
})
export class TournamentMachinesPageModule {}
