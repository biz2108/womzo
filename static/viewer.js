/*
 * Copyright (C) 2026 SJB
 * SPDX-License-Identifier: AGPL-3.0-only
 * See LICENSE for the full licence terms.
 */

(() => {
  "use strict";
  const cameras = JSON.parse(document.getElementById("camera-data").textContent);
  const byId = new Map(cameras.map((camera) => [String(camera.id), camera]));
  const shell = document.getElementById("video-shell");
  const title = document.getElementById("now-title");
  const location = document.getElementById("now-location");
  const source = document.getElementById("source-link");
  const note = document.getElementById("player-note");
  const search = document.getElementById("search");
  const buttons = [...document.querySelectorAll(".camera-item")];
  const noMatch = document.getElementById("no-match");
  let hls = null;
  function clearPlayer() {
    if (hls) { hls.destroy(); hls = null; }
    shell.replaceChildren();
  }
  function message(value) {
    const item = document.createElement("div");
    item.className = "player-placeholder";
    item.textContent = value;
    shell.appendChild(item);
  }
  function play(camera, updateAddress = true) {
    clearPlayer();
    buttons.forEach((button) => button.classList.toggle("active", button.dataset.id === String(camera.id)));
    title.textContent = camera.title;
    location.textContent = camera.location;
    source.href = camera.url;
    source.hidden = false;
    note.textContent = "Video is delivered directly by its original provider, not through this server.";
    if (camera.kind === "youtube" && camera.youtube_id) {
      const iframe = document.createElement("iframe");
      iframe.title = camera.title;
      iframe.src = `https://www.youtube-nocookie.com/embed/${encodeURIComponent(camera.youtube_id)}?autoplay=1&playsinline=1&rel=0`;
      iframe.allow = "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; web-share; fullscreen";
      iframe.allowFullscreen = true;
      iframe.referrerPolicy = "strict-origin-when-cross-origin";
      shell.appendChild(iframe);
    } else if (camera.kind === "ipcamlive") {
      const iframe = document.createElement("iframe");
      iframe.title = camera.title;
      iframe.src = camera.url;
      iframe.allow = "autoplay; fullscreen; picture-in-picture";
      iframe.allowFullscreen = true;
      iframe.referrerPolicy = "strict-origin-when-cross-origin";
      shell.appendChild(iframe);
      note.textContent = "This player is embedded from IPCamLive. If the camera owner restricts embedding, use Original source.";
    } else if (camera.kind === "myearthcam") {
      const iframe = document.createElement("iframe");
      iframe.title = camera.title;
      iframe.src = camera.url;
      iframe.allow = "autoplay; fullscreen; picture-in-picture";
      iframe.allowFullscreen = true;
      iframe.referrerPolicy = "strict-origin-when-cross-origin";
      shell.appendChild(iframe);
      note.textContent = "Embedded MyEarthCam player. If the provider limits use on other websites, select Original source.";
    } else if (camera.kind === "hls") {
      const video = document.createElement("video");
      video.controls = true;
      video.autoplay = true;
      video.playsInline = true;
      shell.appendChild(video);
      if (video.canPlayType("application/vnd.apple.mpegurl")) {
        video.src = camera.url;
        video.play().catch(() => {});
      } else if (window.Hls && window.Hls.isSupported()) {
        hls = new window.Hls();
        hls.loadSource(camera.url);
        hls.attachMedia(video);
        hls.on(window.Hls.Events.ERROR, (_, data) => {
          if (data.fatal) note.textContent = "The stream could not be played here (possibly CORS or an unavailable stream). Try Original source.";
        });
      } else {
        note.textContent = "This browser cannot play HLS streams. Try Original source.";
      }
    } else if (camera.kind === "image") {
      const img = document.createElement("img");
      img.className = "camera-image";
      img.src = camera.url;
      img.alt = camera.title;
      shell.appendChild(img);
      note.textContent = "This camera provides an image, which may not refresh automatically. Open Original source for updates.";
    } else {
      message("This webcam is available on its original website. Select Original source above to open it.");
      note.textContent = "The source is a webpage, not a directly embeddable video link.";
    }
    if (updateAddress) {
      const next = new URL(window.location.href);
      next.searchParams.set("camera", camera.id);
      history.replaceState(null, "", next);
    }
  }
  buttons.forEach((button) => button.addEventListener("click", () => play(byId.get(button.dataset.id))));
  search.addEventListener("input", () => {
    const needle = search.value.trim().toLocaleLowerCase();
    let matches = 0;
    buttons.forEach((button) => {
      const show = button.dataset.search.includes(needle);
      button.hidden = !show;
      if (show) matches += 1;
    });
    noMatch.hidden = matches !== 0 || buttons.length === 0;
  });
  const preselected = new URL(window.location.href).searchParams.get("camera");
  if (preselected && byId.has(preselected)) play(byId.get(preselected), false);
})();
