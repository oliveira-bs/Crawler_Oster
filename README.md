### Crawler - Oster

Esse projeto tem como finalidade extrair informações referente aos produtos disponíveis no site da [Oster](https://www.oster.com.br/). Para isso, foi desenvolvido um crawler baseado na linguagem python com a ferramenta **Scrapy** .

O objetivo do crawler é extrair as seguintes informações para cada produto:
* GTIN (gtin)
* Nome do produto (name)
* Moeda de transação (currency)
* Preço (price)
* Departamento (category)
* Cod. do produto na Loja (sku)
* Vendedor (seller)
* Url do produto (pageUrl)
* Url da imagem do produto (image)
* Data da extração (created_at)

Com esses dados podemos monitorar a validade das precificação de cada produto e realizar a rastreabilidade dessa informação via código GTIN(global)/sku(ambiente e-commerce).  

### Especificações - site

O site da [Oster](https://www.oster.com.br/) funciona no modelo de e-commerce e é baseado em JavaScript, portanto exige a interação com alguns elementos gráficos da página para realizar ações, por exemplo: carregar próximos produtos por meio do **scroll down**.

### Estratégia para raspagem

A estratégia para extrair os dados do site foi acessar o [Sitemaps](https://www.oster.com.br/sitemap/sitemap.xml) para acessar os setores/departamentos dos medicamentos. A paginação desses itens foi realizada com a manipulação da url base de cada departamento. Os dados extraídos são armazenados em formato *json* no diretório *raw*.