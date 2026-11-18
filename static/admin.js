/*
 * Copyright (C) 2026 SJB
 * SPDX-License-Identifier: AGPL-3.0-only
 * See LICENSE for the full licence terms.
 */


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
