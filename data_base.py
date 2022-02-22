import sqlite3

class DataBase():
    def __init__(self, name = 'system_db.db') -> None:
        self.name = name
    
    def conecta(self):
        self.connection = sqlite3.connect(self.name)

    def close_conection(self):
        try:
            self.connection.close()
        except:
            pass

    def create_table_users(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                user TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                access TEXT NOT NULL
                );
            """)
        except AttributeError:
            print('Faça conexão')

    def insert_user(self, name, user, password, acess):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO users(name, user, password, acess) VALUES(?,?,?,?)
            """,(name, user, password, acess))
            self.connection.commit()
            
        except:
            print('Erro ao criar novo usuário: ')

    def check_user(self, user, password):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
            SELECT * FROM users;
            """)
            for linha in cursor.fetchall():
                if linha[2].upper() == user.upper() and linha[3] == password and linha[4] == 'Administrador':
                    return 'Administrador'

                elif linha[2].upper() == user.upper() and linha[3] == password and linha[4] == 'Demais':
                    return 'Demais'

                else:
                    continue
            return 'Usuário sem acesso'
        except:
            pass


    def create_table_nfe(self):
        cursor = self.connection.cursor()
        cursor.execute(f""" 
        CREATE TABLE IF NOT EXISTS notas(

        chave TEXT UNIQUE NOT NULL,
        nat_op TEXT,
        mod TEXT,
        nfe TEXT,
        serie TEXT,
        data_emissao TEXT,
        data_saient TEXT,
        tp_nf TEXT,
        cod_mun_fg TEXT,
        id_dest TEXT,
        tp_imp TEXT,
        tp_emi TEXT,
        tp_amb TEXT,
        fin_nfe TEXT,
        ind_pres TEXT,
        nf_ref TEXT,
        doc_emit TEXT,
        nome_emit TEXT,
        fantasia_emit TEXT,
        rua_emit TEXT,
        nro_emit TEXT,
        bairro_emit TEXT,
        cod_mun_emit TEXT,
        mun_emit TEXT,
        uf_emit TEXT,
        cep_emit TEXT,
        cod_pais_emit TEXT,
        pais_emit TEXT,
        fone_emit TEXT,
        ie_emit TEXT,
        cnae_fiscal TEXT,
        crt_emit TEXT,
        cnpj_avulsa TEXT,
        nome_avulsa TEXT,
        doc_dest TEXT,
        nome_dest TEXT,
        rua_dest TEXT,
        nro_dest TEXT,
        cpl_dest TEXT,
        bairro_dest TEXT,
        cod_mun_dest TEXT,
        mun_dest TEXT,
        uf_dest TEXT,
        cep_dest TEXT,
        cod_pais_dest TEXT,
        pais_dest TEXT,
        fone_dest TEXT,
        sit_ie_dest TEXT,
        ie_dest TEXT,
        isuf_dest TEXT,
        im_dest TEXT,
        email_dest TEXT,
        doc_retirada TEXT,
        nome_retirada TEXT,
        rua_retirada TEXT,
        nro_retirada TEXT,
        cpl_retirada TEXT,
        bairro_retirada TEXT,
        cod_mun_retirada TEXT,
        mun_retirada TEXT,
        uf_retirada TEXT,
        cep_retirada TEXT,
        cod_pais_retirada TEXT,
        pais_retirada TEXT,
        fone_retirada TEXT,
        email_retirada TEXT,
        ie_retirada TEXT,
        doc_entrega TEXT,
        nome_entrega TEXT,
        rua_entrega TEXT,
        nro_entrega TEXT,
        cpl_entrega TEXT,
        bairro_entrega TEXT,
        cod_mun_entrega TEXT,
        mun_entrega TEXT,
        uf_entrega TEXT,
        cep_entrega TEXT,
        cod_pais_entrega TEXT,
        pais_entrega TEXT,
        fone_entrega TEXT,
        email_entrega TEXT,
        ie_entrega TEXT,
        t_bc_icms TEXT,
        t_v_icms TEXT,
        t_v_deso TEXT,
        pcfufdest TEXT,
        icmsufdest TEXT,
        icmsufremet TEXT,
        t_fcp TEXT,
        t_bcst TEXT,
        t_st TEXT,
        t_fcpst TEXT,
        t_fcpst_ret TEXT,
        t_vprod TEXT,
        t_vfrete TEXT,
        t_vseguro TEXT,
        t_vdesc TEXT,
        t_vii TEXT,
        t_vipi TEXT,
        t_vpis TEXT,
        t_vcofins TEXT,
        t_voutro TEXT,
        t_nf TEXT,
        t_trib TEXT,
        modfrete TEXT,
        doc_trans TEXT,
        nome_trans TEXT,
        ie_trans TEXT,
        ender_trans TEXT,
        mun_trans TEXT,
        uf_trans TEXT,
        data_importacao TEXT,
        usuario TEXT,
        PRIMARY KEY(chave)
        );

        """)        

    def create_table_nfe_produtos(self):
        cursor = self.connection.cursor()
        cursor.execute(f""" 
        CREATE TABLE IF NOT EXISTS produtos(
            chave TEXT,
            cod_item TEXT,
            c_ean TEXT,
            c_barra TEXT,
            descricao_item TEXT,
            ncm TEXT,
            nve TEXT,
            cest TEXT,
            cfop TEXT,
            un_medida TEXT,
            qtd_item TEXT,
            vlr_unit_item TEXT,
            vlr_item TEXT,
            ind_escala TEXT,
            cnpj_fab TEXT,
            c_benef TEXT,
            ex_tipi TEXT,
            u_trib TEXT,
            q_trib TEXT,
            v_un_trib TEXT,
            v_frete TEXT,
            v_seg TEXT,
            v_desc TEXT,
            v_outro TEXT,
            ind_tot TEXT,
            orig TEXT,
            cst_csosn TEXT,
            orig_part TEXT,
            cst_part TEXT,
            mod_bc TEXT,
            v_bc TEXT,
            red_bc TEXT,
            icms_part TEXT,
            v_icms_part TEXT,
            mod_bcst TEXT,
            mva_st_part TEXT,
            red_bc_st TEXT,
            bc_st_part TEXT,
            icms_st TEXT,
            pBCOp TEXT,
            uf_st TEXT,
            orig_st TEXT,
            cst_st TEXT,
            bc_st_ret TEXT,
            st TEXT,
            v_st TEXT,
            v_st_ret TEXT,
            v_bcfcpst_ret TEXT,
            p_fcpst_ret TEXT,
            v_fcpst_ret TEXT,
            v_bcst_dest TEXT,
            v_icms_st_dest TEXT,
            p_redbcefet TEXT,
            v_bcefet TEXT,
            p_icms_efet TEXT,
            v_icms_efet TEXT,
            cst_ipi TEXT,
            bc_ipi TEXT,
            p_ipi TEXT,
            q_unid_ipi TEXT,
            v_unid_ipi TEXT,
            v_ipi TEXT,
            cst_int TEXT,
            v_bc_ii TEXT,
            v_desp_adu TEXT,
            v_ii TEXT,
            v_iof TEXT,
            v_bc_iss TEXT,
            alq_iss TEXT,
            v_iss TEXT,
            c_mun_fg_iss TEXT,
            c_serv TEXT,
            v_deducao TEXT,
            v_outro_iss TEXT,
            v_desc_inc TEXT,
            v_desc_cond TEXT,
            v_iss_ret TEXT,
            ind_iss TEXT,
            c_servico TEXT,
            c_mun TEXT,
            c_pais TEXT,
            n_processo TEXT,
            ind_incentivo TEXT,
            cst_pis TEXT,
            v_bc_pis TEXT,
            p_pis TEXT,
            v_pis TEXT,
            cst_COFINS TEXT,
            v_bc_COFINS TEXT,
            p_COFINS TEXT,
            v_COFINS TEXT,
            data_importacao TEXT,
            usuario TEXT
            );
            """
)
    def create_table_nfe_faturamento(self):
        cursor = self.connection.cursor()
        cursor.execute(f""" 
        CREATE TABLE IF NOT EXISTS faturamento(
        chave TEXT,
        fat TEXT,
        v_orig TEXT,
        v_desc TEXT,
        v_liq TEXT,
        data_importacao TEXT,
        usuario TEXT
        );
        """
        )

    def create_table_nfe_duplicata(self):
        cursor = self.connection.cursor()
        cursor.execute(f""" 
        CREATE TABLE IF NOT EXISTS duplicata(
        chave TEXT,
        ndup TEXT,
        dvenc TEXT,
        vdup TEXT,
        data_importacao TEXT,
        usuario TEXT
        );
        """
        )

    def insert_nfe(self, *args):

        var_nfe_list = ('chave', 'nat_op', 'mod', 'nfe', 'serie', 'data_emissao', 'data_saient', 'tp_nf', 'cod_mun_fg', 'id_dest', 'tp_imp', 'tp_emi', 'tp_amb', 'fin_nfe', 'ind_pres', 
            'nf_ref', 'doc_emit', 'nome_emit', 'fantasia_emit', 'rua_emit', 'nro_emit', 'bairro_emit', 'cod_mun_emit', 'mun_emit', 'uf_emit', 'cep_emit', 'cod_pais_emit', 'pais_emit', 
            'fone_emit', 'ie_emit', 'cnae_fiscal', 'crt_emit', 'cnpj_avulsa', 'nome_avulsa', 'doc_dest', 'nome_dest', 'rua_dest', 'nro_dest', 'cpl_dest', 'bairro_dest', 'cod_mun_dest', 
            'mun_dest', 'uf_dest', 'cep_dest', 'cod_pais_dest', 'pais_dest', 'fone_dest', 'sit_ie_dest', 'ie_dest', 'isuf_dest', 'im_dest', 'email_dest', 'doc_retirada', 'nome_retirada', 
            'rua_retirada', 'nro_retirada', 'cpl_retirada', 'bairro_retirada', 'cod_mun_retirada', 'mun_retirada', 'uf_retirada', 'cep_retirada', 'cod_pais_retirada', 'pais_retirada', 
            'fone_retirada', 'email_retirada', 'ie_retirada', 'doc_entrega', 'nome_entrega', 'rua_entrega', 'nro_entrega', 'cpl_entrega', 'bairro_entrega', 'cod_mun_entrega', 'mun_entrega', 
            'uf_entrega', 'cep_entrega', 'cod_pais_entrega', 'pais_entrega', 'fone_entrega', 'email_entrega', 'ie_entrega', 't_bc_icms', 't_v_icms', 't_v_deso', 'pcfufdest', 'icmsufdest', 
            'icmsufremet', 't_fcp', 't_bcst', 't_st', 't_fcpst', 't_fcpst_ret', 't_vprod', 't_vfrete', 't_vseguro', 't_vdesc', 't_vii', 't_vipi', 't_vpis', 't_vcofins', 't_voutro', 't_nf', 
            't_trib', 'modfrete', 'doc_trans', 'nome_trans', 'ie_trans', 'ender_trans', 'mun_trans', 'uf_trans', 'data_importacao', 'usuario')

        qtd = ','.join(map(str, '?'*113))

        query = f"""INSERT INTO notas{var_nfe_list} VALUES({qtd})"""

        try:
            cursor = self.connection.cursor()
            cursor.execute(query ,(args))
            self.connection.commit()
            
        except:
            print('Erro ao inserir nota')

    def insert_nfe_produto(self, *args):

        var_prod_str = ('chave', 'cod_item', 'c_ean', 'c_barra', 'descricao_item', 'ncm', 'nve', 'cest', 'cfop', 'un_medida', 'qtd_item', 'vlr_unit_item', 'vlr_item', 
            'ind_escala', 'cnpj_fab', 'c_benef', 'ex_tipi', 'u_trib', 'q_trib', 'v_un_trib', 'v_frete', 'v_seg', 'v_desc', 'v_outro', 'ind_tot', 'orig', 'cst_csosn', 'orig_part', 
            'cst_part', 'mod_bc', 'v_bc', 'red_bc', 'icms_part', 'v_icms_part', 'mod_bcst', 'mva_st_part', 'red_bc_st', 'bc_st_part', 'icms_st', 'pBCOp', 'uf_st', 'orig_st', 'cst_st', 
            'bc_st_ret', 'st', 'v_st', 'v_st_ret', 'v_bcfcpst_ret', 'p_fcpst_ret', 'v_fcpst_ret', 'v_bcst_dest', 'v_icms_st_dest', 'p_redbcefet', 'v_bcefet', 'p_icms_efet', 'v_icms_efet', 
            'cst_ipi', 'bc_ipi', 'p_ipi', 'q_unid_ipi', 'v_unid_ipi', 'v_ipi', 'cst_int', 'v_bc_ii', 'v_desp_adu', 'v_ii', 'v_iof', 'v_bc_iss', 'alq_iss', 'v_iss', 'c_mun_fg_iss', 'c_serv', 
            'v_deducao', 'v_outro', 'v_desc_inc', 'v_desc_cond', 'v_iss_ret', 'ind_iss', 'c_servico', 'c_mun', 'c_pais', 'n_processo', 'ind_incentivo', 'cst_pis', 'v_bc_pis', 'p_pis', 'v_pis', 
            'cst_COFINS', 'v_bc_COFINS', 'p_COFINS', 'v_COFINS', 'data_importacao', 'usuario')


        qtd_prod = ','.join(map(str, '?'*93))

        query = f"""INSERT INTO produtos{var_prod_str} VALUES({qtd_prod})"""

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, args)
            self.connection.commit()
            
        except AttributeError:
            print('Erro ao importar produtos')

    def insert_nfe_faturamento(self, chave, fat, v_orig, v_desc, v_liq, data_importacao, usuario):

        var_funcao = (chave, fat, v_orig, v_desc, v_liq, data_importacao, usuario)
        var_funcao_str = ('chave', 'fat', 'v_orig', 'v_desc', 'v_liq', 'data_importacao', 'usuario')
        qtd = ','.join(map(str, '?'*7)) #usa-se este modo pois simples '?,'*7 finaliza com o ultimo '?' com virgula aí dá erro
        query = f"""INSERT INTO faturamento{var_funcao_str}VALUES({qtd})"""

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, var_funcao)
            self.connection.commit()

        except:
            print('Erro ao inserir a nota no banco de dados')


    def insert_nfe_duplicata(self, chave, ndup, dvenc, vdup, data_importacao, usuario):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO duplicata(chave, ndup, dvenc, vdup, data_importacao, usuario) VALUES(?, ?, ?, ?, ?, ?)
            """,(chave, ndup, dvenc, vdup, data_importacao, usuario))
            self.connection.commit()
            
        except AttributeError:
            print('Erro ao inserir as duplicatas')
    
    def lista_produtos(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM produtos')
            rows = cursor.fetchall()#Armazena os dados lidos na linha anterior
            return rows
        except:
            print('erro ao listar Notas')

    def check_nota(self, chave):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""SELECT * FROM notas WHERE chave = '{chave}'""")
            cont = cursor.fetchall()
            if cont[0][0] == chave:
                return 'Existe'
            else:
                return 'Não existe'

        except:
            return 'Não existe'


if __name__ == '__main__':

    db = DataBase()
    db.conecta()
    if db.check_nota('11220110486453000123550010000007891235243511') == 'Existe':
        print('conectiou')
    #db.insert_user('cadu', 'cadu', '123', 'Demais')
    #db.insert_nfe_faturamento('54559','559fat', '5', '2', '3', '05/01/2022', 'bbruno')
    # db.insert_nfe_produto('chaveteste', 'cod_itemteste', 'c_eanteste', 'c_barrateste', 'descricao_itemteste', 'ncmteste', 'nveteste', 'cestteste', 'cfopteste', 'un_medidateste', 'qtd_itemteste', 'vlr_unit_itemteste', 'vlr_itemteste', 
    #     'ind_escalateste', 'cnpj_fabteste', 'c_benefteste', 'ex_tipiteste', 'u_tribteste', 'q_tribteste', 'v_un_tribteste', 'v_freteteste', 'v_segteste', 'v_descteste', 'v_outroteste', 'ind_totteste', 'origteste', 'cst_csosnteste', 'orig_partteste', 
    #     'cst_partteste', 'mod_bcteste', 'v_bcteste', 'red_bcteste', 'icms_partteste', 'v_icms_partteste', 'mod_bcstteste', 'mva_st_partteste', 'red_bc_stteste', 'bc_st_partteste', 'icms_stteste', 'pBCOpteste', 'uf_stteste', 'orig_stteste', 'cst_stteste', 
    #     'bc_st_retteste', 'stteste', 'v_stteste', 'v_st_retteste', 'v_bcfcpst_retteste', 'p_fcpst_retteste', 'v_fcpst_retteste', 'v_bcst_destteste', 'v_icms_st_destteste', 'p_redbcefetteste', 'v_bcefetteste', 'p_icms_efetteste', 'v_icms_efetteste', 
    #     'cst_ipiteste', 'bc_ipiteste', 'p_ipiteste', 'q_unid_ipiteste', 'v_unid_ipiteste', 'v_ipiteste', 'cst_intteste', 'v_bc_iiteste', 'v_desp_aduteste', 'v_iiteste', 'v_iofteste', 'v_bc_issteste', 'alq_issteste', 'v_issteste', 'c_mun_fg_issteste', 'c_servteste', 
    #     'v_deducaoteste', 'v_outroteste', 'v_desc_incteste', 'v_desc_condteste', 'v_iss_retteste', 'ind_issteste', 'c_servicoteste', 'c_munteste', 'c_paisteste', 'n_processoteste', 'ind_incentivoteste', 'cst_pisteste', 'v_bc_pisteste', 'p_pisteste', 'v_pisteste', 
    #     'cst_COFINSteste', 'v_bc_COFINSteste', 'p_COFINSteste', 'v_COFINSteste', 'data_importacaoteste', 'usuarioteste')
    #db.insert_nfe('chaveteste2', 'nat_opteste', 'modteste', 'nfeteste', 'serieteste', 'teste', 'data_emissaoteste', 'teste', 'data_saientteste', 'tp_nfteste', 'cod_mun_fgteste', 'id_destteste', 'tp_impteste', 'tp_emiteste', 'tp_ambteste', 'fin_nfeteste', 'ind_presteste', 'nf_refteste', 'doc_emit teste', 'nome_emitteste', 'fantasia_emitteste', 'rua_emitteste', 'nro_emitteste', 'bairro_emitteste', 'cod_mun_emitteste', 'mun_emitteste', 'uf_emitteste', 'cep_emitteste', 'cod_pais_emitteste', 'pais_emitteste', 'fone_emitteste', 'ie_emitteste', 'cnae_fiscalteste', 'crt_emitteste', 'cnpj_avulsateste', 'nome_avulsateste', 'doc_dest teste', 'nome_destteste', 'rua_destteste', 'nro_destteste', 'cpl_destteste', 'bairro_destteste', 'cod_mun_destteste', 'mun_destteste', 'uf_destteste', 'cep_destteste', 'cod_pais_destteste', 'pais_destteste', 'fone_destteste', 'sit_ie_destteste', 'ie_destteste', 'isuf_destteste', 'im_destteste', 'email_destteste', 'doc_retirada teste', 'nome_retiradateste', 'rua_retiradateste', 'nro_retiradateste', 'cpl_retiradateste', 'bairro_retiradateste', 'cod_mun_retiradateste', 'mun_retiradateste', 'uf_retiradateste', 'cep_retiradateste', 'cod_pais_retiradateste', 'pais_retiradateste', 'fone_retiradateste', 'email_retiradateste', 'ie_retiradateste', 'doc_entregateste', 'nome_entregateste', 'rua_entregateste', 'nro_entregateste', 'cpl_entregateste', 'bairro_entregateste', 'cod_mun_entregateste', 'mun_entregateste', 'uf_entregateste', 'cep_entregateste', 'cod_pais_entregateste', 'pais_entregateste', 'fone_entregateste', 'email_entregateste', 'ie_entregateste', 't_bc_icmsteste', 't_v_icmsteste', 't_v_desoteste', 'pcfufdestteste', 'icmsufdestteste', 'icmsufremetteste', 't_fcpteste', 't_bcstteste', 't_stteste', 't_fcpstteste', 't_fcpst_retteste', 't_vprodteste', 't_vfreteteste', 't_vseguroteste', 't_vdescteste', 't_viiteste', 't_vipiteste', 't_vpisteste', 't_vcofinsteste', 't_voutroteste', 't_nfteste', 't_tribteste', 'modfreteteste', 'doc_transteste', 'nome_transteste', 'ie_transteste', 'ender_transteste', 'mun_transteste', 'brunotteste')
    db.close_conection()

    # DataBase().conecta()
    # DataBase().insert_user('ellen', 'ellen', '123', 'Demais')
    # DataBase().close_conection()
#     db = DataBase()
#     db.conecta()
#     db.create_table_nfe()
#     db.create_table_nfe_produtos()
#     db.create_table_nfe_faturamento()
#     db.create_table_nfe_duplicata()
#     db.close_conection()
