$(document).ready(function(){
  
    var searchBtn =$('#search-btn');//Aqui estou pegando o o button que esta no html
    var searchForm =$('#search-form');//Aqui estou pegando o que foi escrito no form que contem o id search-form

    $(searchBtn).on('click', function(){//quando houver um click no button com id '#search-btn' execute essa ação
     searchForm.submit();//de submeter o escrito para a url
    
    });
   
});