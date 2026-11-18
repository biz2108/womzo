
(() => {
  "use strict";

  const notice = document.getElementById("login-countdown");
  const password = document.getElementById("password");
  const button = document.getElementById("login-button");

  if (!notice || !password || !button) return;

  const seconds = Number(notice.dataset.seconds);
  const deadline = Date.now() + seconds * 1000;

  function updateCountdown() {
    const remaining = Math.max(
      0, Math.ceil((deadline - Date.now()) / 1000)
    );

    if (remaining > 0) {
      notice.textContent =
        `Too many login attempts. Please try again in ${remaining} seconds.`;

      button.textContent = `Sign in (${remaining}s)`;

      window.setTimeout(updateCountdown, 250);
    } else {
      notice.classList.remove("error");
      notice.setAttribute("role", "status");
      notice.textContent = "You may now try signing in again.";

      password.disabled = false;
      button.disabled = false;
      button.textContent = "Sign in";
    }
  }

  updateCountdown();
})();
