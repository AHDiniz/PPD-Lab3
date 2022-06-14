# PPD-Lab3

Experimento com arquitetura publisher/subscriber para sistemas distribuídos. Um pequeno vídeo mostrando sua execução pode ser encontrado [neste link](https://drive.google.com/uc?id=1BiHqm--zcvpr3hkBWhK1H-SsqZwX8TOW&export=download).

## Instalação
Para rodar corretamente este projeto, instale as dependencias python contidas no arquivo [requirements.txt](./requirements.txt). Uma forma rápida de realizar essas instalações é rodar, caso esteja usando python, o comando:

``` $ pip install -r ./requirements.txt ```

ou, caso esteja usando python3, o comando:

``` $ pip3 install -r ./requirements.txt ```

Este projeto requer ainda a instalação do [Eclipse Mosquitto&trade;](https://mosquitto.org/).

## Rodando

Para rodar este programa, primeiro esteja certo de ter o [Eclipse Mosquitto&trade;](https://mosquitto.org/) rodando. Após isto, rode o server, caso esteja usando python, com o comando:

``` $ python miner/miner_server.py ```

ou, caso esteja usando python3, o comando:

``` $ python3 miner/miner_server.py ```

Após rodar o server, rode o script clinte, caso esteja usando python, com o comando:

``` $ python miner/miner_client.py ```

ou, caso esteja usando python3, o comando:

``` $ python3 miner/miner_client.py ```

## Sobre o [Eclipse Mosquitto&trade;](https://mosquitto.org/)
> Eclipse Mosquitto is an open source (EPL/EDL licensed) message broker that implements the MQTT protocol versions 5.0, 3.1.1 and 3.1. Mosquitto is lightweight and is suitable for use on all devices from low power single board computers to full servers.

> The MQTT protocol provides a lightweight method of carrying out messaging using a publish/subscribe model. This makes it suitable for Internet of Things messaging such as with low power sensors or mobile devices such as phones, embedded computers or microcontrollers.

> The Mosquitto project also provides a C library for implementing MQTT clients, and the very popular mosquitto_pub and mosquitto_sub command line MQTT clients.

> Mosquitto is part of the Eclipse Foundation, is an iot.eclipse.org project and is sponsored by cedalo.com.

Texto retirado do site https://mosquitto.org/.
Acessado no dia 14/06/2022.