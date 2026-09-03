(() => {
  if ("serviceWorker" in navigator) {
    let refreshing = false;

    navigator.serviceWorker.addEventListener("controllerchange", () => {
      if (refreshing) return;
      refreshing = true;
      window.location.reload();
    });

    window.addEventListener("load", () => {
      navigator.serviceWorker
        .register("./service-worker.js", { updateViaCache: "none" })
        .then(registration => registration.update())
        .catch(() => {});
    });
  }

  let deferredPrompt = null;
  let installButton = null;

  function removeButton() {
    if (installButton) installButton.remove();
    installButton = null;
  }

  function showInstallButton() {
    if (installButton || window.matchMedia("(display-mode: standalone)").matches) return;
    installButton = document.createElement("button");
    installButton.type = "button";
    installButton.textContent = "Instalar app";
    installButton.setAttribute("aria-label", "Instalar Calculadora como aplicativo");
    Object.assign(installButton.style, {
      position: "fixed",
      right: "12px",
      bottom: "calc(12px + env(safe-area-inset-bottom))",
      zIndex: "9999",
      border: "0",
      borderRadius: "999px",
      padding: "10px 14px",
      background: "#a51016",
      color: "#fff",
      font: "800 12px system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif",
      boxShadow: "0 8px 24px rgba(16,24,40,.22)"
    });
    installButton.addEventListener("click", async () => {
      if (!deferredPrompt) return;
      deferredPrompt.prompt();
      await deferredPrompt.userChoice.catch(() => null);
      deferredPrompt = null;
      removeButton();
    });
    document.body.appendChild(installButton);
  }

  window.addEventListener("beforeinstallprompt", event => {
    event.preventDefault();
    deferredPrompt = event;
    showInstallButton();
  });

  window.addEventListener("appinstalled", () => {
    deferredPrompt = null;
    removeButton();
  });
})();
