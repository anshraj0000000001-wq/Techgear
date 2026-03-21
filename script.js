document.addEventListener("DOMContentLoaded", function() {

  emailjs.init("sscyr-ok-cj__MejU");

  document.getElementById("form").addEventListener("submit", function(e) {
    e.preventDefault();

    emailjs.sendForm("service_pqoh5id", "template_xw0gpwq", this)
      .then(() => alert("massage send successfully thanks to Mail me "))
      .catch(() => alert("Error"));
  });

});