import { NgModule } from '@angular/core';
import { PssPageComponent } from './pss-page/pss-page';
import { CustomHeaderComponent } from './custom-header/custom-header';
import { CreateEditEntityComponent } from './create-edit-entity/create-edit-entity';
@NgModule({
	declarations: [
    PssPageComponent,    
    CustomHeaderComponent,
    CreateEditEntityComponent],
	imports: [],
	exports: [
    PssPageComponent,
    CustomHeaderComponent,
    CreateEditEntityComponent]
})
export class ComponentsModule {}
