function trocar_imagens(){
    const imagens = document.querySelectorAll('.flavor_images img');
    if (imagens.length === 0) return;

    const imagem_ativa = Array.from(imagens).findIndex(img => img.classList.contains('ativo'));


    imagens[imagem_ativa].classList.remove('ativo');



    const proxima_imagem = (imagem_ativa + 1) % imagens.length;
    imagens[proxima_imagem].classList.add('ativo');
}

setInterval(trocar_imagens, 4000);