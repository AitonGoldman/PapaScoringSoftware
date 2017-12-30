import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { CreateTournamentPage } from './create-tournament';

@NgModule({
  declarations: [
    CreateTournamentPage,
  ],
  imports: [
    IonicPageModule.forChild(CreateTournamentPage),
  ],
})
export class CreateTournamentPageModule {}
