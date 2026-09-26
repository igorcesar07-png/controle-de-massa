# Controle de massa — pavimentação

Aplicativo HTML para apontamento de trechos e comparação entre massa usinada e aplicada.

## Recursos

- Edição de dimensões em metros: comprimento com passo de 1 m, largura de 0,01 m e espessura de 0,001 m.
- Cálculo automático da estaca final conforme comprimento e sentido.
- Panos sequenciais vinculados à estaca final do pano anterior.
- Volume, massa aplicada, saldo e diferença percentual calculados automaticamente.
- Salvar e reabrir apontamentos em JSON e imprimir relatórios.

## Uso

Abra `index.html` no navegador. Não exige instalação ou compilação.

Os dados iniciais são exemplos. Os apontamentos devem ser salvos em arquivo; esta versão não possui banco de dados nem sincronização entre usuários.

## Publicação

O arquivo `index.html` pode ser hospedado como site estático no Netlify ou GitHub Pages.

## Cálculos

Volume = comprimento × largura × espessura.

Massa aplicada = volume × densidade (t/m³).

Saldo = massa usinada − massa aplicada.

Diferença percentual = saldo ÷ massa usinada × 100, quando a massa usinada é maior que zero.
