function DirecionMaps(latitud,longitud,campo_latitud,campo_longitud,campo_direccion,bandera_mapa,campo_foto){
    $("#container_mapa").append(
      '<div id="modal_mapa" class="modal fade" style="z-index: 1051;">'+
          '<div class="modal-dialog">'+
              '<div class="modal-content">'+
                  '<div class="modal-header bg-indigo-700">'+
                      '<button type="button" class="close" data-dismiss="modal">×</button>'+
                      '<h6 id="title_mostradas" class="modal-title"><span><i class="icon-location4"></i></span> SELECCIONA UNA UBICACIÓN</h6>'+
                  '</div>'+
                  '<div class="form-horizontal">'+
                    '<div class="modal-body">'+
                        '<div class="form-group">'+
                            '<div class="col-lg-12">'+
                              '<div class="row">'+
                                '<div class="col-md-8"><input id="pac-input" class="controls" type="text" placeholder="Busca una direción..."></div>'+
                                '<div class="col-md-4"><a href="javascript:void(0)" onclick="limpiarDireccion()" type="button" data-dismiss="modal" class="btn bg-indigo-700 btn-labeled btn-xlg"><b><i class="icon-location4"></i></b>ASIGNAR</a></div>'+
                              '</div>'+
                            '</div>'+
                        '</div>'+
                        '<div class="form-group">'+
                          '<div class="row">'+
                            '<div class="col-md-12">'+
                              '<div id="map_canvas"></div>'+
                            '</div>'+
                          '</div>'+
                        '</div>'+
                    '</div>'+
                  '</div>'+
              '</div>'+
          '</div>'+
      '</div>'
    )
    $('#modal_mapa').modal({
    }).on('shown.bs.modal', function () {
      var map_options = {
          center: new google.maps.LatLng(latitud, longitud),
          zoom: 17,
          mapTypeId: google.maps.MapTypeId.ROADMAP
      };
      var map = new google.maps.Map(document.getElementById("map_canvas"), map_options);
      var defaultBounds = new google.maps.LatLngBounds(
          new google.maps.LatLng(-6, 106.6),
          new google.maps.LatLng(-6.3, 107)
      );
      var input = document.getElementById("pac-input");
      var autocomplete = new google.maps.places.Autocomplete(input);
      autocomplete.bindTo("bounds", map);
      var marker = new google.maps.Marker({
        position: new google.maps.LatLng(latitud, longitud),
        map: map
      });
      google.maps.event.addListener(autocomplete, "place_changed", function()
      {
          var place = autocomplete.getPlace();
          if (place.geometry.viewport) {
              map.fitBounds(place.geometry.viewport);
          } else {
              map.setCenter(place.geometry.location);
              map.setZoom(17);
          }
          // GUARDO LAS COORDENADAS EN EL CAMPO DIRECCION ID
          marker.setPosition(place.geometry.location);
          $('#'+campo_direccion).val($("#pac-input").val())
          $('#'+campo_latitud).val(place.geometry.location.lat)
          $('#'+campo_longitud).val(place.geometry.location.lng)
          $('#'+campo_foto).attr("src","https://maps.googleapis.com/maps/api/staticmap?center="+$('#'+campo_latitud).val()+","+$('#'+campo_longitud).val()+"+&zoom=15&size=200x200&scale=4&markers="+$('#'+campo_latitud).val()+","+$('#'+campo_longitud).val()+"&key=AIzaSyAgtggm5fEK2oiyx7BMCaUTiFlCJIpNSk8");
      });
      google.maps.event.addListener(map, "click", function(event)
      {
          $('#'+bandera_mapa).val(event.latLng)
          var coordenadas = $('#'+bandera_mapa).val().replace("(", "").replace(")", "").split(",");
          $('#'+campo_latitud).val(coordenadas[0])
          $('#'+campo_longitud).val(coordenadas[1])
          marker.setPosition(event.latLng);
          $('#'+campo_foto).attr("src","https://maps.googleapis.com/maps/api/staticmap?center="+$('#'+campo_latitud).val()+","+$('#'+campo_longitud).val()+"+&zoom=15&size=200x200&scale=4&markers="+$('#'+campo_latitud).val()+","+$('#'+campo_longitud).val()+"&key=AIzaSyAgtggm5fEK2oiyx7BMCaUTiFlCJIpNSk8");
      });
    });
}


function limpiarDireccion(){
    $('#pac-input').val('')
}

function limpiarSelects(params) {
  for (i=0; i<params.length; i++) {
      if ($('#'+params[i]).find("option:first-child").val() == ""){
        $('#'+params[i]).children('option:not(:first)').remove();
        $('#'+params[i]).select2().select2('val',"");
      }else{
        $('#'+params[i]).empty().trigger('change')
      }
  }
}


function countries(campoPais,campoDep,campoPro,campoDis,campoUr){
    if ($("#"+campoPais).val() !="" || $("#"+campoPais).val() != null){
        traerDepartamentos($("#"+campoPais).val(),campoDep,campoPro,campoDis,campoUr);
    }else{
      list = [campoDep,campoPro,campoDis,campoUr]
      limpiarSelects(list);
  }
}

function departaments(campoDep,campoPro,campoDis,campoUr) {
  if ($("#"+campoDep).val() !=""){
     traerProvincias($("#"+campoDep).val(),campoPro,campoDis,campoUr);
  }else{
    list = [campoPro,campoDis,campoUr]
    limpiarSelects(list);
  }
}

function provinces(campoPro,campoDis,campoUr) {
    if ($("#"+campoPro ).val() !=""){
        traerDistritos($("#"+campoPro).val(),campoDis,campoUr);
    }else{
      list = [campoDis,campoUr]
      limpiarSelects(list);
    }
}

function districts(campoDis,campoUr) {
    if ($("#"+campoDis ).val() !=""){
        traerUrbanizaciones($("#"+campoDis).val(),campoUr);
    }else{
      list = [campoUr]
      limpiarSelects(list);
    }
}

function traerDepartamentos(pais,campoDep,campoPro,campoDis,campoUr,departamento) {
    list = [campoDep,campoPro,campoDis,campoUr]
    limpiarSelects(list);
    if (pais != ""){
      $.ajax({
          url: '/departaments?country='+pais,
          type: 'GET',
          success: function(data) {
              for (var i = 0; i < data.length; i++) {
                  $("#"+campoDep).append("<option value='" + data[i].pk + "'>" + data[i].fields.name + "</option>");
              }
              $("#"+campoDep+">option[value="+departamento+"]").attr("selected", "selected");
          }
      });
    }
}

function traerProvincias(departamento,campoPro,campoDis,campoUr,provincia) {
    list = [campoPro,campoDis,campoUr]
    limpiarSelects(list);
    if (departamento != ""){
      $.ajax({
          url: '/provinces?departament='+departamento,
          type: 'GET',
          success: function(data) {
              for (var i = 0; i < data.length; i++) {
                  $("#"+campoPro).append("<option value='" + data[i].pk + "'>" + data[i].fields.name + "</option>");
              }
              $("#"+campoPro+">option[value="+provincia+"]").attr("selected", "selected");
          }
      });
    }
}

function traerDistritos(provincia,campoDis,campoUr,distrito) {
    list = [campoDis,campoUr]
    limpiarSelects(list);
    if (provincia != ""){
      $.ajax({
          url: '/districts?province='+provincia,
          type: 'GET',
          success: function(data) {
              for (var i = 0; i < data.length; i++) {
                  $("#"+campoDis).append("<option value='" + data[i].pk + "'>" + data[i].fields.name + "</option>");
              }
              $("#"+campoDis+">option[value="+distrito+"]").attr("selected", "selected");
          }
      });
    }
}


function traerUrbanizaciones(distrito,campoUr,urbanizacion) {
    list = [campoUr]
    limpiarSelects(list);
    if (distrito != ""){
      $.ajax({
          url: '/urbanizations?district='+distrito,
          type: 'GET',
          success: function(data) {
              for (var i = 0; i < data.length; i++) {
                  $("#"+campoUr).append("<option value='" + data[i].pk + "'>" + data[i].fields.name + "</option>");
              }
          }
      });
    }
}
