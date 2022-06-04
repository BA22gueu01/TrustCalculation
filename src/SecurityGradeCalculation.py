import ApparmorCheck
import CertificateCheck
import VulnerabilityScanCheck


class SecurityGradeCalculation:

    def __init__(self):
        self.apparmorGrade = 0
        self.apparmorWeight = 0.2
        self.certificateGrade = 0
        self.certificateWeight = 0.3
        self.vulnerabilityScanGrade = 0
        self.vulnerabilityScanWeight = 0.5
        self.vulnerabilityScan = VulnerabilityScanCheck.VulnerabilityScan()

    def calculateGrade(self):
        return self.apparmorWeight * self.apparmorGrade + self.certificateWeight * self.certificateGrade + self.vulnerabilityScanWeight * self.vulnerabilityScanGrade

    def getAppArmorGrade(self):
        return self.apparmorGrade

    def getCertificateGrade(self):
        return self.certificateGrade

    def getVulnerabilityScanGrade(self):
        return self.vulnerabilityScanGrade

    def getNiktoCheckGrade(self, list):
        return self.vulnerabilityScan.getNiktoCheckGrade(list)

    def getSsllabsCheckGrade(self, list):
        return self.vulnerabilityScan.getSsllabsCheckGrade(list)

    def getHttpobsCheckGrade(self, list):
        return self.vulnerabilityScan.getHttpobsCheckGrade(list)


    def calculateVulnerabilityScanGrade(self):
        self.vulnerabilityScanGrade = self.vulnerabilityScan.getVulnerabilityScanGrade()
        print("VulnerabilityScanGrade: ", self.vulnerabilityScanGrade)

    def calculateApparmorGrade(self):
        apparmorCheck = ApparmorCheck.ApparmorCheck()
        self.apparmorGrade = apparmorCheck.getApparmorGrade()
        print("ApparmorGrade: ", self.apparmorGrade)

    def calculateCertificateGrade(self):
        certificateCheck = CertificateCheck.CertificateCheck("zhaw.ch", "443")
        self.certificateGrade = certificateCheck.checkCertificate()
        print("CertificateGrade: ", self.certificateGrade)

    def dailyUpdate(self):
        self.calculateCertificateGrade()
        self.calculateApparmorGrade()
        self.calculateVulnerabilityScanGrade()

    def initialCalculation(self):
        self.calculateCertificateGrade()
        self.calculateApparmorGrade()
        self.calculateVulnerabilityScanGrade()
