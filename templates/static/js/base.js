


const profile = document.getElementById('foto_perfil');
const menu = document.getElementById('menu');
const btnHamburguer = document.getElementById('btnHamburuger');
const menuLateral = document.getElementById('sidebar');

btnHamburguer.addEventListener('click', e => {
    menuLateral.classList.toggle('md:hidden')
})


profile.addEventListener('click', e => {
    menu.classList.toggle('hidden')
})
