import math

##################### User Default Variables #####################
R1 = 1000.0 #Resistance of used resistor, never go lower than 300 ohms
Ra = 25.0 #Resistance over Arduino pins
Vin = 5.0 #Voltage which is used for measurement
Vdrop = 0.0
EC = 0.0
EC20 = 0.0
Rc = 0.0

R1 += Ra

PPMConversion = 0.64 #ppm value which differs from country to country

#Value will change depending on chemical solution and chemical we are meauring
temperatureCoef = 0.019 #0.019 is the standard for plant nutrients

K = 2.88 #Constant that is set depending on cable used

def EC_conversion(temperature, ECRaw):
    ECRaw =165 #REMOVE!

    Vdrop = (Vin * ECRaw) / 1024.0
    Rc = (Vdrop * R1) / (Vin - Vdrop)
    Rc -= Ra
    EC = 1000 / (Rc * K)
    EC20 = EC / (1 + temperatureCoef * (temperature - 20))
    ppm = EC20 *(PPMConversion * 1000)

    return EC20

