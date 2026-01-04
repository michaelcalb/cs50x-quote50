document.addEventListener("DOMContentLoaded", () => {
    axios.get("/user-likes-requotes")
    .then((response) => {
        const likedQuoteIds = response.data.likedQuoteIds
        const likeButtons = document.querySelectorAll("[data-quote-id]")
        
        const requotedQuoteIds = response.data.requotedQuoteIds
        const requoteButtons = document.querySelectorAll("[data-quote-id]")

        likeButtons.forEach(button => {
            const quoteId = button.getAttribute("data-quote-id")
            const likeCounters = document.querySelectorAll(`[data-quote-id="${quoteId}"][data-like-button] .quote-button-number`)
            const icons = button.querySelectorAll(`[data-quote-id="${quoteId}"][data-like-button] i`)
            
            if (likedQuoteIds.includes(quoteId)) {
                icons.forEach(icon => {
                    icon.classList.add("bi-heart-fill")
                    icon.classList.remove("bi-heart")
                })
                likeCounters.forEach(counter => {
                    counter.classList.add("num-liked")
                })
            } else {
                likeCounters.forEach(counter => {
                    counter.classList.remove("num-liked")
                })
            }
        });

        requoteButtons.forEach(button => {
            const quoteId = button.getAttribute("data-quote-id")
            const requoteCounters = document.querySelectorAll(`[data-quote-id="${quoteId}"][data-requote-button] .quote-button-number`)
            const icons = button.querySelectorAll(`[data-quote-id="${quoteId}"][data-requote-button] i`)

            if (requotedQuoteIds.includes(quoteId)) {
                icons.forEach(icon => {
                    icon.classList.add("requoted")
                    icon.classList.remove("requote")
                })
                requoteCounters.forEach(counter => {
                    counter.classList.add("num-requoted")
                })
            } else {
                requoteCounters.forEach(counter => {
                    counter.classList.remove("num-requoted")
                })
            }
        })
    })
    .catch( () => {
        window.location.href = "/login";
    })
})

function updateLikes(quoteId) {
    axios.post("/like", { quoteId })
    .then((response) => {
        const likes = response.data.likes
        const likeCounters = document.querySelectorAll(`[data-quote-id="${quoteId}"][data-like-button] .quote-button-number`)
        const icons = document.querySelectorAll(`[data-quote-id="${quoteId}"][data-like-button] i`)
        
        likeCounters.forEach(counter => {
            counter.textContent = likes
        })

        if (icons[0].classList.contains("bi-heart")) {
            icons.forEach(icon => {
                icon.classList.add("bi-heart-fill")
                icon.classList.remove("bi-heart")
            })
            likeCounters.forEach(counter => {
                counter.classList.add("num-liked")
            })
        } else {
            icons.forEach(icon => {
                icon.classList.add("bi-heart")
                icon.classList.remove("bi-heart-fill")
            })
            likeCounters.forEach(counter => {
                counter.classList.remove("num-liked")
            })
        }
    })
    .catch( (error) => {
        console.log(error)
    })
}

function updateRequotes(quoteId) {
    axios.post("/requote", { quoteId })
    .then((response) => {
        const requotes = response.data.requotes
        const requoteCounters = document.querySelectorAll(`[data-quote-id="${quoteId}"][data-requote-button] .quote-button-number`)
        const icons = document.querySelectorAll(`[data-quote-id="${quoteId}"][data-requote-button] i`)

        requoteCounters.forEach(counter => {
            counter.textContent = requotes
        })

        if (icons[0].classList.contains("requoted")) {
            icons.forEach(icon => {
                icon.classList.add("requote")
                icon.classList.remove("requoted")
            })
            requoteCounters.forEach(counter => {
                counter.classList.remove("num-requoted")
            })
        } else {
            icons.forEach(icon => {
                icon.classList.add("requoted")
                icon.classList.remove("requote")
            })
            requoteCounters.forEach(counter => {
                counter.classList.add("num-requoted")
            })
        }
    })
    .catch( (error) => {
        console.log(error)
    })
}