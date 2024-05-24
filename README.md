# projeto-cloud

## Pedro Drumond

### Sobre o Projeto
O projeto é uma implementação de uma infraestrutura na AWS utilizando os serviços de VPC, subnets, Auto Scaling com instâncias EC2, Application Load Balancer (ALB), DynamoDB e endpoints de VPC. O objetivo foi criar uma arquitetura que fosse escalável e segura para aplicar uma aplicação.

### Visão Geral da Arquitetura do Projeto
A arquitetura proposta consiste em uma Virtual Private Cloud (VPC) que pode hospedar subnets públicas e privadas, configuradas para suportar instâncias EC2 que são escaladas automaticamente com base na demanda. Um Application Load Balancer (ALB) distribui o tráfego de entrada entre as instâncias EC2 para garantir alta disponibilidade e escalabilidade. Um banco de dados DynamoDB é utilizado para armazenamento de dados, proporcionando alta performance e escalabilidade automática. Para melhorar a segurança e a eficiência, um endpoint VPC é configurado para acesso ao DynamoDB sem a necessidade de saída pela internet.



### Passo a Passo

## Criar
aws cloudformation create-stack --stack-name jameStack --template-body file://projeto.yaml --capabilities CAPABILITY_IAM --region sa-east-1

## Update
aws cloudformation update-stack --stack-name jameStack --template-body file://projeto.yaml --capabilities CAPABILITY_IAM --region sa-east-1

## Delete
 aws cloudformation delete-stack --jameStack MyInfrastructure
