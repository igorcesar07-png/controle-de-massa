# Controle de massa — fresagem, RDO e aplicação

Aplicativo web (um único `index.html`, sem instalação) para controlar a fresagem, o RDO da aplicação e o consumo de CBUQ em campo. Pensado para uso no celular.

## Painéis

1. **Controle de fresagem** — densidade e **massa total usinada do dia**. A tela mostra só o **resumo dos segmentos**, cada um com **Editar** e **Excluir** (com confirmação). O formulário (estaca inicial, sentido, comprimento, faixa, largura, espessura, sequencial) abre só ao editar ou adicionar; ao salvar, volta ao resumo atualizado. Total de massa "fresada" = volume × densidade.
2. **RDO da aplicação** — recebe automaticamente os segmentos da fresagem e permite editar o que foi aplicado sem alterar a fresagem.
   - Quadro **usinado × aplicado no RDO** (t e m³) com a diferença (usinado − aplicado).
   - Lista de **diferenças RDO × fresagem**: valor da fresagem, valor do RDO e diferença com sinal (▲ + a mais, azul · ▼ − a menos, vermelho), inclusive massa e volume.
   - Resumo dos apontamentos no mesmo layout da Fresagem, com **Editar** (formulário só ao editar) e ↺ Restaurar. Apontamentos alterados ficam em roxo, com uma linha “Campo: Fresagem X → RDO Y (±dif.)”.
   - Resumo da fresagem como referência (recolhido).
3. **Acompanhamento da aplicação** — usa **somente** dados da fresagem (mais segmentos extras cadastrados aqui); nada do RDO.
   - Total usinado (vem da fresagem), placa do último caminhão aplicado, total acumulado até esse caminhão, se foi aplicado por inteiro e a sobra dele.
   - **Massa disponível** = total usinado − acumulado até o caminhão + sobra do caminhão.
   - Lista **A APLICAR** (segmentos fresados não aplicados + extras) com a massa necessária.
   - **Segmentos extras** (Editar/Excluir) aparecem só aqui e somam na massa necessária.
   - No final: **saldo** = disponível − necessária. Falta → alerta para acionar a usina. Sobra → metros a mais a fresar = saldo ÷ (espessura × largura × densidade).

Um aviso fixo no topo mostra o saldo do painel aberto, sempre a partir da mesma massa usinada:
- Fresagem: usinado − fresado.
- RDO: usinado − apontado no RDO.
- Acompanhamento: usinado − acumulado até o último caminhão + sobra desse caminhão − a aplicar.

Amarelo = sobra, vermelho = falta, verde = dentro da tolerância.

No Acompanhamento, o quadro de caminhões mostra o total usinado, o nº e a placa do último aplicado e os restantes a aplicar (total − nº do último, +1 se o último teve sobra).

## Relatórios

Cada painel tem o botão **Imprimir relatório** (A4), com cabeçalho (nome, data, obra/trecho, responsável) e somente os dados daquele painel: Fresagem (usinado do dia, segmentos, área/volume/massa), RDO (apontamentos, área/volume/massa aplicada) e Acompanhamento (último caminhão, segmentos a aplicar com extras, saldo e metros a fresar).

## Dados

- Salvos automaticamente no próprio aparelho (navegador).
- Menu ⋯: salvar/abrir arquivo `.json` (abre arquivos das versões anteriores), imprimir relatório, novo apontamento.
