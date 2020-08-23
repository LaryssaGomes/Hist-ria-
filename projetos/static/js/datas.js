$(document).ready(function() {
  // Setup - add a text input to each footer cell
  
  $('#example thead tr').clone(true).appendTo( '#example thead' );
  $('#example thead tr:eq(1) th').each( function (i) {
      var title = $(this).text();
      if(title!='Imagem'){
         $(this).html( '<input type="text" placeholder="Search '+title+'" />' );

        $( 'input', this ).on( 'keyup change', function () {
            if ( table.column(i).search() !== this.value ) {
                table
                    .column(i)
                    .search( this.value )
                    .draw();
            }
        } ); 
      }
      
  } );

  var table = $('#example').DataTable( {
      orderCellsTop: true,
      fixedHeader: true
      
  } );
} );