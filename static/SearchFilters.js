const usersButton = document.getElementById("filter-button-users")
const quotesButton = document.getElementById("filter-button-quotes")
const sourcesButton = document.getElementById("filter-button-sources")
const users = document.getElementById("results-users")
const quotes = document.getElementById("results-quotes")
const sources = document.getElementById("results-sources")

function resultsUsers() {
    usersButton.classList.add("filter-selected")
    quotesButton.classList.remove("filter-selected")
    sourcesButton.classList.remove("filter-selected")
    users.classList.remove("invisible")
    quotes.classList.add("invisible")
    sources.classList.add("invisible")
}

function resultsQuotes() {
    usersButton.classList.remove("filter-selected")
    quotesButton.classList.add("filter-selected")
    sourcesButton.classList.remove("filter-selected")
    users.classList.add("invisible")
    quotes.classList.remove("invisible")
    sources.classList.add("invisible")
}

function resultsSources() {
    usersButton.classList.remove("filter-selected")
    quotesButton.classList.remove("filter-selected")
    sourcesButton.classList.add("filter-selected")
    users.classList.add("invisible")
    quotes.classList.add("invisible")
    sources.classList.remove("invisible")
}