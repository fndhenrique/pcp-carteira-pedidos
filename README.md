# 🏭 Visão Geral da Produção (End-to-End: Python + Power BI)
<img width="1316" height="734" alt="VISÃO GERAL DA PRODUÇÃO" src="https://github.com/user-attachments/assets/e58fe8e0-8b1d-46da-a8ea-bc8d5f8edc40" />


## 📌 Visão Geral do Projeto
Este projeto é uma solução completa de dados (*End-to-End*) focada no **Planejamento e Controle da Produção (PCP)** de uma indústria metalúrgica/fundição. O objetivo foi transformar dados brutos de pedidos e catálogos de produtos em uma "Torre de Controle" para tomada de decisão tática no chão de fábrica, equilibrando o atendimento aos prazos com a eficiência no consumo térmico.

---

## ⚙️ Arquitetura da Solução & Engenharia de Dados (Python)
Todo o pipeline de ETL (Extração, Transformação e Carga) foi construído em **Python**. O script não apenas limpa os dados, mas simula um ambiente de produção dinâmico, aplicando regras matemáticas de engenharia.

### 1. Data Quality & Anonimização (LGPD)
* Utilização da biblioteca `Faker` para anonimizar as razões sociais dos clientes e as descrições técnicas dos produtos, permitindo a exibição pública do portfólio sem ferir o compliance corporativo.

### 2. Tratamento e Limpeza
* Remoção estrutural de colunas desnecessárias e tratamento de dados nulos/vazios (`dropna`) para garantir a integridade do modelo semântico no Power BI.

### 3. Motor de Simulação & Regras de Negócio
Para dar robustez à base de dados, o script simula a entrada de 500 novos pedidos mantendo a integridade relacional do catálogo, aplicando as seguintes regras industriais:
* **Geração de Prazos (Dias Úteis):** Algoritmo que calcula datas de entrega lógicas, saltando automaticamente sábados e domingos utilizando a biblioteca `datetime`.
* **Dimensionamento de Produção:** Cálculo do número de caixas a produzir usando vetorização com `numpy.ceil()`, arredondando fracionamentos de projeto para o teto.
* **Cálculo de Eficiência Térmica:** Separação do "Peso Cheio" vazado no forno para extrair o **Peso Exclusivo de Galhada** (sucata de retorno) e o volume de peças boas (`PEÇAS VAZADAS`).
* **Status de Produção Dinâmico:** Simulação de apontamentos no chão de fábrica que classificam os pedidos em "TOTAL", "PARCIAL" ou "NÃO PRODUZIDO".

---

## 📊 Dashboard Executivo (Power BI)
Os dados processados alimentam um painel interativo (Dark Theme) focado em **atendimento de prazos** e **redução de desperdício metálico**:

* **KPIs Principais:** Acompanhamento imediato de Progresso da Produção (%), Total Produzido, Saldo a Produzir (Backlog) e Rendimento Metálico Global.
* **Acompanhamento de Carteira:** Gráfico combinado de série temporal cruzando o que foi pedido vs. o que foi efetivamente produzido dentro das datas de entrega.
<img width="552" height="249" alt="Captura de tela 2026-08-18 143145" src="https://github.com/user-attachments/assets/85edaf02-0117-48d4-888d-087b55785c2f" />

* **Raio-X da Galhada (Scatter Plot):** Cruzamento da *Média de Peso da Peça* com o *Rendimento Metálico* por SKU, permitindo à Engenharia de Processos identificar rapidamente moldes críticos de alto volume que consomem energia térmica em excesso.
<img width="630" height="252" alt="RENDIMENTO POR PESO DE PEÇA" src="https://github.com/user-attachments/assets/606fb5ea-ddf1-462e-8d35-c16ed9c6e2a1" />

* **Ofensores de Sucata por Cliente:** Gráfico 100% empilhado apontando quais clientes possuem o pior mix de rendimento, impactando a margem de lucro da operação.
<img width="550" height="280" alt="PROPORÇÃO PEÇA VS  GALHADA" src="https://github.com/user-attachments/assets/b22920b3-bc3c-445b-b473-af398ef303b2" />


---

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.x
* **Bibliotecas de Dados:** `pandas`, `numpy`, `faker`, `datetime`
* **Visualização:** Power BI (DAX, Modelagem Star Schema)
