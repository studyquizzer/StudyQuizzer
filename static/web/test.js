function foo() {
    var e = window.getSelection(),
        n = e.toString();

    fetch(`https://owlbot.info/api/v4/dictionary/${n}`, {
        headers: {
            'Authorization': 'Token a5ab3dc468825ff3a1ac3dfac049ed05ef3f246f'
        },
    }).then(e => e.json()).then(e => fine(e, n))
}

function fine(e, n) {
    let t = "";
    for (var i in e.definitions) {
        t = i;
        break
    }
    let definition = e["definitions"][0]["definition"];

    let modal = document.getElementById("definitionModalLabel");
    let define = document.getElementById("define"); 

    modal.textContent = n;
    define.textContent = definition;

    $("#definitionModal").modal("show")
}