
(() => {
  "use strict";

  const deleteForms = document.querySelectorAll(".delete-camera-form");

  deleteForms.forEach((form) => {
    form.addEventListener("submit", (event) => {
      const confirmed = window.confirm("Remove this camera?");

      if (!confirmed) {
        event.preventDefault();
      }
    });
  });
})();
