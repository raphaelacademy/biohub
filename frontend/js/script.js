const botaoMenu =
    document.getElementById('menu-hamburger');
const menuLinks =
    document.getElementById('menu-links');

    botaoMenu.addEventListener('click', () => {
const menuAberto =
    menuLinks.classList.toggle('aberto');

    botaoMenu.setAttribute('aria-expanded', menuAberto);
    botaoMenu.setAttribute('aria-label', menuAberto ? 'Fechar menu' : 'Abrir menu');
    botaoMenu.textContent = menuAberto ? '✖' : '☰';
});