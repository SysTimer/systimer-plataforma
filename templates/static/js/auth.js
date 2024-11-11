const pesNome = document.getElementById('pes_nome');
const pesSobrenome = document.getElementById('pes_sobrenome');
const empNome = document.getElementById('emp_nome');
const pesEmail = document.getElementById('pes_email');
const pesSenha = document.getElementById('pes_senha');


pesNome.addEventListener('input', e => {
    if (e.target.value) {
        console.log('Entrou');
        e.classList.add('ring-lime-600')

    } else {
        console.log('Removido')
        pesNome.classList.remove("ring-lime-600"); 
        pesNome.classList.add("ring-rose-500");    
    }
});