mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"823500+salilathalye@users.noreply.github.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml