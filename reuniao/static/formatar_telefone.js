document.addEventListener("DOMContentLoaded", function() {
    const telefoneInput = document.getElementById("id_celular");

    if (telefoneInput) {
        telefoneInput.addEventListener("input", function(event) {
            let valor = telefoneInput.value.replace(/\D/g, "");
            if (valor.length > 11) {
                valor = valor.slice(0, 11);
            }
            if (valor.length > 2) {
                valor = `(${valor.slice(0, 2)}) ${valor.slice(2, 3)}${valor.slice(3, 7)}-${valor.slice(7, 11)}`;
            }
            telefoneInput.value = valor;
        });
    }
});
