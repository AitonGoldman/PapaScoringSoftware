import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { TicketPurchasePage } from './ticket-purchase';
import { AutoCompleteModule } from 'ionic2-auto-complete';
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    TicketPurchasePage,
  ],
  imports: [
      IonicPageModule.forChild(TicketPurchasePage),
      AutoCompleteModule,
      CustomComponentsModule,      
  ],
})
export class TicketPurchasePageModule {}
