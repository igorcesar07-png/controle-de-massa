# Controle de massa — fresagem, RDO e aplicação

Aplicativo web (um único `index.html`, sem instalação) para controlar a fresagem, o RDO da aplicação e o consumo de CBUQ em campo. Pensado para uso no celular.

## Painéis

1. **Controle de fresagem** — cadastro dos segmentos fresados (estaca inicial, sentido, comprimento, faixa, largura, espessura). A estaca final é calculada; “Sequencial” encadeia com o segmento anterior. Mostra a massa de CBUQ equivalente ao volume fresado (volume × densidade) e um resumo com o total de massa “fresada”.
2. **RDO da aplicação** — recebe automaticamente todos os segmentos da fresagem. Os valores podem ser editados sem alterar a fresagem; quando ficam diferentes, o valor original da fresagem aparece discretamente em roxo abaixo do campo. Cada segmento pode ser marcado como **Concluído**, ter observação e ser restaurado (↺).
3. **Acompanhamento da aplicação** — massa recebida da usina (com botão “+1 caminhão”), massa já aplicada (segmentos concluídos), restante, necessário para os pendentes e o saldo:
   - **Falta** → alerta vermelho “acionar a usina imediatamente” com toneladas e número de caminhões, e botão para copiar/compartilhar o pedido.
   - **Sobra** → quanto ainda precisa fresar, em toneladas e em metros, para a largura e espessura informadas.

Um aviso fixo no topo mostra a situação em todos os painéis.

## Dados

- Salvos automaticamente no próprio aparelho (navegador).
- Menu ⋯: salvar/abrir arquivo `.json` (compatível com arquivos da versão anterior), imprimir relatório, novo apontamento.

## Cálculos

- Massa do segmento = comprimento × largura × espessura × densidade.
- Aplicada = Σ massa RDO dos concluídos · Necessário = Σ massa RDO dos pendentes.
- Saldo = (recebida − aplicada) − necessário. Negativo = falta; positivo = sobra.
- Metros a fresar = sobra ÷ (densidade × largura × espessura).
- Caminhões = arredondar para cima (falta ÷ carga por caminhão).
