document.addEventListener('DOMContentLoaded', function() {
    const documentoField = document.querySelector('#id_documento');
    const planFieldset = document.querySelectorAll('.collapse')[0]; // Plan de Cambios y Mejoras
    const cncFieldset = document.querySelectorAll('.collapse')[1]; // Cédula de No Conformidad

    function toggleFieldsets() {
        const value = parseInt(documentoField.value);
        if (value === 1) {
            planFieldset.style.display = 'none';
            cncFieldset.style.display = 'block';
        } else if (value === 2) {
            planFieldset.style.display = 'block';
            cncFieldset.style.display = 'none';
        } else {
            planFieldset.style.display = 'none';
            cncFieldset.style.display = 'none';
        }
    }

    toggleFieldsets(); // Ejecutar al cargar la página

    documentoField.addEventListener('change', toggleFieldsets); // Ejecutar cuando el valor del campo cambia
});
