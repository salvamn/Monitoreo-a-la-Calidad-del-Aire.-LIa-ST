function loadDoc() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
      /*document.getElementById("demo").innerHTML = this.responseText;*/
      console.log(JSON.parse(this.responseText))
      console.log()



      var datos = JSON.parse(this.responseText);
      console.log (datos.dht22[0].humedad)

      var datoshumedad = document.getElementById("peticionhumedad")
      datoshumedad.textContent = datos.dht22[0].humedad;


      var datostemperatura = document.getElementById("peticiontemperatura")
      datostemperatura.textContent = datos.dht22[0].temperatura;


      }



    xhttp.open("GET", "http://127.0.0.1:8082/listar_datos_sensores", true);
    xhttp.send();
  }

loadDoc()

setInterval(loadDoc, 60000);