import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { TournamentDirectorHomePage } from './tournament-director-home';
import { SimpleNotificationsModule } from 'angular2-notifications';

@NgModule({
  declarations: [
    TournamentDirectorHomePage,
  ],
  imports: [
      IonicPageModule.forChild(TournamentDirectorHomePage),
      SimpleNotificationsModule.forRoot()
  ],
})
export class TournamentDirectorHomePageModule {}
