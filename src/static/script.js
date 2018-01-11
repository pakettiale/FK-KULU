var numTositteet = 0
var erittelyt = null
var erittelySkeleton = `
    <div id={tosite} class="form-group input-group">
        <div class="input-group-prepend">
            <label class="input-group-text btn btn-outline-secondary"> <span id="{liitePh}"><span class="fa fa-file"></span></span><input type="file" id="{liite}" name="{liite}" hidden/></label>
        </div>
        <input class="form-control" placeholder="Kuvaus" name="{kuvaus}" type="text" />
        <input class="form-control col-sm-1 text-right" placeholder="€" id="{summa}" name="{summa}" type="text" />
        <div class="input-group-append">
            <button id={poista} class="btn btn-warning btn-outline-secondary" type="button"><span class="fa fa-trash-o"></span></button>
        </div>
    </div>`

function AddTositeField() {
    numTositteet += 1
    var elem = $(erittelySkeleton
        .replace(/{tosite}/g, "tosite" + numTositteet)
        .replace(/{kuvaus}/g, "kuvaus" + numTositteet)
        .replace(/{liite}/g, "liite" + numTositteet)
        .replace(/{liitePh}/g, "liitePh" + numTositteet)
        .replace(/{summa}/g, "summa" + numTositteet)
        .replace(/{poista}/g, "poista" + numTositteet)
    )
    erittelyt.append(elem)

    $("#liite" + numTositteet).change(function() {
        var parts = $("#liite" + numTositteet)[0].value.split("\\")
        var fn = parts[parts.length-1]
        $("#liitePh" + numTositteet).text(fn)
    })

    $("#summa" + numTositteet).change(function() {
        var sum = 0
        for(var i = 1; i <= numTositteet; i++) {
            sum += parseFloat($("#summa" + i)[0].value)
        }
        $("#total").text(sum)
    })

    $("#poista" + numTositteet).click(function() {
        $("#tosite" + numTositteet).remove()
        numTositteet -= 1
    })
}

function submit() {

}

$(document).ready(function() {
    erittelyt = $("#erittelyt")

    AddTositeField()

    $("#add").click(AddTositeField)
    $("#submit").click(submit)
})
