import os
import xml.etree.ElementTree as Et
from datetime import date, datetime
import data_base

class Read_xml():
    def __init__(self, directory):
        self.directory = directory
    
    def all_files(self):
        return [ os.path.join(self.directory, arq) for arq in os.listdir(self.directory) if arq.lower().endswith('.xml')]

    def check_chave(self, xml):

        self.xml = xml
        root = Et.parse(self.xml).getroot()
        nsNFe = {"ns":"http://www.portalfiscal.inf.br/nfe"}

        self.chave = self.check_none(root.find('./ns:protNFe/ns:infProt/ns:chNFe', nsNFe))
        nfe = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:nNF", nsNFe))
        nome_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:xNome', nsNFe))

        dbdb = data_base.DataBase()
        dbdb.conecta()
        if dbdb.check_nota(self.chave) == 'Não existe':
            with open('Relatório de importação.txt', 'a') as arq:
                arq.write(f'Importada com sucesso NF-e n° {nfe} emitida por {nome_emit}, {self.chave} \n')
                arq.close()
                self.nfe_data(self.xml)

        else:
            with open('Relatório de importação.txt', 'a') as arq:
                arq.write(f'ESTA NOTA JÁ EXISTE! {nfe} emitida por {nome_emit}, {self.chave} \n')
                arq.close()

        dbdb.close_conection()

    def nfe_data(self, xml):
        root = Et.parse(xml).getroot()
        nsNFe = {"ns":"http://www.portalfiscal.inf.br/nfe"}

        #Dados da NF-e
        chave = self.check_none(root.find('./ns:protNFe/ns:infProt/ns:chNFe', nsNFe))
        nat_op = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:natOp", nsNFe))
        mod = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:mod", nsNFe))
        nfe = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:nNF", nsNFe))
        serie = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:serie", nsNFe))
        data_emissao = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:dhEmi", nsNFe))
        data_emissao = f'{data_emissao[8:10]}/{data_emissao[5:7]}/{data_emissao[:4]}'
        data_saient = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:dhSaiEnt", nsNFe))
        data_saient = f'{data_saient[8:10]}/{data_saient[5:7]}/{data_saient[:4]}'
        tp_nf = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:tpNF", nsNFe))
        cod_mun_fg = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:cMunFG", nsNFe)) #Código do municipio do fato gerador
        id_dest= self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:idDest", nsNFe)) #Identificador do destino da operação (1-Interna;2-Interestadual;3-Exterior)
        tp_imp = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:tpImp", nsNFe)) #Formato de impressão do DANFE (0-sem DANFE;1-DANFe Retrato; 2-DANFe Paisagem;3-DANFe Simplificado;4-DANFe NFC-e;5-DANFe NFC-e em mensagem eletrônica)
        tp_emi = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:tpEmis", nsNFe)) #Forma de emissão da NF-e: 1 - Normal; 2 - Contingência FS; 3 - Regime Especial NFF (NT 2021.002); 4 - Contingência DPEC; 5 - Contingência FSDA; 6 - Contingência SVC - AN; 7 - Contingência SVC - RS; 9 - Contingência off-line NFC-e
        tp_amb = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:tpAmb", nsNFe)) #1 - Produção; 2 - Homologação
        fin_nfe = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:finNFe", nsNFe)) #1 - NFe normal; 2 - NFe complementar; 3 - NFe de ajuste; 4 - Devolução/Retorno
        ind_pres = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:indPres", nsNFe)) #Indicador de presença do comprador no estabelecimento comercial no momento da oepração(0-Não se aplica (ex.: Nota Fiscal complementar ou de ajuste;1-Operação presencial;2-Não presencial, internet;3-Não presencial, teleatendimento;4-NFC-e entrega em domicílio;5-Operação presencial, fora do estabelecimento;9-Não presencial, outros)

        #Notas referenciadas
        nf_ref = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:NFref/ns:refNFe", nsNFe))        



        #Dados Emitente
        if self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:CPF', nsNFe)) != '':
            doc_emit = self.format_cnpj_cpf(self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:CPF', nsNFe)))
        elif  self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:CNPJ', nsNFe)) != '':
            doc_emit = self.format_cnpj_cpf(self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:CNPJ', nsNFe)))
        else:
            print('erro na definição do emitente')
            quit()
        

        nome_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:xNome', nsNFe))
        fantasia_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:xFant', nsNFe))
        rua_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:xLgr', nsNFe))
        nro_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:nro', nsNFe))
        bairro_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:xBairro', nsNFe))
        cod_mun_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:cMun', nsNFe))
        mun_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:xMun', nsNFe))
        uf_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:UF', nsNFe))
        cep_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:CEP', nsNFe))
        cod_pais_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:cPais', nsNFe))
        pais_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:xPais', nsNFe))
        fone_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:fone', nsNFe))
        ie_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:IE', nsNFe))
        cnae_fiscal = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:CNAE', nsNFe))
        crt_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:CRT', nsNFe)) #1 – Simples Nacional; 2 – Simples Nacional – excesso de sublimite de receita bruta; 3 – Regime Normal.

        #Nota Avulsa
        cnpj_avulsa = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:avulsa/ns:CNPJ", nsNFe)) #CNPJ do orgão emissor
        nome_avulsa = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:avulsa/ns:xOrgao", nsNFe))

        #Dados do destinatário
        if self.check_none(root.find('./ns:NFe/ns:infNFe/ns:dest/ns:CPF', nsNFe)) != '':
            doc_dest = self.format_cnpj_cpf(self.check_none(root.find('./ns:NFe/ns:infNFe/ns:dest/ns:CPF', nsNFe)))
        elif  self.check_none(root.find('./ns:NFe/ns:infNFe/ns:dest/ns:CNPJ', nsNFe)) != '':
            doc_dest = self.format_cnpj_cpf(self.check_none(root.find('./ns:NFe/ns:infNFe/ns:dest/ns:CNPJ', nsNFe)))
        else:
            print('erro na definição do destinatario')
            quit()

        nome_dest = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:dest/ns:xNome', nsNFe))
        rua_dest = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:xLgr', nsNFe))
        nro_dest = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:nro', nsNFe))
        cpl_dest = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:xCpl', nsNFe)) #Complemento
        bairro_dest = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:xBairro', nsNFe))
        cod_mun_dest = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:cMun', nsNFe))
        mun_dest = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:xMun', nsNFe))
        uf_dest = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:UF', nsNFe))
        cep_dest = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:CEP', nsNFe))
        cod_pais_dest = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:cPais', nsNFe))
        pais_dest = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:xPais', nsNFe))
        fone_dest = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:fone', nsNFe))
        sit_ie_dest = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:dest/ns:indIEDest', nsNFe)) #Indicador da IE do destinatário: 1 – Contribuinte ICMSpagamento à vista; 2 – Contribuinte isento de inscrição; 9 – Não Contribuinte
        ie_dest = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:dest/ns:IE', nsNFe))
        isuf_dest = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:dest/ns:ISUF', nsNFe)) #Suframa
        im_dest = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:dest/ns:IM', nsNFe)) #Inscrição Municipal
        email_dest = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:dest/ns:email', nsNFe))

        #Dados da Retirada
        if self.check_none(root.find('./ns:NFe/ns:infNFe/ns:retirada/ns:CPF', nsNFe)) != '':
            doc_retirada = self.format_cnpj_cpf(self.check_none(root.find('./ns:NFe/ns:infNFe/ns:retirada/ns:CPF', nsNFe)))
        elif  self.check_none(root.find('./ns:NFe/ns:infNFe/ns:retirada/ns:CNPJ', nsNFe)) != '':
            doc_retirada = self.format_cnpj_cpf(self.check_none(root.find('./ns:NFe/ns:infNFe/ns:retirada/ns:CNPJ', nsNFe)))
        else:
            doc_retirada = ''

        nome_retirada = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:retirada/ns:xNome', nsNFe))
        rua_retirada = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:retirada/ns:xLgr', nsNFe))
        nro_retirada = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:retirada/ns:nro', nsNFe))
        cpl_retirada = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:retirada/ns:xCpl', nsNFe)) #Complemento
        bairro_retirada = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:retirada/ns:xBairro', nsNFe))
        cod_mun_retirada = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:retirada/ns:cMun', nsNFe))
        mun_retirada = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:retirada/ns:xMun', nsNFe))
        uf_retirada = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:retirada/ns:UF', nsNFe))
        cep_retirada = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:retirada/ns:CEP', nsNFe))
        cod_pais_retirada = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:retirada/ns:cPais', nsNFe))
        pais_retirada = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:retirada/ns:xPais', nsNFe))
        fone_retirada = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:retirada/ns:fone', nsNFe))
        email_retirada = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:retirada/ns:email', nsNFe))
        ie_retirada = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:retirada/ns:IE', nsNFe))

        #Dados entrega
        if self.check_none(root.find('./ns:NFe/ns:infNFe/ns:entrega/ns:CPF', nsNFe)) != '':
            doc_entrega = self.format_cnpj_cpf(self.check_none(root.find('./ns:NFe/ns:infNFe/ns:entrega/ns:CPF', nsNFe)))
        elif  self.check_none(root.find('./ns:NFe/ns:infNFe/ns:entrega/ns:CNPJ', nsNFe)) != '':
            doc_entrega = self.format_cnpj_cpf(self.check_none(root.find('./ns:NFe/ns:infNFe/ns:entrega/ns:CNPJ', nsNFe)))
        else:
            doc_entrega = ''

        nome_entrega = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:entrega/ns:xNome', nsNFe))
        rua_entrega = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:entrega/ns:xLgr', nsNFe))
        nro_entrega = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:entrega/ns:nro', nsNFe))
        cpl_entrega = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:entrega/ns:xCpl', nsNFe)) #Complemento
        bairro_entrega = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:entrega/ns:xBairro', nsNFe))
        cod_mun_entrega = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:entrega/ns:cMun', nsNFe))
        mun_entrega = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:entrega/ns:xMun', nsNFe))
        uf_entrega = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:entrega/ns:UF', nsNFe))
        cep_entrega = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:entrega/ns:CEP', nsNFe))
        cod_pais_entrega = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:entrega/ns:cPais', nsNFe))
        pais_entrega = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:entrega/ns:xPais', nsNFe))
        fone_entrega = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:entrega/ns:fone', nsNFe))
        email_entrega = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:entrega/ns:email', nsNFe))
        ie_entrega = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:entrega/ns:IE', nsNFe))

        #Totais da nota
        t_bc_icms = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vBC", nsNFe))
        t_v_icms = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vICMS", nsNFe))
        t_v_deso = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vICMSDeson", nsNFe))
        pcfufdest = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vFCPUFDest", nsNFe))
        icmsufdest = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vICMSUFDest", nsNFe))
        icmsufremet = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vICMSUFRemet", nsNFe))
        t_fcp = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vFCP", nsNFe))
        t_bcst = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vBCST", nsNFe))
        t_st = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vST", nsNFe))
        t_fcpst = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vFCPST", nsNFe))
        t_fcpst_ret = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vFCPSTRet", nsNFe))
        t_vprod = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vProd", nsNFe))
        t_vfrete = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vFrete", nsNFe))
        t_vseguro = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vSeg", nsNFe))
        t_vdesc = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vDesc", nsNFe))
        t_vii = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vII", nsNFe))
        t_vipi = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vIPI", nsNFe))
        t_vpis = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vPIS", nsNFe))
        t_vcofins = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vCOFINS", nsNFe))
        t_voutro = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vOutro", nsNFe))
        t_nf = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vNF", nsNFe))
        t_trib = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vTotTrib", nsNFe))    

        #Transporte
        modfrete = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:transp/ns:modFrete", nsNFe))
        if self.check_none(root.find('./ns:NFe/ns:infNFe/ns:transp/ns:transporta/ns:CPF', nsNFe)) != '':
            doc_trans = self.format_cnpj_cpf(self.check_none(root.find('./ns:NFe/ns:infNFe/ns:transp/ns:transporta/ns:CPF', nsNFe)))
        elif  self.check_none(root.find('./ns:NFe/ns:infNFe/ns:entrega/ns:CNPJ', nsNFe)) != '':
            doc_trans = self.format_cnpj_cpf(self.check_none(root.find('./ns:NFe/ns:infNFe/ns:transp/ns:transporta/ns:CNPJ', nsNFe)))
        else:
            doc_trans = ''

        nome_trans = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:transp/ns:transporta/ns:xNome', nsNFe))
        ie_trans = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:transp/ns:transporta/ns:IE', nsNFe))
        ender_trans = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:transp/ns:transporta/ns:xEnder', nsNFe))
        mun_trans = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:transp/ns:transporta/ns:xMun', nsNFe))
        uf_trans = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:transp/ns:transporta/ns:UF', nsNFe))
        #Dados importação
        data_importacao = datetime.now()
        data_importacao = data_importacao.strftime('%d/%m/%Y, %H:%M:%S', )
        usuario = str('bruno')

        #Insere NF-e
        dados_nota = [chave, nat_op, mod, nfe, serie, data_emissao, data_saient, tp_nf, cod_mun_fg, id_dest, tp_imp, tp_emi, tp_amb, 
        fin_nfe, ind_pres, nf_ref, doc_emit , nome_emit, fantasia_emit, rua_emit, nro_emit, bairro_emit, cod_mun_emit, mun_emit, uf_emit, cep_emit, 
        cod_pais_emit, pais_emit, fone_emit, ie_emit, cnae_fiscal, crt_emit, cnpj_avulsa, nome_avulsa, doc_dest , nome_dest, rua_dest, nro_dest, cpl_dest, 
        bairro_dest, cod_mun_dest, mun_dest, uf_dest, cep_dest, cod_pais_dest, pais_dest, fone_dest, sit_ie_dest, ie_dest, isuf_dest, im_dest, email_dest, 
        doc_retirada , nome_retirada, rua_retirada, nro_retirada, cpl_retirada, bairro_retirada, cod_mun_retirada, mun_retirada, uf_retirada, cep_retirada, 
        cod_pais_retirada, pais_retirada, fone_retirada, email_retirada, ie_retirada, doc_entrega, nome_entrega, rua_entrega, nro_entrega, cpl_entrega, 
        bairro_entrega, cod_mun_entrega, mun_entrega, uf_entrega, cep_entrega, cod_pais_entrega, pais_entrega, fone_entrega, email_entrega, ie_entrega, 
        t_bc_icms, t_v_icms, t_v_deso, pcfufdest, icmsufdest, icmsufremet, t_fcp, t_bcst, t_st, t_fcpst, t_fcpst_ret, t_vprod, t_vfrete, t_vseguro, 
        t_vdesc, t_vii, t_vipi, t_vpis, t_vcofins, t_voutro, t_nf, t_trib, modfrete, doc_trans, nome_trans, ie_trans, ender_trans, mun_trans,  uf_trans,
        data_importacao, usuario]

        dbdb = data_base.DataBase()
        dbdb.conecta()
        dbdb.insert_nfe(*dados_nota)
        dbdb.close_conection()

        #Cobrança
        """fat"""
        fat = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:cobr/ns:fat/ns:nFat', nsNFe))
        v_orig = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:cobr/ns:fat/ns:vOrig', nsNFe))
        v_desc = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:cobr/ns:fat/ns:vDesc', nsNFe))
        v_liq = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:cobr/ns:fat/ns:vLiq', nsNFe))
        usuario = 'bruno'


        dbdb.conecta()
        dbdb.insert_nfe_faturamento(chave, fat, v_orig, v_desc, v_liq, data_importacao, usuario)
        dbdb.close_conection()

        """duplicata"""
        dados_dp = []
        for dup in root.findall('.ns:NFe/ns:infNFe/ns:cobr/ns:dup', nsNFe):
            ndup = self.check_none(dup.find('.ns:nDup', nsNFe))
            dvenc = self.check_none(dup.find('.ns:dVenc', nsNFe))
            vdup = self.check_none(dup.find('.ns:vDup', nsNFe))
            
            dbdb.conecta()
            dbdb.insert_nfe_duplicata(chave, ndup, dvenc, vdup, data_importacao, usuario)
            dbdb.close_conection()

        #Item da nota
        itemNota = 1
        prod = []

        for item in root.findall("./ns:NFe/ns:infNFe/ns:det", nsNFe):
            cod_item =  self.check_none(item.find(".ns:prod/ns:cProd", nsNFe))
            c_ean = self.check_none(item.find(".ns:prod/ns:cEAN", nsNFe))
            c_barra = self.check_none(item.find(".ns:prod/ns:cBarra", nsNFe))
            descricao_item = self.check_none(item.find('.ns:prod/ns:xProd', nsNFe))
            ncm = self.check_none(item.find('.ns:prod/ns:NCM', nsNFe))
            nve = self.check_none(item.find('.ns:prod/ns:NVE', nsNFe))
            cest = self.check_none(item.find('.ns:prod/ns:CEST', nsNFe))
            cfop = self.check_none(item.find('.ns:prod/ns:CFOP', nsNFe))
            un_medida = self.check_none(item.find('.ns:prod/ns:uCom', nsNFe))
            qtd_item = self.check_none(item.find('.ns:prod/ns:qCom', nsNFe))
            vlr_unit_item = self.check_none(item.find('.ns:prod/ns:vUnCom', nsNFe))
            vlr_item = self.check_none(item.find('.ns:prod/ns:vProd', nsNFe))

            ind_escala = self.check_none(item.find('.ns:prod/ns:indEscala', nsNFe))
            cnpj_fab = self.check_none(item.find('.ns:prod/ns:CNPJFab', nsNFe))
            c_benef = self.check_none(item.find('.ns:prod/ns:cBenef', nsNFe))
            ex_tipi = self.check_none(item.find('.ns:prod/ns:EXTIPI', nsNFe))
            u_trib = self.check_none(item.find('.ns:prod/ns:uTrib', nsNFe))
            q_trib = self.check_none(item.find('.ns:prod/ns:qTrib', nsNFe))
            v_un_trib = self.check_none(item.find('.ns:prod/ns:vUnTrib', nsNFe))
            v_frete = self.check_none(item.find('.ns:prod/ns:vFrete', nsNFe))
            v_seg = self.check_none(item.find('.ns:prod/ns:vSeg', nsNFe))
            v_desc = self.check_none(item.find('.ns:prod/ns:vDesc', nsNFe))
            v_outro = self.check_none(item.find('.ns:prod/ns:vOutro', nsNFe))
            ind_tot = self.check_none(item.find('.ns:prod/ns:indTot', nsNFe))

            #Imposto
            v_tot_trib = self.check_none(item.find('.ns:imposto/ns:vTotTrib', nsNFe))
            codigos = ['/ns:ICMS00', '/ns:ICMS10', '/ns:ICMS20', '/ns:ICMS30', '/ns:ICMS40', '/ns:ICMS51', '/ns:ICMS60', '/ns:ICMS70', '/ns:ICMS90', '/ns:ICMSSN101', '/ns:ICMSSN102', '/ns:ICMSSN201', '/ns:ICMSSN202', '/ns:ICMSSN500', '/ns:ICMSSN900']
            for cada in codigos:
                if self.check_none(item.find(f'.ns:imposto/ns:ICMS{cada}/ns:orig', nsNFe)) == '':
                    pass
                else:
                    orig = self.check_none(item.find(f'.ns:imposto/ns:ICMS{cada}/ns:orig', nsNFe))
                    if self.check_none(item.find(f'.ns:imposto/ns:ICMS{cada}/ns:CST', nsNFe)) == '':
                        cst_csosn = self.check_none(item.find(f'.ns:imposto/ns:ICMS{cada}/ns:CSOSN', nsNFe))
                    else:
                        cst_csosn = self.check_none(item.find(f'.ns:imposto/ns:ICMS{cada}/ns:CST', nsNFe))
            #ICMS Partilhado entre estados
            orig_part = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSPart/ns:orig', nsNFe))
            cst_part = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSPart/ns:CST', nsNFe))
            mod_bc = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSPart/ns:modBC', nsNFe))
            v_bc = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSPart/ns:vBC', nsNFe))
            red_bc = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSPart/ns:pRedBC', nsNFe))
            icms_part = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSPart/ns:pICMS', nsNFe))
            v_icms_part = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSPart/ns:vICMS', nsNFe))
            mod_bcst = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSPart/ns:modBCST', nsNFe))
            mva_st_part = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSPart/ns:pMVAST', nsNFe))
            red_bc_st = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSPart/ns:pRedBCST', nsNFe))
            bc_st_part = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSPart/ns:vBCST', nsNFe))
            icms_st = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSPart/ns:pICMSST', nsNFe))
            pBCOp = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSPart/ns:pBCOp', nsNFe))
            uf_st = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSPart/ns:UFST', nsNFe))
            #ICMS S.T.
            orig_st = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSST/ns:orig', nsNFe))
            cst_st = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSST/ns:CST', nsNFe))
            bc_st_ret = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSST/ns:vBCSTRet', nsNFe))
            st = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSST/ns:pST', nsNFe))
            v_st = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSST/ns:vICMSSubstituto', nsNFe))
            v_st_ret = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSST/ns:vICMSSTRet', nsNFe))
            v_bcfcpst_ret = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSST/ns:vBCFCPSTRet', nsNFe))
            p_fcpst_ret = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSST/ns:pFCPSTRet', nsNFe))
            v_fcpst_ret = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSST/ns:vFCPSTRet', nsNFe))
            v_bcst_dest = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSST/ns:vBCSTDest', nsNFe))
            v_icms_st_dest = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSST/ns:vICMSSTDest', nsNFe))
            p_redbcefet = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSST/ns:pRedBCEfet', nsNFe))
            v_bcefet = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSST/ns:vBCEfet', nsNFe))
            p_icms_efet = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSST/ns:pICMSEfet', nsNFe))
            v_icms_efet = self.check_none(item.find('.ns:imposto/ns:ICMS/ns:ICMSST/ns:vICMSEfet', nsNFe))
            #IPI
            cst_ipi = self.check_none(item.find('.ns:imposto/ns:IPI/ns:IPITrib/ns:CST', nsNFe))
            bc_ipi = self.check_none(item.find('.ns:imposto/ns:IPI/ns:IPITrib/ns:vBC', nsNFe))
            p_ipi = self.check_none(item.find('.ns:imposto/ns:IPI/ns:IPITrib/ns:pIPI', nsNFe))
            q_unid_ipi = self.check_none(item.find('.ns:imposto/ns:IPI/ns:IPITrib/ns:qUnid', nsNFe))
            v_unid_ipi = self.check_none(item.find('.ns:imposto/ns:IPI/ns:IPITrib/ns:vUnid', nsNFe))
            v_ipi = self.check_none(item.find('.ns:imposto/ns:IPI/ns:IPITrib/ns:vIPI', nsNFe))
            cst_int = self.check_none(item.find('.ns:imposto/ns:IPI/ns:IPINT/ns:CST', nsNFe))
            #II
            v_bc_ii = self.check_none(item.find('.ns:imposto/ns:II/ns:vBC', nsNFe))
            v_desp_adu = self.check_none(item.find('.ns:imposto/ns:II/ns:vDespAdu', nsNFe))
            v_ii = self.check_none(item.find('.ns:imposto/ns:II/ns:vII', nsNFe))
            v_iof = self.check_none(item.find('.ns:imposto/ns:II/ns:vIOF', nsNFe))
            #ISSQN
            v_bc_iss = self.check_none(item.find('.ns:imposto/ns:ISSQN/ns:vBC', nsNFe))
            alq_iss = self.check_none(item.find('.ns:imposto/ns:ISSQN/ns:vAliq', nsNFe))
            v_iss = self.check_none(item.find('.ns:imposto/ns:ISSQN/ns:vISSQN', nsNFe))
            c_mun_fg_iss = self.check_none(item.find('.ns:imposto/ns:ISSQN/ns:cMunFG', nsNFe))
            c_serv = self.check_none(item.find('.ns:imposto/ns:ISSQN/ns:cListServ', nsNFe))
            v_deducao = self.check_none(item.find('.ns:imposto/ns:ISSQN/ns:vDeducao', nsNFe))
            v_outro_iss = self.check_none(item.find('.ns:imposto/ns:ISSQN/ns:outro', nsNFe))
            v_desc_inc = self.check_none(item.find('.ns:imposto/ns:ISSQN/ns:vDescIncond', nsNFe))
            v_desc_cond = self.check_none(item.find('.ns:imposto/ns:ISSQN/ns:vDescCond', nsNFe))
            v_iss_ret = self.check_none(item.find('.ns:imposto/ns:ISSQN/ns:vISSRet', nsNFe))
            ind_iss = self.check_none(item.find('.ns:imposto/ns:ISSQN/ns:indISS', nsNFe))
            c_servico = self.check_none(item.find('.ns:imposto/ns:ISSQN/ns:cServico', nsNFe))
            c_mun = self.check_none(item.find('.ns:imposto/ns:ISSQN/ns:cMun', nsNFe))
            c_pais = self.check_none(item.find('.ns:imposto/ns:ISSQN/ns:cPais', nsNFe))
            n_processo = self.check_none(item.find('.ns:imposto/ns:ISSQN/ns:nProcesso', nsNFe))
            ind_incentivo = self.check_none(item.find('.ns:imposto/ns:ISSQN/ns:indIncentivo', nsNFe))
            #PIS
            cst_pis = self.check_none(item.find('.ns:imposto/ns:PIS/ns:PISAliq/ns:CST', nsNFe))
            v_bc_pis = self.check_none(item.find('.ns:imposto/ns:PIS/ns:PISAliq/ns:vBC', nsNFe))
            p_pis = self.check_none(item.find('.ns:imposto/ns:PIS/ns:PISAliq/ns:pPIS', nsNFe))
            v_pis = self.check_none(item.find('.ns:imposto/ns:PIS/ns:PISAliq/ns:vPIS', nsNFe))
            #COFINS
            cst_COFINS = self.check_none(item.find('.ns:imposto/ns:COFINS/ns:COFINSAliq/ns:CST', nsNFe))
            v_bc_COFINS = self.check_none(item.find('.ns:imposto/ns:COFINS/ns:COFINSAliq/ns:vBC', nsNFe))
            p_COFINS = self.check_none(item.find('.ns:imposto/ns:COFINS/ns:COFINSAliq/ns:pCOFINS', nsNFe))
            v_COFINS = self.check_none(item.find('.ns:imposto/ns:COFINS/ns:COFINSAliq/ns:vCOFINS', nsNFe))

            produtos = [chave, cod_item, c_ean, c_barra, descricao_item, ncm, nve, cest, cfop, un_medida, qtd_item, vlr_unit_item, vlr_item, ind_escala, cnpj_fab, c_benef, ex_tipi,
            u_trib, q_trib, v_un_trib, v_frete, v_seg, v_desc, v_outro, ind_tot, orig, cst_csosn, orig_part, cst_part, mod_bc, v_bc, red_bc, icms_part, v_icms_part, mod_bcst, mva_st_part,
            red_bc_st, bc_st_part, icms_st, pBCOp, uf_st, orig_st, cst_st, bc_st_ret, st, v_st, v_st_ret, v_bcfcpst_ret, p_fcpst_ret, v_fcpst_ret, v_bcst_dest, v_icms_st_dest, p_redbcefet, 
            v_bcefet, p_icms_efet, v_icms_efet, cst_ipi, bc_ipi, p_ipi, q_unid_ipi, v_unid_ipi, v_ipi, cst_int, v_bc_ii, v_desp_adu, v_ii, v_iof, v_bc_iss, alq_iss, v_iss, c_mun_fg_iss, 
            c_serv, v_deducao, v_outro_iss, v_desc_inc, v_desc_cond, v_iss_ret, ind_iss, c_servico, c_mun, c_pais, n_processo, ind_incentivo, cst_pis, v_bc_pis, p_pis, v_pis, cst_COFINS, 
            v_bc_COFINS, p_COFINS, v_COFINS, data_importacao, usuario]

            dbdb.conecta()
            dbdb.insert_nfe_produto(*produtos)
            dbdb.close_conection()

        

        







    def check_none(self, var):
        if var == None:
            return ''
        else:
            try:
                return var.text.replace('.',',')
            except:
                return var.text

    def format_cnpj_cpf(self, doc):
        if len(doc) == 14:
            try:
                doc = f'{doc[:2]}.{doc[2:5]}.{doc[5:8]}/{doc[8:12]}-{doc[12:14]}'
                return doc

            except:
                return ""
        elif len(doc) == 11:
                try:
                    doc = f'{doc[:3]}.{doc[3:6]}.{doc[6:9]}-{doc[9:11]}'
                    return doc
                except:
                    return ''
        else:
            print('erro na validação do CPF ou CNPJ')
            quit()

        
if __name__ == "__main__":
    xml  = Read_xml('C:\\Users\\ADM\\Downloads\\delete')
    all = xml.all_files()
    for i in all:
        xml.check_chave(i)

