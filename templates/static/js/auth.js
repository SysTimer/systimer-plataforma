const pesNome = document.getElementById("pes_nome");
const pesSobrenome = document.getElementById("pes_sobrenome");
const empNome = document.getElementById("emp_nome");
const pesEmail = document.getElementById("pes_email");
const pesSenha = document.getElementById("pes_senha");

// Recuperar Senha
const newPwd = document.getElementById("senha");
const newPwdConfirm = document.getElementById("password_novaSenha");

const modal = document.getElementById('myModal');
const openModalButton = document.getElementById('forgot-password-link');
const closeModalButton = document.getElementById('cancel-button');
const form = document.getElementById('recuperar-form');
const message = document.getElementById('message');


openModalButton.addEventListener('click', function(e) {
  e.preventDefault(); 
  modal.classList.remove('hidden');
});

closeModalButton.addEventListener('click', function() {
  modal.classList.add('hidden');  // Oculta o modal
});

form.addEventListener('submit', function(e) {
  e.preventDefault(); 
  message.classList.remove('hidden');
  modal.classList.add('hidden');
});


newPwdConfirm.addEventListener("change", function (e) {
  const div = document.getElementById("senhaErr");
  let span = document.createElement("span");

  if (newPwd.value !== newPwdConfirm.value) {
    console.log('Entrou')
    span.style.color = "Red";
    span.textContent = "As senhas não coincidem";
    div.appendChild(span)
  } else {
    div.remove(span)
  }
});
