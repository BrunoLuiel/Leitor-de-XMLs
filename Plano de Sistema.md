O que eu quero:
r: Banco de dados para fazer auditorias

Sumario dos passos para concluir este plano:
 1- Importar NF-e
    1.2- Criar Foreing Key com CT-e
    1.2- importar eventos vinculando situação do documento quando:
        1.2.1- cancelada
        1.2.2- CC-e


 2- Importar CT-e
    1.2- Criar Foreing Key
    1.2- importar eventos vinculando situação do documento quando:
        1.2.1- cancelada
        1.2.2- CC-e

Etapas:
1- Importar documento fiscal:
    1.1- Regra de reconhecimento do XML:
        -Se o arquivo tiver a tag <mod>55</mod> ou <mod>65</mod> usar importador de NF-e
        -Se o arquivo tiver a tag <mod>57</mod> usar importador de CT-e
        -se o arquivo tiver a tag <detEvento> usar o importador de eventos

        #Regra para todas as importações:
        Ao iniciar uma nova seção de importação limpar o arquivo relatório de importação
        inserir cópia dos arquivos XMLs dentro da pasta do programa para fazer exportação depois

1- 1.1 Importar NF-e pelo PyQT5
        1.1.1- Entregar relatório de notas lançadas e não lançadas podendo haver os seguintes porques:
            1.1.1.1- Nota já existe
            1.1.1.2- Erro na importação desconhecido
