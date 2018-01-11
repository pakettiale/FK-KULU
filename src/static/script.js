var erittelyt = null
var erittelySkeleton = `
    <div id={tosite} class="form-group input-group">
        <div class="input-group-prepend">
            <label class="input-group-text btn btn-outline-secondary"> <span id="{liitePh}"><span class="fa fa-file"></span></span><input type="file" id="{liite}" name="{liite}" hidden/></label>
        </div>
        <input class="form-control" placeholder="Kuvaus" id="{kuvaus}" name="{kuvaus}" type="text" />
        <input class="form-control col-sm-1 text-right" placeholder="€" id="{summa}" name="{summa}" type="text" />
        <div class="input-group-append">
            <button id={poista} class="btn btn-warning btn-outline-secondary" type="button"><span class="fa fa-trash-o"></span></button>
        </div>
    </div>`

function setValidation(sel, isValid) {
    if(isValid) {
        $(sel).addClass('is-valid')
        $(sel).removeClass('is-invalid')
    }else{
        $(sel).addClass('is-invalid')
        $(sel).removeClass('is-valid')
    }
}

function validateIBAN() {
    var iban = $("#iban")[0].value
    setValidation("#iban", IBAN.isValid(iban))
}

function validateNotEmpty(sel) {
    return function() {
        var val = $(sel)[0].value
        setValidation(sel, val.length != 0)
    }
}

function AddTositeField() {
    var id = Math.floor((1+Math.random()) * 1e6)
    var elem = $(erittelySkeleton
        .replace(/{tosite}/g, id)
        .replace(/{kuvaus}/g, "kuvaus" + id)
        .replace(/{liite}/g, "liite" + id)
        .replace(/{liitePh}/g, "liitePh" + id)
        .replace(/{summa}/g, "summa" + id)
        .replace(/{poista}/g, "poista" + id)
    )
    erittelyt.append(elem)

    $("#liite" + id).change(function() {
        var parts = $("#liite" + id)[0].value.split("\\")
        var fn = parts[parts.length-1]
        $("#liitePh" + id).text(fn)
    })

    $("#summa" + id).on('input', function() {
        var sum = 0
        $("[id^=summa]").each(function() {
            var s = $(this)[0].value.replace(',', '.').replace('€', '')
            sum += parseFloat(parseFloat(s) ? s : '0')
        })
        $("#total").text(sum)
    })

    $("#poista" + id).click(function() {
        $("#" + id).remove()

        if(erittelyt)
    })

    // Validations

    $("#summa" + id).on('input', function(){
        var s = $("#summa" + id)[0].value.replace(',', '.').replace('€', '')
        console.log(s);
        setValidation("#summa" + id, s.length != 0 && parseFloat(s))
    })
    $("#kuvaus" + id).on('input', validateNotEmpty("#kuvaus" + id))
}

function submit() {
}

$(document).ready(function() {
    erittelyt = $("#erittelyt")

    AddTositeField()

    $("#add").click(AddTositeField)
    $("#submit").click(submit)
    $("#iban").on('input', validateIBAN)
    $("#nimi").on('input', validateNotEmpty("#nimi"))
    $("#peruste").on('input', validateNotEmpty("#peruste"))
})
