const VALIDATE_COORS = /^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$/

var coors = document.getElementById("geo-coors");
var errors = document.getElementById("errors");
var submit = document.getElementById("submit");

coors.addEventListener('input', function() {
  if (VALIDATE_COORS.test(coors.value)) {
    errors.innerHTML = "";

    submit.removeAttribute("disabled");
  } else {
    errors.innerHTML = "invalid coordinates, should be of format 40.714224,-73.961452";
    submit.addAttribute("disabled", "disabled");
  }
});
