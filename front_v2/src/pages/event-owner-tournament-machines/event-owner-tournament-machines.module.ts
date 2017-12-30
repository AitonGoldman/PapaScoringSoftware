import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { EventOwnerTournamentMachinesPage } from './event-owner-tournament-machines';
import { AutoCompleteModule } from 'ionic2-auto-complete';

@NgModule({
  declarations: [
    EventOwnerTournamentMachinesPage,
  ],
  imports: [
      IonicPageModule.forChild(EventOwnerTournamentMachinesPage),
      AutoCompleteModule      
  ],
})
export class EventOwnerTournamentMachinesPageModule {}
