class motor:
    def __init__(self, free_speed, stall_torque, stall_current, free_current, power, name):
        self.free_speed = free_speed
        self.stall_torque = stall_torque
        self.stall_current = stall_current
        self.free_current = free_current
        self.power = power
        self.name = name

CIM = motor(5330, 2.41, 131.00, 2.70, 336.29, "CIM")
MINI_CIM = motor(5840, 1.41, 89.00, 3.00, 215.58, "Mini CIM")
BAG = motor(13180, 0.43, 53.00, 1.80, 148.37, "BAG")
PRO775 = motor(18730, 0.71, 134.00, 0.70, 348.15, "775 Pro")
AM775 = motor(5800, 0.28, 18.00, 1.60, 42.52, "AM 775")
AM9015 = motor(14720, 0.36, 71, 3.7, 134.49, "AM 9015")
CIMAND1MINICIM = motor(5508, 3.82, 220, 8.16, 550.84, "1 CIM and 1 Mini CIM")
CIMAND2MINICIM = motor(5593, 5.23, 309, 9.62, 765.80, "1 CIM and 2 Mini CIMS")
MINICIMAND2CIM = motor(5437, 6.23, 351, 9.15, 886.78, "1 Mini CIM and 2 CIMs")
BBRS77518 = motor(13050, 0.72, 97.00, 2.70, 245.99, "BB RS 77518")
BBRS550 = motor(19000, 0.38, 84.00, 0.40, 189.02, "BB RS 550")
NEO = motor(5676, 3.36, 166, 1.3, 499.29, "Neo")
FALCON500 = motor(6380, 4.69, 257, 1.5, 783.36, "Falcon 500")
NEO550 = motor(11000, 0.97, 100, 1.3, 279.34, "Neo 550")

ALL_MOTORS = [CIM, MINI_CIM, BAG, PRO775, AM775, AM9015, CIMAND1MINICIM, CIMAND2MINICIM, MINICIMAND2CIM, BBRS77518, BBRS550, NEO, FALCON500, NEO550]