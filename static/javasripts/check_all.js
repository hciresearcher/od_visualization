
document.getElementById("selectAllYear1").addEventListener("change", function() {
    var checkboxes = document.querySelectorAll('input[id="cbtest1"]');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = this.checked;
    }
});

document.getElementById("selectAllMonth1").addEventListener("change", function() {
    var checkboxes = document.querySelectorAll('input[id="cbtest2"]');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = this.checked;
    }
});

document.getElementById("selectAllHour1").addEventListener("change", function() {
    var checkboxes = document.querySelectorAll('input[id="cbtest3"]');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = this.checked;
    }
});

document.getElementById("selectAllAge1").addEventListener("change", function() {
    var checkboxes = document.querySelectorAll('input[id="cbtest4"]');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = this.checked;
    }
});

document.getElementById("selectAllYear2").addEventListener("change", function() {
    var checkboxes = document.querySelectorAll('input[id="cbtest5"]');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = this.checked;
    }
});

document.getElementById("selectAllMonth2").addEventListener("change", function() {
    var checkboxes = document.querySelectorAll('input[id="cbtest6"]');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = this.checked;
    }
});

document.getElementById("selectAllHour2").addEventListener("change", function() {
    var checkboxes = document.querySelectorAll('input[id="cbtest7"]');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = this.checked;
    }
});

document.getElementById("selectAllAge2").addEventListener("change", function() {
    var checkboxes = document.querySelectorAll('input[id="cbtest8"]');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = this.checked;
    }
});
