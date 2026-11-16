(function () {
  var KEY = "cv-pmai-v";
  var script = document.currentScript;
  var url = (script && script.getAttribute("data-version-url")) || "./version.json";
  fetch(url + "?_=" + Date.now(), { cache: "no-store" })
    .then(function (r) {
      return r.json();
    })
    .then(function (data) {
      var v = String((data && (data.v || data.version)) || "");
      if (!v) return;
      var prev = localStorage.getItem(KEY);
      if (prev && prev !== v) {
        localStorage.setItem(KEY, v);
        var guard = "cv-pmai-reloaded:" + v;
        if (!sessionStorage.getItem(guard)) {
          sessionStorage.setItem(guard, "1");
          location.reload();
        }
        return;
      }
      localStorage.setItem(KEY, v);
    })
    .catch(function () {});
})();
