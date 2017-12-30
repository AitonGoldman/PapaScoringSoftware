import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { EventOwnerCreateTournamentPage } from './event-owner-create-tournament';

@NgModule({
  declarations: [
    EventOwnerCreateTournamentPage,
  ],
  imports: [
    IonicPageModule.forChild(EventOwnerCreateTournamentPage),
  ],
})
export class EventOwnerCreateTournamentPageModule {}
