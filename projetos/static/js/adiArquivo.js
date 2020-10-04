
function tipoGenericoCarregada(){
    var myOpts = document.getElementById('generico');
    for (x=1;x<myOpts.length;x++){
        var aux = myOpts[x].value
        document.getElementById(aux).style.display="none";
}
}
function tipoGenerico(){
    var atual = document.getElementById('generico');
    var lista = document.getElementById('generico').options;
    for (x=0;x<lista.length;x++){
        if(lista[x].value == atual.value){
            document.getElementById(atual.value).style.display="";
        }else{
            document.getElementById(lista[x].value).style.display="none";
        }
    }
    
}

