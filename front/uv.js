function loadDoc() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
      /*document.getElementById("demo").innerHTML = this.responseText;*/
      console.log(JSON.parse(this.responseText))
      console.log()

      var datos = JSON.parse(this.responseText);
      console.log (datos.uv[0].radiacion_uv)

      var datosradiacionuv = document.getElementById("peticionradiacionluz")
      var redondeo = Math.round(datos.uv[0].radiacion_uv)

      datosradiacionuv.textContent = redondeo;


      }



    xhttp.open("GET", "http://127.0.0.1:8082/listar_datos_sensores", true);
    xhttp.send();
  }

loadDoc()
setInterval(loadDoc, 60000);