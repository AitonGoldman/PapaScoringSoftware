import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ScorekeeperStartPlayerPage } from './scorekeeper-start-player';
import { AutoCompleteModule } from 'ionic2-auto-complete';
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    ScorekeeperStartPlayerPage,
  ],
  imports: [
      IonicPageModule.forChild(ScorekeeperStartPlayerPage),
      AutoCompleteModule,
      CustomComponentsModule
  ],
})
export class ScorekeeperStartPlayerPageModule {}
