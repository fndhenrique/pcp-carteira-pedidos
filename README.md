# 🏭 Visão Geral da Produção (End-to-End: Python + Power BI)


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
* **Raio-X da Galhada (Scatter Plot):** Cruzamento da *Média de Peso da Peça* com o *Rendimento Metálico* por SKU, permitindo à Engenharia de Processos identificar rapidamente moldes críticos de alto volume que consomem energia térmica em excesso.
* **Ofensores de Sucata por Cliente:** Gráfico 100% empilhado apontando quais clientes possuem o pior mix de rendimento, impactando a margem de lucro da operação.

---

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.x
* **Bibliotecas de Dados:** `pandas`, `numpy`, `faker`, `datetime`
* **Visualização:** Power BI (DAX, Modelagem Star Schema)
