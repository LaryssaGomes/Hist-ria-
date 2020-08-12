esconderElementos();
document.getElementById('texto').style.display="none";
function esconderElementos(){
    document.getElementById('A').style.display="none";
    document.getElementById('V').style.display="none";
    document.getElementById('F').style.display="none";
    document.getElementById('D').style.display="none";
    document.getElementById('T').style.display="none";
}
function update() {
    var select = document.getElementById('id_arq_tipo_de_formato');
    var option = select.options[select.selectedIndex];
    var elementosDiv = {0: "V", 1: "D", 2: "F", 3:"A"};
    if (option.value == ''){
        document.getElementById('nada').style.display="";
        esconderElementos();
    }else{
        for (var cont = 0; cont in elementosDiv; cont++){
            if (option.value == elementosDiv[cont]){
                esconderTexto();
                radio = document.getElementById('1')
                radio2 = document.getElementById('0')
                radio.checked = false
                radio2.checked = false
                document.getElementById(option.value).style.display="";
                document.getElementById('nada').style.display="none";

                if(option.value == 'F'){
                    document.getElementById('T').style.display="none";
                }else{
                    document.getElementById('T').style.display="";
                }
                for (var cont0 = 0; cont in elementosDiv; cont0++){
                    if(elementosDiv[cont]!=elementosDiv[cont0]){
                        document.getElementById(elementosDiv[cont0]).style.display="none";
                    }
                }
            }
    
        }
    }

   
       
        
}

update();
// Restrição de mostrar elementos Transcrição
function mostrarTexto(){
    document.getElementById('texto').style.display="";
}
function esconderTexto(){
    document.getElementById('texto').style.display="none";
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
document.getElementById('espeficos').style.display="none";

function esconderEspeficos(){
    var myOpts = document.getElementById('generico').options;
    for (x=1;x<myOpts.length;x++){
        var aux = myOpts[x].value
        document.getElementById(aux).style.display="none";
}
}
esconderEspeficos();
function tipo(){
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
