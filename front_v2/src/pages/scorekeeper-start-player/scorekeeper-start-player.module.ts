import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ScorekeeperStartPlayerPage } from './scorekeeper-start-player';
import { AutoCompleteModule } from 'ionic2-auto-complete';
import { CustomComponentsModule } from '../../components/custom-components.module';
import { IonicImageLoader } from 'ionic-image-loader';

@NgModule({
  declarations: [
    ScorekeeperStartPlayerPage,
  ],
  imports: [
      IonicPageModule.forChild(ScorekeeperStartPlayerPage),
      AutoCompleteModule,
      CustomComponentsModule,
      IonicImageLoader
  ],
})
export class ScorekeeperStartPlayerPageModule {}
