let button = $("#mpc-load-more")
const errorMessage = $("#mpc-error-message")
const loadingInit = $("#mpc-loading-init")
const container = $("#mpc-company-collection-container")
const path = "most-popular-companies"
const buttonText = button.html()

$(document).ready(function () {
    let offset = 1
    let range = 10

    button.click(() => {
        onButtonClick(offset, range).then(() => offset += range).catch(() => errorMessage.show())
    })
    initialize(offset, range).then(() =>
        offset += range
    ).catch(() =>
        errorMessage.show()
    ).finally(() =>
        loadingInit.hide()
    )
})

async function initialize(offset, range) {
    button.hide()
    loadingInit.show()
    return await $.get(`${path}?limit=${range}&offset=${offset}`, async data => {
        container.append(data)
    }).always(() => button.show()).done(() => errorMessage.hide())
}

async function onButtonClick(offset, range) {
    button.attr("disabled", true)
    button.html("<div class='loader'></div>")
    return await $.get(`${path}?limit=${range}&offset=${offset}`, (data, textStatus, request) => {
        container.append(data)
        if (request.getResponseHeader('end-reached') === "False") button.attr("disabled", false)
        else button.css("display", "none")
    }).fail(() => {
        button.attr("disabled", false)
    }).always(() => {
        button.html(buttonText)
    }).done(() => errorMessage.hide())
}
