import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { TicketPurchasePage } from './ticket-purchase';

@NgModule({
  declarations: [
    TicketPurchasePage,
  ],
  imports: [
    IonicPageModule.forChild(TicketPurchasePage),
  ],
})
export class TicketPurchasePageModule {}
