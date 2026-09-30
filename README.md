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

## Navegação

Menu lateral (☰, canto superior esquerdo) com as páginas: Fresagem, RDO aplicação, Acompanhamento, **Controle de geometria** e **Viagens de fresado**.

## Controle de geometria

- Base geográfica `geo.json`, gerada por `tools/build_geo.py` a partir de `data-src/B2B3_KMZ_Estaca.kmz` (estaca, coordenadas, hodômetro contínuo) e `data-src/R08_unifilar_solucoes_BR277.json` (código da solução por sentido e faixa). O script confere que os dois arquivos batem estaca a estaca e que o hodômetro é contínuo (passo de 20 m).
- O GPS do celular é projetado sobre a linha das estacas para estimar a estaca (hodômetro). O cálculo roda no aparelho, funcionando sem sinal; os registros vão para o servidor.
- Precisão pior que 25 m, GPS antigo ou distância maior que 60 m do eixo são sinalizados; sobreposição de panos ou ausência de correspondência exigem escolha manual. Também é possível informar a estaca manualmente.
- Sentido e faixa são sugeridos pelo pano e precisam ser confirmados.
- A espessura de projeto não existe no unifilar: vem da legenda por código (FF 0,060 m, FE 0,100 m, FS 0,040 m informados; os demais em branco até serem preenchidos). Sem espessura cadastrada, a leitura é salva sem comparação.
- Comprimento: medida única por pano, com correções guardadas em histórico. Largura e espessura: várias leituras, cada uma com data/hora, GPS e precisão, estaca, pano, segmento de projeto, solução, sentido, faixa e (espessura) a espessura de projeto usada. Leituras agrupadas por segmento de projeto quando o pano atravessa mais de um.

## Viagens de fresado

- Cartões das 7 placas da frota fixa; toque → Chegada ou Saída.
- Toque repetido do mesmo evento da mesma placa em menos de 60 s é ignorado; evento igual ao anterior (ex.: duas chegadas seguidas) gera aviso e pede confirmação.
- Histórico do dia; quem registrou pode corrigir tipo/horário ou cancelar, e cada correção fica guardada.
- Status de envio: salvo no servidor, envio pendente (sem conexão) ou falhou.

## Relatórios

Cada painel tem o botão **Imprimir relatório** (A4), com cabeçalho (nome, data, obra/trecho, responsável) e somente os dados daquele painel: Fresagem (usinado do dia, segmentos, área/volume/massa), RDO (apontamentos, área/volume/massa aplicada) e Acompanhamento (último caminhão, segmentos a aplicar com extras, saldo e metros a fresar).

## Uso em equipe (nuvem, com login)

Com a configuração do Firebase preenchida em `FIREBASE_CONFIG` (no `index.html`), o app passa a funcionar em equipe:

- Login com e-mail e senha (usuários criados pelo responsável no Console do Firebase; auto-cadastro desativado).
- Lista de apontamentos compartilhados; todos veem as alterações em tempo real.
- Cada segmento é salvo separado, com quem lançou, quem alterou o RDO e quem marcou como aplicado (e a hora).
- Funciona sem sinal: as alterações ficam no aparelho e sobem quando a internet volta (bolinha amarela = sincronizando, verde = sincronizado).
- Regras de segurança do banco em `firestore.rules`.

Sem configuração (`FIREBASE_CONFIG = null`), o app funciona só no aparelho, como antes.

## Dados

- Salvos automaticamente no próprio aparelho (navegador).
- Menu ⋯: salvar/abrir arquivo `.json` (abre arquivos das versões anteriores), imprimir relatório, novo apontamento.
