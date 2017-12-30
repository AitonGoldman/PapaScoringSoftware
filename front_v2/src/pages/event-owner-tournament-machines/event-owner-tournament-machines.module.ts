import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { EventOwnerTournamentMachinesPage } from './event-owner-tournament-machines';
import { AutoCompleteModule } from 'ionic2-auto-complete';
import { SimpleNotificationsModule } from 'angular2-notifications';

@NgModule({
  declarations: [
    EventOwnerTournamentMachinesPage,
  ],
  imports: [
      IonicPageModule.forChild(EventOwnerTournamentMachinesPage),
      AutoCompleteModule,
      SimpleNotificationsModule.forRoot()      
  ],
})
export class EventOwnerTournamentMachinesPageModule {}
