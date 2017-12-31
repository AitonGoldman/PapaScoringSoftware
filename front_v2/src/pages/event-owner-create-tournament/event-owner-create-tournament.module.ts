import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { EventOwnerCreateTournamentPage } from './event-owner-create-tournament';
import { ImageUploadModule } from "angular2-image-upload";

@NgModule({
  declarations: [
    EventOwnerCreateTournamentPage,
  ],
  imports: [
      IonicPageModule.forChild(EventOwnerCreateTournamentPage),
      ImageUploadModule.forRoot()
      
  ],
})
export class EventOwnerCreateTournamentPageModule {}
