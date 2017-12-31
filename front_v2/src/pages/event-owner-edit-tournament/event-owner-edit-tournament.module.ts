import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { EventOwnerEditTournamentPage } from './event-owner-edit-tournament';
import { ImageUploadModule } from "angular2-image-upload";

@NgModule({
  declarations: [
    EventOwnerEditTournamentPage,
  ],
  imports: [
    IonicPageModule.forChild(EventOwnerEditTournamentPage),
      ImageUploadModule.forRoot()
  ],
})
export class EventOwnerEditTournamentPageModule {}
