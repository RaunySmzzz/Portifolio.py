import os
import html
from dotenv import load_dotenv
import resend
from flask import Flask, render_template, request, jsonify

# Lê as variáveis do arquivo .env (no seu computador).
# No Render, elas vêm do painel "Environment" e o .env não existe.
load_dotenv()

resend.api_key = os.getenv('RESEND_API_KEY')
EMAIL_DESTINO = os.getenv('EMAIL_DESTINO')

app = Flask(__name__)


@app.route('/')
def home():
    """Renderiza a página principal do portfólio."""
    return render_template('index.html')


@app.route('/enviar-mensagem', methods=['POST'])
def enviar_mensagem():
    """Recebe o formulário de contato e envia por e-mail para você."""
    dados = request.get_json() or {}

    nome = dados.get('name', '').strip()
    email = dados.get('email', '').strip()
    mensagem = dados.get('message', '').strip()

    if not nome or not email or not mensagem:
        return jsonify({'erro': 'Todos os campos são obrigatórios.'}), 400

    if not resend.api_key or not EMAIL_DESTINO:
        print('ERRO: RESEND_API_KEY ou EMAIL_DESTINO não configurados')
        return jsonify({'erro': 'Servidor de e-mail não configurado.'}), 500

    # html.escape evita que alguém injete código HTML no seu e-mail
    corpo = (
        f'<p><strong>Nome:</strong> {html.escape(nome)}</p>'
        f'<p><strong>E-mail:</strong> {html.escape(email)}</p>'
        f'<p><strong>Mensagem:</strong></p>'
        f'<p>{html.escape(mensagem).replace(chr(10), "<br>")}</p>'
    )

    try:
        resend.Emails.send({
            'from': 'Portfólio <onboarding@resend.dev>',
            'to': [EMAIL_DESTINO],
            'reply_to': email,
            'subject': f'Nova mensagem do portfólio - {nome}',
            'html': corpo,
        })
    except Exception as e:
        print(f'Falha ao enviar e-mail: {e}')
        return jsonify({'erro': 'Não foi possível enviar a mensagem agora.'}), 500

    return jsonify({'mensagem': f'Obrigado, {nome}! Sua mensagem foi enviada.'})


if __name__ == '__main__':
    # Só roda no seu computador (python app.py).
    # No Render, quem inicia o site é o gunicorn e este bloco é ignorado.
    from livereload import Server

    server = Server(app.wsgi_app)
    server.watch('templates/*.html')
    server.watch('static/*.css')
    server.watch('static/*.js')
    server.serve(port=5001, debug=True)