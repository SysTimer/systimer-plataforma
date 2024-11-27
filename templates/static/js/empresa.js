function submitForm(element) {
    event.preventDefault(); 
    const form = element.closest('form');
    const empCod = form.querySelector('input[name="emp_cod"]').value;
    const cargoNome = form.querySelector('input[name="cargo_nome"]').value;
    form.submit();
  }
  