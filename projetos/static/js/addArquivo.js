esconde()
function esconde(){
    document.getElementById('F').style.display="none";
    document.getElementById('V').style.display="none";
    document.getElementById('D').style.display="none";
    document.getElementById('A').style.display="none";
    document.getElementById('uploadV').style.display="none";
    document.getElementById('uploadA').style.display="none";
    document.getElementById('uploadF').style.display="none";
    document.getElementById('uploadD').style.display="none";
}

function esconderElementos(tipoSelecionado){
    var lista = ["V","D", "F", "A"];
    var listaUpload = ['uploadV','uploadD','uploadF','uploadA']
    for(i=0;i<lista.length;i++){
        if(tipoSelecionado!=lista[i]){
            document.getElementById(lista[i]).style.display="none";
            document.getElementById(listaUpload[i]).style.display="none";
            
        }
    }
}
function tiposDeDocumento(){
    
    tipo = document.getElementById('id_arq_tipo_de_formato');
    tipoSelecionado = tipo.value
    if(tipoSelecionado == 'nada'){
        esconde()
        document.getElementById('nada').style.display="";

    }else if(tipoSelecionado=='Video' ){
    
        document.getElementById('nada').style.display="none";
        document.getElementById('V').style.display="";
        document.getElementById('uploadV').style.display="";
        esconderElementos('V');
    }else if(tipoSelecionado=='Audio' ){
        document.getElementById('nada').style.display="none";
        document.getElementById('A').style.display="";
        document.getElementById('uploadA').style.display="";
        esconderElementos('A');
    }else if(tipoSelecionado=='Fotografia'||tipo.value=='Mapa' || tipo.value=='Pintura' || tipo.value=='Gravura' ){
        esconderElementos('F');
        document.getElementById('nada').style.display="none";
        document.getElementById('F').style.display="";
        document.getElementById('uploadF').style.display="";
        
    }else if(tipoSelecionado=='Impresso' || tipo.value=='Manuscrito' ){
        
        document.getElementById('nada').style.display="none";
        document.getElementById('D').style.display="";
        document.getElementById('uploadD').style.display="";
        esconderElementos('D');
    }else{
        document.getElementById('nada').style.display="none";
        esconde()
        
    }
}




// Adicionar restrição nos input type files
document.getElementById('id_vid_video').accept="video/*";
document.getElementById('id_aud_audio').accept="audio/* ";
document.getElementById('id_doc_documento').accept="application/pdf";

// Populando o select dia
var select = document.getElementById("dia");
for(a=1;a<32;a++){
    if(a<10){
        select.options[select.options.length] = new Option("0"+a, "0"+a);
    }else{
        select.options[select.options.length] = new Option(a, a);
    }
}

// Populando o select ano
var selectAno = document.getElementById("ano");

function anoMaximo(){
    var data = new Date();
    var ano = data.getFullYear();
    ano = ano+1;
    return ano;
}
// Tipo espeficos
document.getElementById('espeficos').style.display="none";

function esconderEspeficos(){
    var myOpts = document.getElementById('generico').options;
    for (x=1;x<myOpts.length;x++){
        var aux = myOpts[x].value
        document.getElementById(aux).style.display="none";
}
}
esconderEspeficos();
function tipoGenerico(){
    var tipo = document.getElementById('generico')
    if(tipo){
        if(tipo.value=='vazio'){
                document.getElementById('espeficos').style.display="none";
        }else{
            document.getElementById('espeficos').style.display=""; 
            document.getElementById(tipo.value).style.display=""; 
            var myOpts = document.getElementById('generico').options;
            for (x=1;x<myOpts.length;x++){
                var aux = myOpts[x].value
                if(aux!=tipo.value){
                    document.getElementById(aux).style.display="none";
                }
                
            }
        } 
    }
}
