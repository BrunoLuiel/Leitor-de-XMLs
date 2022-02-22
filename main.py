from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog
import sys
from data_base import DataBase
from XML_files import Read_xml


class Janela(QMainWindow):
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        self.tela = uic.loadUi('login.ui')
        self.tela_main = uic.loadUi('main.ui')
        self.tela.btnLogin.clicked.connect(lambda: self.check_login())
        self.tela.show()
        app.exec_()
        



    def carrega_janela(self, screen):
        screen.show()

    def check_login(self):
        self.userss = DataBase()
        self.userss.conecta()
        autenticado = self.userss.check_user(self.tela.lineUser.text().upper(), self.tela.linePassword.text())


        if autenticado.lower() == 'administrador' or autenticado.lower() == 'demais':
            self.w = MainWindow(autenticado.lower())
            #self.w.show()
            self.tela.close()
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Erro de acesso')
            msg.setText('Usuário ou senha incorreta')
            msg.exec()


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        # self.setWindowTitle('Sistema de Gerenciamento')
        self.tela_main = uic.loadUi('main.ui')
        self.tela_main.show()
        self.tela_main.btnAtualizaProdutos.clicked.connect(lambda: self.atualiza_tabela())



 

        if user.lower() == 'demais':
            self.tela_main.btn_cadastrar.setVisible(False)
            self.tela_main.pushButton_6.setVisible(False)
    
        #Buttons to transfer to other screens
        self.tela_main.btn_home.clicked.connect(lambda: self.tela_main.Pages.setCurrentWidget(self.tela_main.pg_home))
        self.tela_main.btn_importar.clicked.connect(lambda: self.tela_main.Pages.setCurrentWidget(self.tela_main.pg_Importa))
        self.tela_main.btn_tabelas.clicked.connect(lambda: self.tela_main.Pages.setCurrentWidget(self.tela_main.pg_table))
        self.tela_main.btn_cadastrar.clicked.connect(lambda: self.tela_main.Pages.setCurrentWidget(self.tela_main.pg_cad_user))
        self.tela_main.btn_contato.clicked.connect(lambda: self.tela_main.Pages.setCurrentWidget(self.tela_main.pg_contato))
        self.tela_main.btn_sobre.clicked.connect(lambda: self.tela_main.Pages.setCurrentWidget(self.tela_main.pg_sobre))

        #Register user button
        self.tela_main.pushButton_6.clicked.connect(self.subscribe_user)

        #XML files
        self.tela_main.pushButton.clicked.connect(self.open_path)
        self.tela_main.btn_importar_2.clicked.connect(self.import_xml)

    def subscribe_user(self):
        if self.tela_main.input_senha.text() != self.tela_main.inp_confsenha.text():
            msg = QMessageBox()
            msg.setWindowTitle('Senha incorreta!')
            msg.setText('A senha digitada não confere!')
            msg.exec_()
            return None
        
        nome = self.tela_main.input_nome.text()
        user = self.tela_main.input_usuario.text()
        password = self.tela_main.input_senha.text()
        acess = self.tela_main.comboBox.currentText()

        db = DataBase()
        db.conecta()
        db.insert_user(nome, user, password, acess)
        db.close_conection()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Cadastro de usuário')
        msg.setText('Cadastro realizado com sucesso!')
        msg.exec_()
        
        self.tela_main.input_nome.setText('')
        self.tela_main.input_usuario.setText('')
        self.tela_main.input_senha.setText('')
        self.tela_main.inp_confsenha.setText('')

    def atualiza_tabela(self):
        self.db = DataBase()
        self.db.conecta()

        #Inserindo dados na tabela
        rows = self.db.lista_produtos()

        self.tela_main.tableWidget.setRowCount(len(self.db.lista_produtos()))
        self.tela_main.tableWidget.setColumnCount(len(self.db.lista_produtos()[0]))
        self.tela_main.tableWidget.setHorizontalHeaderLabels(['chaveTEXT', 'cod_itemTEXT', 'c_eanTEXT', 'c_barraTEXT', 'descricao_itemTEXT', 'ncmTEXT', 'nveTEXT', 'cestTEXT', 'cfopTEXT', 'un_medidaTEXT', 'qtd_itemTEXT', 'vlr_unit_itemTEXT', 'vlr_itemTEXT', 'ind_escalaTEXT', 'cnpj_fabTEXT', 'c_benefTEXT', 'ex_tipiTEXT', 'u_tribTEXT', 'q_tribTEXT', 'v_un_tribTEXT', 'v_freteTEXT', 'v_segTEXT', 'v_descTEXT', 'v_outroTEXT', 'ind_totTEXT', 'origTEXT', 'cst_csosnTEXT', 'orig_partTEXT', 'cst_partTEXT', 'mod_bcTEXT', 'v_bcTEXT', 'red_bcTEXT', 'icms_partTEXT', 'v_icms_partTEXT', 'mod_bcstTEXT', 'mva_st_partTEXT', 'red_bc_stTEXT', 'bc_st_partTEXT', 'icms_stTEXT', 'pBCOpTEXT', 'uf_stTEXT', 'orig_stTEXT', 'cst_stTEXT', 'bc_st_retTEXT', 'stTEXT', 'v_stTEXT', 'v_st_retTEXT', 'v_bcfcpst_retTEXT', 'p_fcpst_retTEXT', 'v_fcpst_retTEXT', 'v_bcst_destTEXT', 'v_icms_st_destTEXT', 'p_redbcefetTEXT', 'v_bcefetTEXT', 'p_icms_efetTEXT', 'v_icms_efetTEXT', 'cst_ipiTEXT', 'bc_ipiTEXT', 'p_ipiTEXT', 'q_unid_ipiTEXT', 'v_unid_ipiTEXT', 'v_ipiTEXT', 'cst_intTEXT', 'v_bc_iiTEXT', 'v_desp_aduTEXT', 'v_iiTEXT', 'v_iofTEXT', 'v_bc_issTEXT', 'alq_issTEXT', 'v_issTEXT', 'c_mun_fg_issTEXT', 'c_servTEXT', 'v_deducaoTEXT', 'v_outro_issTEXT', 'v_desc_incTEXT', 'v_desc_condTEXT', 'v_iss_retTEXT', 'ind_issTEXT', 'c_servicoTEXT', 'c_munTEXT', 'c_paisTEXT', 'n_processoTEXT', 'ind_incentivoTEXT', 'cst_pisTEXT', 'v_bc_pisTEXT', 'p_pisTEXT', 'v_pisTEXT', 'cst_COFINSTEXT', 'v_bc_COFINSTEXT', 'p_COFINSTEXT', 'v_COFINSTEXT', 'data_importacaoTEXT', 'usuarioTEX'])



        for L in range(len(rows)): #Linha
            for C in range(len(rows[0])): #Coluna
                item = QtWidgets.QTableWidgetItem(f'{rows[L][C]}')
                self.tela_main.tableWidget.setItem(L, C, item)

        self.db.close_conection()
    
    def open_path(self):
        self.path = QFileDialog.getExistingDirectory(self, str('Open Directory'), '\home', QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.tela_main.txt_file.setText(self.path)

    def import_xml(self):
        xml = Read_xml(self.tela_main.txt_file.text())
        all = xml.all_files()
        self.tela_main.progressBar.setMaximum(len(all))
        
        cont = 1

        for i in all:
            self.tela_main.progressBar.setValue(cont)
            cont+=1
            try:
                xml.check_chave(i)

            except:
                print('Erro ao importar o arquivo ' + i)
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Operação finalizada')
        msg.setText('Operação finalizada!')
        msg.exec_()
            


L = Janela()
