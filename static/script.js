// Atualiza o ano no rodapé automaticamente
document.getElementById('year').textContent = new Date().getFullYear();

// Rolagem suave para os links do menu
document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const targetId = link.getAttribute('href').substring(1);
    const targetSection = document.getElementById(targetId);
    if (targetSection) {
      targetSection.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// Envio do formulário de contato (exemplo: envia para o backend Flask)
const form = document.getElementById('contact-form');
const feedback = document.getElementById('form-feedback');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const data = {
    name: document.getElementById('name').value,
    email: document.getElementById('email').value,
    message: document.getElementById('message').value
  };

  try {
    const response = await fetch('/enviar-mensagem', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (response.ok) {
      feedback.textContent = result.mensagem || 'Mensagem enviada com sucesso!';
      form.reset();
    } else {
      feedback.textContent = result.erro || 'Erro ao enviar a mensagem.';
    }
  } catch (err) {
    feedback.textContent = 'Não foi possível conectar ao servidor.';
  }
});