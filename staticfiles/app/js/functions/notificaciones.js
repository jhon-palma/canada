//setInterval(Notificaciones, 30000000000000000);
setInterval(Notificaciones, 600000);
function Notificaciones(){
  $.ajax({
     type:'GET',
     url: '/getNotifications',
     success: function (data) {
       $.each(data, function(key, value){
          if (value.fields.h_inicio == null || value.fields.h_inicio == '' || value.fields.h_fin == null || value.fields.h_fin == ''){
            if (value.fields.tipo == 'TAREA'){
              mensagesInfo(value.fields.tipo,value.fields.contacto,'','notificacion_tareas');
            }
            if (value.fields.tipo == 'PENDIENTE'){
              mensagesInfo(value.fields.tipo,value.fields.contacto,'','notificacion_pendientes');
            }
            if (value.fields.tipo == 'LLAMADA'){
              mensagesInfo(value.fields.tipo,value.fields.contacto,'','notificacion_llamadas');
            }
          }else{
            if (value.fields.tipo == 'CITA'){
              mensagesInfo(value.fields.tipo+'&nbsp;&nbsp;&nbsp;&nbsp;'+'('+value.fields.h_inicio+" - "+value.fields.h_fin+')',value.fields.contacto,'','notificacion_citas');
            }
            if (value.fields.tipo == 'PROPIEDAD'){
              mensagesInfo(value.fields.tipo+'&nbsp;&nbsp;&nbsp;&nbsp;'+'('+value.fields.h_inicio+" - "+value.fields.h_fin+')',value.fields.contacto,'','notificacion_propiedades');
            }
            if (value.fields.tipo == 'MOSTRADA'){
              mensagesInfo(value.fields.tipo+'&nbsp;&nbsp;&nbsp;&nbsp;'+'('+value.fields.h_inicio+" - "+value.fields.h_fin+')',value.fields.contacto,'','notificacion_mostradas');
            }
          }
       });
     }
  });
}


function mensagesWarning(titulo,campo,texto,duracion){
  var Notify=new PNotify({
	title:titulo,
	text: campo+' '+texto,
	type:"warning",
	addclass: "alert-styled-left",
	delay:duracion,
	animation:"fade",
	mobile:{swipe_dismiss:true,styling:true},
	buttons:{closer:false,sticker:false},
	desktop: {desktop: true,fallback: true},
  });
  Notify.get().click(function() {
      Notify.remove();
  });
}

function mensagesSuccess(titulo,campo,texto){
  var Notify=new PNotify({
	title:titulo,
	text: campo+' '+texto,
	type:"success",
	addclass: "alert-styled-left",
	delay:3000,
	animation:"fade",
	mobile:{swipe_dismiss:true,styling:true},
	buttons:{closer:false,sticker:false},
	desktop: {desktop: true,fallback: true},
  });
  Notify.get().click(function() {
      Notify.remove();
  });
}
function mensagesError(titulo,campo,texto){
  var Notify=new PNotify({
	title:titulo,
	text: campo+' '+texto,
	type:"error",
	addclass: "alert-styled-left",
	delay:3000,
	animation:"fade",
	mobile:{swipe_dismiss:true,styling:true},
	buttons:{closer:false,sticker:false},
	desktop: {desktop: true,fallback: true},
  });
  Notify.get().click(function() {
      Notify.remove();
  });
}

function mensagesInfo(titulo,campo,texto,clase){
  var Notify=new PNotify({
	title:titulo,
  type: "info",
	text: campo+' '+texto,
	addclass: "alert-styled-left",
  cornerclass: clase,
	delay:12000,
  hide: true,
	mobile:{swipe_dismiss:true,styling:true},
	buttons:{closer:false, sticker:false},
	desktop: {desktop: true, fallback: false},
  });
  Notify.get().click(function() {
    Notify.remove();
  });
}
