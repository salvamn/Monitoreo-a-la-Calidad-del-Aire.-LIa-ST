function copiarTexto(id){
    var texto = document.getElementById(id)
    // texto.select()
    // texto.setSelectionRange(0, 99999)
    navigator.clipboard.writeText(texto.innerText)
}