from flask import Flask
import numpy as np
from scipy import stats as st
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

def regLinear(file, dlmtr):
    archivo  = np.genfromtxt(file, delimiter=dlmtr)
    '''x1 = [[i+1 for i in range(len(archivo[x]))] for x in range(len(archivo))]
    valores = [st.linregress(x1[x],archivo[x]) for x in range(len(archivo))]
    B1 = [valores[x].slope for x in range(len(valores))]
    B0 = [valores[x].intercept for x in range(len(valores))]
    p_valor = [valores[x].pvalue for x in range(len(valores))]
    pendiente = [[B0[x] + B1[x]*x1[x][i] for i in range(len(x1[x])) ] for x in range(len(archivo))]'''
    mean =  [np.mean(data) for data in archivo]
    sigma = [np.std(data) for data in archivo]
    randoms = [np.random.normal(mean[x], sigma[x], len(archivo[x])) for x in range(len(archivo))]
    return randoms

class DataSets(Resource):
    def get(self):
        passengersTime  = np.genfromtxt('dataSets/Pasajeros.csv', delimiter=',')
        ArriveTime  = np.genfromtxt('dataSets/llegadas.csv', delimiter=',')
        Times = {}
        timess = []
        for x in range(len(passengersTime)):
            AddTimes = []
            for y in range(len(passengersTime[0])):
                AddTimes.append({'passengerTime':passengersTime[x][y], 'ArriveTime':ArriveTime[x][y]})
            timess.append(AddTimes)
        Times['data'] = timess
        return Times

class LinearRegression(Resource):
    def get(self):
        passengersRandoms = regLinear('dataSets/Pasajeros.csv', ',')
        ArriveRandoms = regLinear('dataSets/llegadas.csv', ',')
        Times = {}
        timess = []
        for x in range(len(passengersRandoms)):
            AddTimes = []
            for y in range(len(passengersRandoms[0])):
                AddTimes.append({'passenger':int(passengersRandoms[x][y]), 'Arrive':int(ArriveRandoms[x][y])})
            timess.append(AddTimes)
        Times['data'] = timess
        return Times['data'][0]

api.add_resource(DataSets, '/')
api.add_resource(LinearRegression, '/linear')

if __name__ == '__main__':
    app.run(debug=True)