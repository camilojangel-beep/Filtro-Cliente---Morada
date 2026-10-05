// Ejemplo de static/experian_demo.local.js (copie este archivo con ese nombre
// y reemplace el registro ficticio por las personas de la base de Experian).
//
// `nombre`, `score`, `obligaciones` (vigentes + cerradas) y `vigentes` vienen
// de HDC+; `aportantes` y `cotizante`, de Valor Ingreso. `apellido` es el
// primer apellido con el que HDC+ acepta la consulta. `nombre_vi` es opcional:
// va cuando Valor Ingreso devuelve otro nombre de pila para la misma cédula.
// Antes de agregar a alguien, verifique que responda los dos informes.
window.EXPERIAN_DEMO_LOCAL = [
    { nombre: "Juan Prueba Demo", cedula: "1000000001", apellido: "PRUEBA", tipo: "CC", score: 750, obligaciones: 12, vigentes: 4, aportantes: 1, cotizante: "Empleado" },
];
