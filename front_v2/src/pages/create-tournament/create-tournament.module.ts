import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { CreateTournamentPage } from './create-tournament';
import { ImageUploadModule } from "angular2-image-upload";

@NgModule({
  declarations: [
    CreateTournamentPage,
  ],
  imports: [
      IonicPageModule.forChild(CreateTournamentPage),
      ImageUploadModule.forRoot()
  ],
})
export class CreateTournamentPageModule {}
