import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { EventOwnerHomePage } from './event-owner-home';
import { ExpandableModule } from '../../components/expandable/expandable.module'
import { SimpleNotificationsModule } from 'angular2-notifications';

@NgModule({
  declarations: [
      EventOwnerHomePage      
  ],
  imports: [
      IonicPageModule.forChild(EventOwnerHomePage),
      ExpandableModule,
      SimpleNotificationsModule.forRoot()      
  ],
})
export class EventOwnerHomePageModule {}
