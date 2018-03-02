import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { DeskworkerHomePage } from './deskworker-home';
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    DeskworkerHomePage,
  ],
  imports: [
      IonicPageModule.forChild(DeskworkerHomePage),
      CustomComponentsModule,
  ],
})
export class DeskworkerHomePageModule {}
