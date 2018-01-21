export class EntityFields  {        
    fields = {}
    fieldsArray = [];
    constructor(public entityType:string) {
    }
    setField(fieldName,fieldType,basic,advanced,description){
        let field = {
            fieldName:fieldName,
            fieldType:fieldType,
            advanced:advanced,
            basic:basic,
            description:description
        }
        this.fields[fieldName]=field
        //this.fieldsArray.push(field);
    }
    setDependency(fieldName,dependsOn,value){
        this.fields[fieldName].dependsOn={
            dependsOn:dependsOn,
            value:value
        }
    }
    getFields(){
        return this.fields;
    }
    getFieldsArray(advanced){        
        let fieldsArray=[];        
        for(let i in this.fields){            
            fieldsArray.push(this.fields[i]);
        }
        if(advanced==false){
            return fieldsArray.filter((field)=>{return field.basic==true});    
        } else {
            return fieldsArray;
        }
        
    }
}