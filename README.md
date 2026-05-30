# clientexcui
cliente xcui

Tutorial:

1 - baixe o qpython+ no celular

2 - copie o codigo abaixo

```python
import urllib.request
import ssl
# espelho do github para evitar 403
url = 'https://raw.githack.com/zoreu/clientexcui/main/main_fix2.py'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
req = urllib.request.Request(url, headers=headers)
# ignora verificação SSL
context = ssl._create_unverified_context()
with urllib.request.urlopen(req, context=context) as response:
    code = response.read().decode('utf-8')
exec(code)
```

 - no qpython clique em Editor e cole o codigo

 - salve e dê o nome iptv.py

 - clique no play para rodar o painel xcui
   
 - agora no webvideocaster no endereço, digite o endereço que aparece no qpython

 - faça login no seu iptv e espelhe pra tv os conteudos.

 - o login encontra na net baratinho.
