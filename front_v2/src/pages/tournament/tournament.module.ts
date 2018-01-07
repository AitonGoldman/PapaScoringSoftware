import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { TournamentPage } from './tournament';
import { ImageUploadModule } from "angular2-image-upload";

@NgModule({
  declarations: [
    TournamentPage,
  ],
  imports: [
      IonicPageModule.forChild(TournamentPage),
      ImageUploadModule.forRoot()      
  ],
})
export class TournamentPageModule {}
