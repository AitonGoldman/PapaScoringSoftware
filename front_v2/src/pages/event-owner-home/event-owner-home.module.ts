import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { EventOwnerHomePage } from './event-owner-home';

@NgModule({
  declarations: [
    EventOwnerHomePage,
  ],
  imports: [
      IonicPageModule.forChild(EventOwnerHomePage)      
  ],
})
export class EventOwnerHomePageModule {}
