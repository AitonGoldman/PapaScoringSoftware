import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { EditTournamentPage } from './edit-tournament';
import { ImageUploadModule } from "angular2-image-upload";

@NgModule({
  declarations: [
    EditTournamentPage,
  ],
  imports: [
      IonicPageModule.forChild(EditTournamentPage),
      ImageUploadModule.forRoot()     
  ],
})
export class EditTournamentPageModule {}
