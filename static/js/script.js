$(document).ready(async function () {
    let i = 0;
    const options = await getOptions()
    createRow(i, options)
    $("#btn_add").click(function () {
        i++
        createRow(i, options)
    })

    $("#btn_gen").click(function () {
        let progress = document.createElement("progress")
        let mainForm = document.getElementById("mainForm")
        progress.style = "width: 100%; height: 50px;"
        progress.id = "prog"
        progress.max = 5
        progress.value = 0
        mainForm.appendChild(progress)
        setInterval(function() {
            progress.value += 1
        }, 1000)

        let format = $("#formatResult").val()
        let table_name = $("#table_name").val()
        let count = $("#count").val()
        const mainDivs = $(".main-div")
        let inputData = []
        if (mainDivs !== undefined) {
            mainDivs.each(function () {
                inputData.push({
                    'name': this.childNodes[0].value,
                    'type': this.childNodes[1].value
                })
            })
        }
        let addData = []
        addData.push({
            "format": format,
            "table_name":  table_name,
            "count": count
        })
        let data = []
        data.push({
            "add_data": addData,
            "input_data": inputData
        })
        console.log(JSON.stringify(data))
        sendData(data)
    })

    $("#close-modal, #close_modal_b").click(function () {
        $("#exampleModal").modal("hide")
    })

})

function sendData(data) {
    const xhr = new XMLHttpRequest();
    let modalBody = document.getElementById("modal-body")
    xhr.open("POST", "/generate-sql")
    xhr.onload = () => {
    if (xhr.status === 200) {
        modalBody.innerHTML = ""
        modalBody.append(xhr.responseText)
        $("#exampleModal").modal("show")
        console.log(xhr.responseText);
    } else {
        console.log("Server response: ", xhr.statusText);
    }
};

    xhr.send(JSON.stringify(data));
}

async function getOptions() {
    const response = await fetch("/get-list", {
    method: 'GET', // *GET, POST, PUT, DELETE, etc.
    headers: {
      'Content-Type': 'application/json'
    },
  });
  return await response.json();
}

function createRow(i, options) {
    const row = document.getElementById("row")
    row.append(div(i, options))
    removeSome()
    removeEl()
}

function removeSome() {
    $(".form-select").unbind()
    $(".del-row").unbind()
}

function div(i, options) {
    let div = document.createElement("div")
    div.className = "input-group mb-3 main-div"
    div.id = "row-" + i
    div.appendChild(textInput())
    div.appendChild(select(i, options))
    div.appendChild(btn(i))
    return div
}

function textInput() {
    let textInput = document.createElement("input")
    textInput.type = "text"
    textInput.className = "form-control"
    textInput.ariaLabel = "Text input with dropdown button"
    textInput.placeholder = "Row`s name"
    textInput.name = "Row_name"
    textInput.style = "width: 60%"
    return textInput
}

function removeEl() {
    $(".del-row").each(function () {
        $(this).click(function () {
            $("#"+this.dataset.row).remove()
        })
    })
}

function btn(i) {
    let btn = document.createElement("button")
    btn.className = "btn btn-outline-danger del-row"
    btn.dataset.row = "row-" + i
    btn.append("X")
    return btn
}

function select(i, options) {
    let selectInput = document.createElement("select")
    selectInput.className = "form-select"
    selectInput.id = "sel-" + i
    selectInput.style = "width: 30%"
    selectInput.name = "type"
    for (let i = 0; i < options.length; i++) {
        let option = document.createElement("option")
        option.append(options[i])
        selectInput.appendChild(option)
    }
    return selectInput
}


