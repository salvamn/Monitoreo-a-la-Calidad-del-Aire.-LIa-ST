function loadDoc() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
      /*document.getElementById("demo").innerHTML = this.responseText;*/
      console.log(JSON.parse(this.responseText))
      console.log()



      var datos = JSON.parse(this.responseText);
      console.log (datos.nova[0].pm_dos_punto_cinco)

      var datospmdospuntocinco = document.getElementById("peticionpmdospuntocinco")
      datospmdospuntocinco.textContent = datos.nova[0].pm_dos_punto_cinco;


      var datospmdiez = document.getElementById("peticionpmdiez")
      datospmdiez.textContent = datos.nova[0].pm_diez;
      }



    xhttp.open("GET", "http://127.0.0.1:8082/listar_datos_sensores", true);
    xhttp.send();
  }

loadDoc()
setInterval(loadDoc, 60000);