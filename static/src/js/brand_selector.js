document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    const params = new URLSearchParams(window.location.search);
    console.log("Ruta actual:", path);
    console.log("Parámetros URL:", window.location.search);
    console.log("Valor de success:", params.get('success'));
  
    const formSection = document.getElementById('form-section');
    const thankYouMessage = document.getElementById('thank-you-message');
  
    if (path === '/thank-you' || params.get('success') === '1') {
      console.log("Condición para mostrar mensaje de gracias cumplida.");
      if (formSection) {
        formSection.style.display = 'none';
        console.log("Formulario ocultado.");
      }
      if (thankYouMessage) {
        thankYouMessage.style.display = 'block';
        console.log("Mensaje de gracias mostrado.");
      }
  
      const newRequestBtn = document.getElementById('new-request');
      if (newRequestBtn) {
        newRequestBtn.addEventListener('click', () => {
          console.log("Botón nueva cotización clickeado.");
          window.location.href = '/marca';
        });
      }
    } else {
      console.log("No es ruta de thanks o success.");
    }
  });
  