import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { DeskworkerHomePage } from './deskworker-home';

@NgModule({
  declarations: [
    DeskworkerHomePage,
  ],
  imports: [
    IonicPageModule.forChild(DeskworkerHomePage),
  ],
})
export class DeskworkerHomePageModule {}
