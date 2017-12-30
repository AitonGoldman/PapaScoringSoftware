import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { TournamentMachinesPage } from './tournament-machines';
import { AutoCompleteModule } from 'ionic2-auto-complete';

@NgModule({
  declarations: [
    TournamentMachinesPage,
  ],
  imports: [
      IonicPageModule.forChild(TournamentMachinesPage),
      AutoCompleteModule
  ],
})
export class TournamentMachinesPageModule {}
