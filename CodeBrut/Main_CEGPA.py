import math
import sys
import re
from Ui_CEGPA import Ui_CEGPA
from PyQt5.QtWidgets import QApplication, QWidget, QSizePolicy
from PyQt5.QtCore import QTimer, Qt
from HoverWigets import HoverWidget


class MainCEGPA(Ui_CEGPA, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.support = 'Avion'

        #Initialisation of the dictionnary
        self.buttons_labels = {
            self.checkBoxBase: self.lineEditBase,
            self.checkBoxRecouvLong: self.lineEditRecouvLong,
            self.checkBoxRecouvLat: self.lineEditRecouvLat,
            self.checkBoxEmpriseSolLat: self.lineEditEmpriseSolLat,
            self.checkBoxHauteurVol: self.lineEditHauteurVol,
            self.checkBoxDistInter: self.lineEditDistInter,
            self.checkBoxTailleDonnees: self.lineEditTailleDonnees,
            self.checkBoxDistMini: self.lineEditDistMini,
            self.checkBoxPrisesAxes: self.lineEditPrisesAxes,
            self.checkBoxResolTerrain: self.lineEditResolTerrain,
            self.checkBoxTailleCapteur: self.lineEditTailleCapteur,
            self.checkBoxFreqAcquisition: self.lineEditFreqAcquisition,
            self.checkBoxLongueurChantier: self.lineEditLongueurChantier,
            self.checkBoxLargeurChantier: self.lineEditLargeurChantier,
            self.checkBoxConsoKero: self.lineEditConsoKero,
            self.checkBoxNombreAxesVols: self.lineEditNombreAxesVols,
            self.checkBoxLongueurVol: self.lineEditLongueurVol,
            self.checkBoxClichesTot: self.lineEditClichesTot,
            self.checkBoxEmpriseSolLong: self.lineEditEmpriseSolLong,
            self.checkBoxHauteurMax: self.lineEditHauteurMax,
            self.checkBoxVitesseVol: self.lineEditVitesseVol,
            self.checkBoxEmissionCO2: self.lineEditEmissionCO2,
            self.checkBoxDistFocale: self.lineEditDistFocale,
            self.checkBoxBites: self.lineEditBites,
            self.checkBoxConsoAvion: self.lineEditConsoAvion,
            self.checkBoxPixCapteur: self.lineEditPixCapteur,
            self.checkBoxConsokW: self.lineEditConsokW,
            self.checkBoxConsoDrone: self.lineEditConsoDrone,
            self.checkBoxEau: self.lineEditEau,
            self.checkBoxPNY: self.lineEditPNY,
            self.checkBoxInsta: self.lineEditInsta,
            self.checkBoxMachine: self.lineEditMachine,
            self.checkBoxParisDakar: self.lineEditParisDakar
        }

        # Inversion of the dictionnary
        self.labels_buttons = {v: k for k, v in self.buttons_labels.items()}

        # Creation of the label text for each label and of the image popping when the mouse is over a label
        for label in self.buttons_labels.values():
            setattr(self, label.objectName()[8:], "")

            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            setattr(self, 'HoverLabel' + label.objectName()[8:], HoverWidget(
                "", f"Ressources/{label.objectName()[8:]}.jpeg", self))
            geomlabel = label.geometry()
            geomframe = label.parent().geometry()

            getattr(self, 'HoverLabel' + label.objectName()[8:]).setGeometry(
                geomframe.left() + geomlabel.left(),
                geomframe.top() + geomlabel.top() - int(1.5 * geomlabel.height()),
                geomlabel.width(),
                geomlabel.height()
            )

        #Initialisation of connections and variables
        self.temp_lock = []
        self.timers = {}
        self.connectButtons()
        self.connectEditLines()
        self.changeText(self.lineEditTailleCapteur)
        self.pushButtonResetGlobal.pressed.connect(self.globalReset)
        self.pushButtonReset.pressed.connect(self.reset)
        self.pushButtonCalcul.pressed.connect(self.do_calculs)
        self.radioButtonDrone.toggled.connect(self.droneButton)
        self.radioButtonAvion.toggled.connect(self.avionButton)
        self.radioButtonAvion.setChecked(True)

        self.ParamCam.setReadOnly(True)
        self.ParamBase.setReadOnly(True)
        self.ParamAvion.setReadOnly(True)
        self.ParamCliches.setReadOnly(True)
        self.ParamChantier.setReadOnly(True)
        self.ResultatConso.setReadOnly(True)

    def connectButtons(self):
        """
        Initialisation of the checkboxes
        :return:
        """
        for button, label in self.buttons_labels.items():
            button.state = 'Unlocked'
            label.state = 'Unlocked'
            button.stateChanged.connect(lambda _, b=button, l=label: self.clique_button(b, l))

    def connectEditLines(self):
        """
        Connect the changes of the text to the rest of the system
        :return:
        """
        for label in self.buttons_labels.values():
            label.textEdited.connect(self.create_text_edited_handler(label))

    def create_text_edited_handler(self, label):
        """
        Create the connection between the .connect and the method editText
        :param label: QLineEdit
        :return:
        """

        def handler(_):
            button = self.labels_buttons[label]
            self.editText(label, button)

        return handler

    def editText(self, label, button):
        """
        Change the state of the label and the button if the QLineEdit is empty or filled
        :param label: QLineEdit
        :param button: QCheckBox
        :return:
        """
        if label.text() == "":
            label.state = 'Unlocked'
            button.state = 'Unlocked'
            button.blockSignals(True)
            button.setCheckState(Qt.Unchecked)
            button.blockSignals(False)

        else:
            label.state = 'Locked'
            button.state = 'Locked'
            button.blockSignals(True)
            button.setCheckState(Qt.Checked)
            button.blockSignals(False)

    def changeText(self, label):
        """
        Change the ',' in '.'
        :param label: QLineEdit
        :return:
        """
        txt = label.text().replace(',', '.')
        label.setText(txt)

    def clique_button(self, bouton, label):
        """
        Change the state of the button and the label if the checkbox as been checked

        :param bouton: QCheckbox
        :param label: QLineEdit
        """
        self.delockTemp(self.temp_lock)
        self.temp_lock = []
        if bouton.state == 'Unlocked':
            label.state = 'Locked'
            bouton.state = 'Locked'
            bouton.blockSignals(True)
            bouton.setCheckState(Qt.Checked)
            bouton.blockSignals(False)
        else:
            label.state = 'Unlocked'
            bouton.state = 'Unlocked'
            bouton.blockSignals(True)
            bouton.setCheckState(Qt.Unchecked)
            bouton.blockSignals(False)

    def is_number(self, text):
        """
        Check if the texte is a number or not
        :param text: str
        :return: Bool
        """
        if text == "":
            return False
        else:
            pattern = r'^-?\d+(\.\d+)?$'
            return re.match(pattern, text) is not None

    def globalReset(self):
        """
        Reset all buttons and all lineEdit
        :return:
        """
        self.delockTemp(self.temp_lock)
        self.temp_lock = []
        for button, label in self.buttons_labels.items():
            button.state = 'Unlocked'
            label.state = 'Unlocked'
            label.setText('')
            button.blockSignals(True)
            button.setCheckState(Qt.Unchecked)
            button.blockSignals(False)

    def reset(self):
        """
        Reset all buttons and lineEdit that are 'Unlocked'
        :return:
        """
        self.delockTemp(self.temp_lock)
        self.temp_lock = []
        for button, label in self.buttons_labels.items():
            if label.state == 'Unlocked':
                label.setText('')

    def do_calculs(self):
        "Launch the calculation system multiple times to assure that all results possible get calculated"
        self.delockTemp(self.temp_lock)
        self.reset()
        for i in range(7):
            self.calculs()
        self.delockTemp(self.temp_lock)
        print(self.lineEditConsokW.state)

    def delockTemp(self, temp_lock):
        """
        Unlock the temporary lock that get put in place inside of self.calculs, which serve to avoid certains bugs
        :param temp_lock: List of QLineEdit
        :return:
        """
        for i in temp_lock:
            i.state = 'Unlocked'
            self.labels_buttons[i].state = 'Unlocked'

    def avionButton(self):
        """
        Change the mode to plane mode : different variables and calculations
        :return:
        """
        self.support = 'Avion'
        self.frameConsoAvion.show()
        self.frameConsoDrone.hide()
        self.frameConsoKero.show()
        self.frameConsokW.hide()
        self.frameMachine.hide()
        self.frameEau.show()
        self.HoverLabelConsoAvion.show()
        self.HoverLabelConsoDrone.hide()
        self.HoverLabelConsoKero.show()
        self.HoverLabelConsokW.hide()
        self.textBrowserMachine.hide()
        self.textBrowserEau.show()

    def droneButton(self):
        """
        Change the mode to drone mode : different variables and calculations
        :return:
        """
        self.support = 'Drone'
        self.frameConsoAvion.hide()
        self.frameConsoDrone.show()
        self.frameConsoKero.hide()
        self.frameConsokW.show()
        self.frameEau.hide()
        self.frameMachine.show()
        self.HoverLabelConsoAvion.hide()
        self.HoverLabelConsoDrone.show()
        self.HoverLabelConsoKero.hide()
        self.HoverLabelConsokW.show()
        self.textBrowserEau.hide()
        self.textBrowserMachine.show()

    def calculs(self):
        """
        Execute all the calculation after importing the sensor size in mm and in pix in a better format
        :return:
        """
        Base = self.lineEditBase.text()
        RecouvLong = self.lineEditRecouvLong.text()
        RecouvLat = self.lineEditRecouvLat.text()
        EmpriseSolLat = self.lineEditEmpriseSolLat.text()
        HauteurVol = self.lineEditHauteurVol.text()
        DistInter = self.lineEditDistInter.text()
        TailleDonnees = self.lineEditTailleDonnees.text()
        DistMini = self.lineEditDistMini.text()
        PrisesAxes = self.lineEditPrisesAxes.text()
        ResolTerrain = self.lineEditResolTerrain.text()
        FreqAcquisition = self.lineEditFreqAcquisition.text()
        LongueurChantier = self.lineEditLongueurChantier.text()
        LargeurChantier = self.lineEditLargeurChantier.text()
        TaillePhotosite = ''
        ConsoKero = self.lineEditConsoKero.text()
        NombreAxesVols = self.lineEditNombreAxesVols.text()
        LongueurVol = self.lineEditLongueurVol.text()
        ClichesTot = self.lineEditClichesTot.text()
        EmpriseSolLong = self.lineEditEmpriseSolLong.text()
        HauteurMax = self.lineEditHauteurMax.text()
        VitesseVol = self.lineEditVitesseVol.text()
        EmmissionCO2 = self.lineEditEmissionCO2.text()
        DistFocale = self.lineEditDistFocale.text()
        Bites = self.lineEditBites.text()
        ConsoAvion = self.lineEditConsoAvion.text()
        PixCapteur = self.lineEditPixCapteur.text()
        ConsoDrone = self.lineEditConsoDrone.text()
        ConsokW = self.lineEditConsokW.text()
        Eau = self.lineEditEau.text()
        ParisDakar = self.lineEditParisDakar.text()
        Insta = self.lineEditInsta.text()
        PNY = self.lineEditPNY.text()
        Machine = self.lineEditMachine.text()

        if self.lineEditTailleCapteur.text() == '':
            TailleCapteur = '  '
        else:
            parts = self.lineEditTailleCapteur.text().replace('X', 'x').replace('*', 'x').split('x')
            long = max(parts)
            larg = min(parts)
            TailleCapteur = [long, larg]

        if self.lineEditPixCapteur.text() == '':
            PixCapteur = '  '
        else:
            parts = self.lineEditPixCapteur.text().replace('X', 'x').replace('*', 'x').split('x')
            long = max(parts)
            larg = min(parts)
            PixCapteur = [long, larg]

        # To avoid division by 0
        try:
            # Taille photosites
            if self.is_number(EmpriseSolLat) and self.is_number(ResolTerrain) and self.is_number(TailleCapteur[0]):
                TaillePhotosite = (str(float(ResolTerrain) * float(TailleCapteur[0]) * 1000 / float(EmpriseSolLat)))

            if self.is_number(EmpriseSolLong) and self.is_number(ResolTerrain) and self.is_number(TailleCapteur[1]):
                TaillePhotosite = (str(float(ResolTerrain) * float(TailleCapteur[1]) * 1000 / float(EmpriseSolLong)))

            if self.is_number(TailleCapteur[0]) and self.is_number(PixCapteur[0]):
                TaillePhotosite = (str(float(TailleCapteur[0]) / float(PixCapteur[0]) * 1000))

            # Base / Baseline
            if self.lineEditBase.state == 'Unlocked':

                if self.is_number(RecouvLong) and self.is_number(EmpriseSolLong):
                    self.lineEditBase.setText(str((1 - float(RecouvLong)) * float(EmpriseSolLong)))
                    self.lineEditBase.state = 'Locked'
                    self.temp_lock.append(self.lineEditBase)

                elif self.is_number(VitesseVol) and self.is_number(FreqAcquisition):
                    self.lineEditBase.setText(str((float(VitesseVol) / 1.9438) / float(FreqAcquisition)))
                    self.lineEditBase.state = 'Locked'
                    self.temp_lock.append(self.lineEditBase)

            # Recouvrement Longitudinal / longitudinal overlap
            if self.lineEditRecouvLong.state == 'Unlocked':
                if self.is_number(Base) and self.is_number(EmpriseSolLong):
                    self.lineEditRecouvLong.setText(str(1 - (float(Base) / float(EmpriseSolLong))))
                    self.lineEditRecouvLong.state = 'Locked'
                    self.temp_lock.append(self.lineEditRecouvLong)

            # Recouvrement latéral / lateral overlap
            if self.lineEditRecouvLat.state == 'Unlocked':
                if self.is_number(DistInter) and self.is_number(EmpriseSolLat):
                    self.lineEditRecouvLat.setText(str(1 - (float(DistInter) / float(EmpriseSolLat))))
                    self.lineEditRecouvLat.state = 'Locked'
                    self.temp_lock.append(self.lineEditRecouvLat)
            # Emprise latéral / lateral footprint size
            if self.lineEditEmpriseSolLat.state == 'Unlocked':
                if self.is_number(DistInter) and self.is_number(RecouvLat):
                    self.lineEditEmpriseSolLat.setText(str(float(DistInter) / (1 - float(RecouvLat))))
                    self.lineEditEmpriseSolLat.state = 'Locked'
                    self.temp_lock.append(self.lineEditEmpriseSolLat)

                elif self.is_number(TailleCapteur[0]) and self.is_number(DistFocale) and self.is_number(HauteurVol):
                    self.lineEditEmpriseSolLat.setText(
                        str(float(HauteurVol) * float(TailleCapteur[0]) / float(DistFocale)))
                    self.lineEditEmpriseSolLat.state = 'Locked'
                    self.temp_lock.append(self.lineEditEmpriseSolLat)

                elif self.is_number(ResolTerrain) and self.is_number(TailleCapteur[0]) and self.is_number(
                        TaillePhotosite):
                    self.lineEditEmpriseSolLat.setText(
                        str(float(ResolTerrain) * float(TailleCapteur[0]) / float(TaillePhotosite) * 1000))

                    self.lineEditEmpriseSolLat.state = 'Locked'
                    self.temp_lock.append(self.lineEditEmpriseSolLat)

            # Emprise longitudinal / longitudinal footprint size
            if self.lineEditEmpriseSolLong.state == 'Unlocked':
                if self.is_number(Base) and self.is_number(RecouvLong):
                    self.lineEditEmpriseSolLong.setText(str(float(Base) / (1 - float(RecouvLong))))

                    self.lineEditEmpriseSolLong.state = 'Locked'
                    self.temp_lock.append(self.lineEditEmpriseSolLong)

                elif self.is_number(HauteurVol) and self.is_number(DistFocale) and self.is_number(TailleCapteur[1]):
                    self.lineEditEmpriseSolLong.setText(
                        str(float(HauteurVol) * float(TailleCapteur[1]) / float(DistFocale)))

                    self.lineEditEmpriseSolLong.state = 'Locked'
                    self.temp_lock.append(self.lineEditEmpriseSolLong)

                elif self.is_number(ResolTerrain) and self.is_number(TailleCapteur[1]) and self.is_number(
                        TaillePhotosite):
                    self.lineEditEmpriseSolLong.setText(
                        str(float(ResolTerrain) * float(TailleCapteur[1]) / float(TaillePhotosite) * 1000))

                    self.lineEditEmpriseSolLong.state = 'Locked'
                    self.temp_lock.append(self.lineEditEmpriseSolLong)

            # Hauteur de vol / flight height
            if self.lineEditHauteurVol.state == 'Unlocked':
                if self.is_number(ResolTerrain) and self.is_number(TaillePhotosite) and self.is_number(DistFocale):
                    self.lineEditHauteurVol.setText(
                        str(float(ResolTerrain) * float(DistFocale) / float(TaillePhotosite) * 1000))
                    self.lineEditHauteurVol.state = 'Locked'
                    self.temp_lock.append(self.lineEditHauteurVol)

            # Distance interbande / line spacing
            if self.lineEditDistInter.state == 'Unlocked':
                if self.is_number(RecouvLat) and self.is_number(EmpriseSolLat):
                    self.lineEditDistInter.setText(str((1 - float(RecouvLat)) * float(EmpriseSolLat)))
                    self.lineEditDistInter.state = 'Locked'
                    self.temp_lock.append(self.lineEditDistInter)

            # Taille des données / size of the data
            if self.lineEditTailleDonnees.state == 'Unlocked':
                if self.is_number(NombreAxesVols) and self.is_number(PrisesAxes) and self.is_number(
                        TailleCapteur[0]) and self.is_number(TailleCapteur[1]) and self.is_number(
                    TaillePhotosite) and self.is_number(Bites):
                    nombre_photos = float(NombreAxesVols) * float(PrisesAxes)

                    nombre_pixel = float(TailleCapteur[0]) * float(TailleCapteur[1]) * 1000000 / (
                            float(TaillePhotosite) ** 2)

                    poids_par_photo = nombre_pixel * float(Bites) * 4 / 8

                    self.lineEditTailleDonnees.setText(str(poids_par_photo * nombre_photos / 1024 ** 3))

                    self.lineEditTailleDonnees.state = 'Locked'
                    self.temp_lock.append(self.lineEditTailleDonnees)

            # Hauteur max des obstacles visible en stéréoscopie / maximum ground elevation visible in stereoscopy

            if self.lineEditHauteurMax.state == 'Unlocked':
                if self.is_number(Base) and self.is_number(EmpriseSolLong) and self.is_number(HauteurVol):
                    self.lineEditHauteurMax.setText(
                        str((1 - 2 * float(Base) / float(EmpriseSolLong)) * float(HauteurVol)))

                    self.lineEditHauteurMax.state = 'Locked'
                    self.temp_lock.append(self.lineEditHauteurMax)

            # Nombre de photos par axes / number of shots per axis
            if self.lineEditPrisesAxes.state == 'Unlocked':
                if self.is_number(LongueurChantier) and self.is_number(VitesseVol) and self.is_number(FreqAcquisition):
                    self.lineEditPrisesAxes.setText(
                        str(float(LongueurChantier) * float(FreqAcquisition) / (float(VitesseVol) / 1.9438)))

                    self.lineEditPrisesAxes.state = 'Locked'
                    self.temp_lock.append(self.lineEditPrisesAxes)

            # Résolution terrain / GSD
            if self.lineEditResolTerrain.state == 'Unlocked':

                if self.is_number(TaillePhotosite) and self.is_number(HauteurVol) and self.is_number(DistFocale):
                    self.lineEditResolTerrain.setText(
                        str(float(TaillePhotosite) * 0.001 * float(HauteurVol) / float(DistFocale)))

                    self.lineEditResolTerrain.state = 'Locked'
                    self.temp_lock.append(self.lineEditResolTerrain)

                elif self.is_number(TailleCapteur[0]) and self.is_number(TaillePhotosite) and self.is_number(
                        EmpriseSolLat):
                    self.lineEditResolTerrain.setText(
                        str(float(EmpriseSolLat) * float(TaillePhotosite) * 0.001 / (float(TailleCapteur[0]))))

                    self.lineEditResolTerrain.state = 'Locked'
                    self.temp_lock.append(self.lineEditResolTerrain)

                elif self.is_number(TailleCapteur[1]) and self.is_number(TaillePhotosite) and self.is_number(
                        EmpriseSolLong):
                    self.lineEditResolTerrain.setText(
                        str(float(EmpriseSolLong) * float(TaillePhotosite) * 0.001 / (float(TailleCapteur[1]))))

            # Fréquence d'acquisition / Acquisition frequency
            if self.lineEditFreqAcquisition.state == 'Unlocked':
                if self.is_number(Base) and self.is_number(VitesseVol):
                    self.lineEditFreqAcquisition.setText(str((float(VitesseVol) / 1.9438) / float(Base)))

                    self.lineEditFreqAcquisition.state = 'Locked'
                    self.temp_lock.append(self.lineEditFreqAcquisition)

                elif self.is_number(PrisesAxes) and self.is_number(LongueurChantier) and self.is_number(VitesseVol):
                    self.lineEditFreqAcquisition.setText(
                        str(float(PrisesAxes) * (float(VitesseVol) / 1.9438) / float(LongueurChantier)))

            # Longueur du chantier / lenght of the site
            if self.lineEditLongueurChantier.state == 'Unlocked':
                pass

            # Largeur du chantier / width of the site
            if self.lineEditLargeurChantier.state == 'Unlocked':
                pass

            # Consommation en Kérozène / Kerozene consumption
            if self.lineEditConsoKero.state == 'Unlocked' and self.support == 'Avion':
                if self.is_number(LongueurVol) and self.is_number(ConsoAvion):
                    self.lineEditConsoKero.setText(str(float(LongueurVol) * float(ConsoAvion) / 0.8))

                    self.lineEditConsoKero.state = 'Locked'
                    self.temp_lock.append(self.lineEditConsoKero)

                elif self.is_number(EmmissionCO2):
                    self.lineEditConsoKero.setText(str(float(EmmissionCO2) / 3.04))

                    self.lineEditConsoKero.state = 'Locked'
                    self.temp_lock.append(self.lineEditConsoKero)

            # Consommation en W / Energy consumption in W
            if self.lineEditConsokW.state == 'Unlocked' and self.support == 'Drone':
                if self.is_number(ConsoDrone) and self.is_number(LongueurVol):
                    self.lineEditConsokW.setText(str(float(ConsoDrone) * float(LongueurVol) / 1000))

                    self.lineEditConsokW.state = 'Locked'
                    self.temp_lock.append(self.lineEditConsokW)

            # Nombre d'axes de vol / Number of flight axes
            if self.lineEditNombreAxesVols.state == 'Unlocked':
                if self.is_number(LargeurChantier) and self.is_number(DistInter):
                    self.lineEditNombreAxesVols.setText(
                        str(int(math.ceil(float(LargeurChantier) / float(DistInter) - 1))))

                    self.lineEditNombreAxesVols.state = 'Locked'
                    self.temp_lock.append(self.lineEditNombreAxesVols)

            # Longueur du vol en distance / Length of the fly
            if self.lineEditDistMini.state == 'Unlocked':
                if self.is_number(LongueurChantier) and self.is_number(NombreAxesVols) and self.is_number(DistInter):
                    self.lineEditDistMini.setText(
                        str((float(NombreAxesVols) * float(LongueurChantier) + float(NombreAxesVols) * float(
                            DistInter) * math.pi / 2) / 1000))

                    self.lineEditDistMini.state = 'Locked'
                    self.temp_lock.append(self.lineEditDistMini)

            # Nombre de clichés total / Total number of shot
            if self.lineEditClichesTot.state == 'Unlocked':
                if self.is_number(PrisesAxes) and self.is_number(NombreAxesVols):
                    self.lineEditClichesTot.setText(str(int(float(PrisesAxes) * float(NombreAxesVols))))

                    self.lineEditClichesTot.state = 'Locked'
                    self.temp_lock.append(self.lineEditClichesTot)
            # Longueur minimum du vol en temps / Minimum flight duration
            if self.lineEditLongueurVol.state == 'Unlocked':
                if self.is_number(DistMini) and self.is_number(VitesseVol):
                    self.lineEditLongueurVol.setText(str(float(DistMini) / ((float(VitesseVol) / 1.9438) * 3.6)))

                    self.lineEditLongueurVol.state = 'Locked'
                    self.temp_lock.append(self.lineEditLongueurVol)

                if self.is_number(ConsoKero) and self.is_number(ConsoAvion):
                    self.lineEditLongueurVol.setText(str(float(ConsoKero) * (0.8) / float(ConsoAvion)))

                    self.lineEditLongueurVol.state = 'Locked'
                    self.temp_lock.append(self.lineEditLongueurVol)
            # Vitesse de vol / flight speed
            if self.lineEditVitesseVol.state == 'Unlocked':
                if self.is_number(LongueurVol) and self.is_number(DistMini):
                    self.lineEditVitesseVol.setText(str(1.9438 * float(DistMini) / (float(LongueurVol) * 3600)))

                    self.lineEditVitesseVol.state = 'Locked'
                    self.temp_lock.append(self.lineEditVitesseVol)

                elif self.is_number(Base) and self.is_number(FreqAcquisition):
                    self.lineEditVitesseVol.setText(str(float(Base) * float(FreqAcquisition) * 1.9438))

                    self.lineEditVitesseVol.state = 'Locked'
                    self.temp_lock.append(self.lineEditVitesseVol)
            # Emission de CO2 / CO2 emissions
            if self.lineEditEmissionCO2.state == 'Unlocked':
                if self.is_number(ConsoKero):
                    self.lineEditEmissionCO2.setText(str(float(ConsoKero) * 3.04))
            # Distance focale / Focal length
            if self.lineEditDistFocale.state == 'Unlocked':
                if self.is_number(EmpriseSolLong) and self.is_number(TailleCapteur[0]) and self.is_number(HauteurVol):
                    self.lineEditDistFocale.setText(
                        str(float(HauteurVol) * float(TailleCapteur[1]) / float(EmpriseSolLong)))

                    self.lineEditDistFocale.state = 'Locked'
                    self.temp_lock.append(self.lineEditDistFocale)

                elif self.is_number(EmpriseSolLat) and self.is_number(TailleCapteur[1]) and self.is_number(HauteurVol):
                    self.lineEditDistFocale.setText(
                        str(float(HauteurVol) * float(TailleCapteur[0]) / float(EmpriseSolLat)))

                    self.lineEditDistFocale.state = 'Locked'
                    self.temp_lock.append(self.lineEditDistFocale)

                elif self.is_number(HauteurVol) and self.is_number(TaillePhotosite) and self.is_number(ResolTerrain):
                    self.lineEditDistFocale.setText(
                        str(float(TaillePhotosite) * float(HauteurVol) * 0.001 / float(ResolTerrain)))

                    self.lineEditDistFocale.state = 'Locked'
                    self.temp_lock.append(self.lineEditDistFocale)

            # Encoage de l'image en bits / Image encoding in bit
            if self.lineEditBites.state == 'Unlocked':
                pass

            # Consommation de l'avion / Airplane consumption
            if self.lineEditConsoAvion.state == 'Unlocked' and self.support == 'Avion':
                if self.is_number(ConsoKero) and self.is_number(LongueurVol):
                    self.lineEditConsoAvion.setText(str(float(ConsoKero) * (0.8) / (float(LongueurVol))))

                    self.lineEditConsoAvion.state = 'Locked'
                    self.temp_lock.append(self.lineEditConsoAvion)

            # Consommation du drone / Drone consumption
            if self.lineEditConsoDrone.state == 'Unlocked' and self.support == 'Drone':
                if self.is_number(LongueurVol) and self.is_number(ConsokW):
                    self.lineEditConsoDrone.setText(str(float(ConsokW) * 1000 / float(LongueurVol)))

                    self.lineEditConsoDrone.state = 'Locked'
                    self.temp_lock.append(self.lineEditConsoDrone)

            # Nombres de pixels / Number of pixels
            if self.lineEditPixCapteur.state == 'Unlocked':
                if self.is_number(TailleCapteur[0]) and self.is_number(TailleCapteur[1]) and self.is_number(
                        TaillePhotosite):
                    self.lineEditPixCapteur.setText(
                        str(math.ceil(float(TailleCapteur[0]) / float(TaillePhotosite) * 1000)) + 'x' + str(
                            math.ceil(float(TailleCapteur[1]) / float(TaillePhotosite) * 1000)))

                    self.lineEditPixCapteur.state = 'Locked'
                    self.temp_lock.append(self.lineEditPixCapteur)

            # Nombre de douches / Number of shower
            if self.lineEditEau.state == 'Unlocked':
                if self.is_number(ConsoKero):
                    self.lineEditEau.setText(str(round(float(ConsoKero) / 50, 2)))

            # Distance Paris Dakar
            if self.lineEditParisDakar.state == 'Unlocked':
                if self.is_number(DistMini):
                    self.lineEditParisDakar.setText(str(float(DistMini) / 4196))

            # Cycles de machines à laver / Washing machine cycles
            if self.lineEditMachine.state == 'Unlocked':
                if self.is_number(ConsokW):
                    self.lineEditMachine.setText(str(round(float(ConsokW) / 0.64, 2)))

            # Paris New-York
            if self.lineEditPNY.state == 'Unlocked':
                if self.is_number(EmmissionCO2):
                    self.lineEditPNY.setText(str(float(EmmissionCO2) / 17500))

            # Reels Instagram
            if self.lineEditInsta.state == 'Unlocked':
                if self.is_number(TailleDonnees):
                    self.lineEditInsta.setText(str(round(float(TailleDonnees) / (14 / 1024), 2)))

        except ZeroDivisionError:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainCEGPA()
    window.show()
    sys.exit(app.exec_())
