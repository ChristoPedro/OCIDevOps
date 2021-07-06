# OCIDevOps

Exemplo de Arquitetura Orientada a Eventos utilizando o Stack Cloud Native do OCI.

## Demo

Demonstração de Cloud Native utilizando Functions + Streaming + Connetor Hub 

- A função producer é trigada através do API Gateway e gera dados nas duas filas NoSQL e File.

- Connetor Hub dispara as funções quando existe um ítem na fila, a função consumernosql salva os dados em um Autonomous Json e a função consumer grava os dados em um arquivo no Object Storage.