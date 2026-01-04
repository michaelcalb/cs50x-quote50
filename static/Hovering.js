const headerProfileIcon = document.querySelector('.header-profile-icon')

headerProfileIcon.addEventListener('mouseover', () => {
    headerProfileIcon.classList.add('bi-person-fill')
    headerProfileIcon.classList.remove('bi-person')
})

headerProfileIcon.addEventListener('mouseout', () => {
    headerProfileIcon.classList.add('bi-person')
    headerProfileIcon.classList.remove('bi-person-fill')
})