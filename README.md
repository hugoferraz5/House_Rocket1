# House Rocket

<div align="center">
<img src="https://user-images.githubusercontent.com/91911052/168933137-774b3228-30db-4b76-a2ae-ea28ed9d6ec4.jpg" width="700px" />
</div>

## Apresentação
A House Rocket é uma empresa focada na revenda de imóveis, ou seja compra imóveis com alto potencial de revenda e vende depois por um preço maior obtendo seu lucro. Vários são os pontos de análises para a compra do imóvel como são os casos da sua localização e preços baixos.
As melhores oportunidades de negócio deverão ser descobertas pelo cientista de dados e que poderão responder todas as requisições do CEO da empresa através da exploração dos dados.Logo, essa análise exploratória dos dados disponíveis poderão mostrar se o negócio será positivo ou negativo.
Os dados podem ser encontrados em https://www.kaggle.com/harlfoxem/housesalesprediction/discussion/207885


As requisições do CEO são:

* Quais casas o CEO da House Rocket deveria comprar e por qual preço de compra?
* Uma vez a casa em posse da empresa, qual o melhor momento para vendê-las e qual seria o preço da venda?

As explorações e requisições do CEO podem ser encontradas em https://analytics-house-rocket1.herokuapp.com/

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
