import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { TournamentMachinesPage } from './tournament-machines';
import { AutoCompleteModule } from 'ionic2-auto-complete';
import { SimpleNotificationsModule } from 'angular2-notifications';

@NgModule({
  declarations: [
    TournamentMachinesPage,
  ],
  imports: [
      IonicPageModule.forChild(TournamentMachinesPage),
      AutoCompleteModule,
      SimpleNotificationsModule.forRoot()
  ],
})
export class TournamentMachinesPageModule {}
