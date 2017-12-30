import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { TournamentDirectorHomePage } from './tournament-director-home';

@NgModule({
  declarations: [
    TournamentDirectorHomePage,
  ],
  imports: [
    IonicPageModule.forChild(TournamentDirectorHomePage),
  ],
})
export class TournamentDirectorHomePageModule {}
