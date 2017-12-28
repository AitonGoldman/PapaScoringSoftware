import { NgModule } from '@angular/core';
import { PssPageComponent } from './pss-page/pss-page';
import { CustomHeaderComponent } from './custom-header/custom-header';
@NgModule({
	declarations: [
    PssPageComponent,    
    CustomHeaderComponent],
	imports: [],
	exports: [
    PssPageComponent,
    CustomHeaderComponent]
})
export class ComponentsModule {}
