import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { TournamentDirectorHomePage } from './tournament-director-home';
import { SimpleNotificationsModule } from 'angular2-notifications';
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    TournamentDirectorHomePage,
  ],
  imports: [
      IonicPageModule.forChild(TournamentDirectorHomePage),
      SimpleNotificationsModule.forRoot(),
      CustomComponentsModule
  ],
})
export class TournamentDirectorHomePageModule {}
