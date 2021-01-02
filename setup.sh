mkdir -p ~/.streamlit/
echo "[general]
email = \"823500+salilathalye@users.noreply.github.com\"
" > ~/.streamlit/credentials.toml
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml