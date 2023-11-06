# House Rocket

<div align="center">
<img src="https://user-images.githubusercontent.com/91911052/168933137-774b3228-30db-4b76-a2ae-ea28ed9d6ec4.jpg" width="700px" />
</div>

## Apresentação
A House Rocket é uma empresa focada na revenda de imóveis, ou seja compra imóveis com alto potencial de revenda e vende depois por um preço maior obtendo seu lucro. Vários são os pontos de análises para a compra do imóvel como são os casos da sua localização e preços baixos.
As melhores oportunidades de negócio deverão ser descobertas pelo cientista de dados e que poderão responder todas as requisições do CEO da empresa através da exploração dos dados.Logo, essa análise exploratória dos dados disponíveis poderão mostrar se o negócio será positivo ou negativo.
Os dados podem ser encontrados em <a href="//www.kaggle.com/harlfoxem/housesalesprediction/discussion/207885">Kaggle</a>.


As requisições do CEO são:

* Quais casas o CEO da House Rocket deveria comprar e por qual preço de compra?
* Uma vez a casa em posse da empresa, qual o melhor momento para vendê-las e qual seria o preço da venda?

As explorações e requisições do CEO podem ser encontradas em <a href="https://github.com/hugoferraz5/House_Rocket1/blob/master/House_Rocket_Dashboard.ipynb">Jupyter</a> e os dashboards em <a href="https://analytics-house-rocket1.herokuapp.com/">Dashboards_streamlit</a>.
| Attribute | Description |
| :----- | :----- |
| id | ID das casas |
| date | Data da venda da casa |
| price | Preço de cada casa vendida |
| bedrooms | Numero de quartos |
| bathrooms | Número de banheiros: 0,5 significa um quarto com banheiro, mas sem chuveiro |
| sqft_living | Metragem quadrada do espaço interior da casa |
| sqft_lot | Metragem quadrada do terreno |
| floors | Número de pisos |
| waterfront | Se a casa tinha vista para o mar ou não |
| view | Índice de 0 a 4 de quão boa era a vista do imóvel |
| condition | Índice de 1 a 5 sobre o estado da casa |
| grade | Índice de 1 a 13: 1-3 fica aquém da construção e design de edifícios, 7 tem um nível médio de construção e design e 11-13 tem um nível de construção e design de alta qualidade |
| sqft_above | Metragem quadrada do espaço interno da habitação acima do nível do solo |
| sqft_basement | Metragem quadrada do espaço interno da habitação que fica abaixo do nível do solo |
| yr_built | Ano em que a casa foi inicialmente construída |
| yr_renovated | Ano da última reforma da casa |
| zipcode | CEP da casa |
| lat | Latitude |
| long | Longitude |
| sqft_living15 | Tamanho médio do espaço interno da habitação para as 15 casas mais próximas, em pés quadrados |
| sqft_lot15 | Tamanho médio dos terrenos para as 15 casas mais próximas, em metros quadrados |


## Premissas de negócio 
* Estação do ano foi um dos fatores para análise de compra do imóvel
* A coluna date mostra a data que a casa foi vendida anteriormente
* As condições do imóvel foi fator determinante para análise de compra do imóvel
* A coluna price mostra o preço que o imóvel foi vendido anteriormente
* A coluna view mostra se o imóvel é em frente ou não ao rio e foi fator determinante na análise de compra

## Insights de negócio
* Imóveis com vista para a água são em média 30% mais caros

Verdadeiro: Investir em casas com vista para água

* Imóveis com data de construção menor que 1955 são em média 50% mais baratos

Falso: Independe o investimento para data de construção acima ou abaixo de 1955

* Imóveis sem porão com maior área total são 40% mais caros do que imóveis com porão

Verdadeiro: Investir em casas sem porão

* Imóveis antigos e não renovados são 40% mais baratos

Verdadeiro: Investir em casas antigas e não reformadas e reformar para venda

* Imóveis com mais banheiros são em média 5% mais caros

Falso: Investir em casas com 3 a 5 banheiros

* O crescimento do preço dos imóveis mês após mês no ano de 2014 é de 10%

Falso: Investir em casas nos meses de menor custo

* Imóveis com 3 banheiros tem um crescimento mês após mês de 15 %

Falso: Investir em casas nos meses de menor custo
## Conclusão
Nesse projeto foram requiridos pelo CEO 2 perguntas e elas foram respondidas através da exploração dos dados pelo Cientista de dados. As perguntas foram:
* Quais casas o CEO da House Rocket deveria comprar e por qual preço de compra?
* Uma vez a casa em posse da empresa, qual o melhor momento para vendê-las e qual seria o preço da venda?

Primeiramente, os imóveis foram divididos por região(zipcode) e em cada zipcode foi calculado as medianas dos preços de compras. A partir dessas medianas, as casas com preços menores e com condições maiores ou iguais a 2 foram selecionadas como aptas.
Com os imóveis aptos para compra, o melhor período(estação do ano) para revenda foi o verão, pois é o período onde o lucro será maior. As casas foram divididas por região(zipcode) e período(estação do ano) através da mediana dos preços de compra e suas datas.
Se o imóvel tiver o preço de compra abaixo da mediana das casas em determinado período do ano por zipcode, terá um acréscimo de 30% no preço da revenda, senão terá apenas 10%.Logo, o objetivo foi alcançado.

## Próximos Passos

Para próximos passos, seria interessante retirar o porão e expandir mais o imóvel, pois casas sem porão e com áreas totatis maiores são 40% mais caros.
