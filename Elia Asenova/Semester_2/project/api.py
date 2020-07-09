import requests
import json
import numpy as np
from flask import Flask
from flask import jsonify
from flask import request
from pymongo import MongoClient
from bson.json_util import dumps
from svm import Model

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.breast_cancer
validDataTypes = ["Copy Number Variation", "Masked Copy Number Variation", "clinical", "miRNA Expression"]
mandatoryFields = {"Copy Number Variation": "Case ID,Chromosome,Start,End,Num_Probes",
                    "Masked Copy Number Variation": "Case ID,Chromosome,Start,End,Num_Probes",
                    "clinical": "submitter_id,tumor_stage,age_at_diagnosis,vital_status",
                    "miRNA Expression": "Case ID,miRNA_ID,read_count"}
model = Model()

@app.route('/v1/patient/datatype/<datatype>', methods=['POST'])
def create_patient_record(datatype):
    if is_data_type_invalid(datatype):
        message = {"message": "Data type is invalid. Valid data types are: " + ', '.join(validDataTypes)}
        return json.dumps(message)

    requestData = request.json
    if requestData is None:
        message = {"message": "Request is invalid. Body is empty"}
        return json.dumps(message)

    mandatoryFieldsByDataType = mandatoryFields[datatype].split(',')
    for field in mandatoryFieldsByDataType:
        if field not in requestData:
            message = {"message": "Mandatory field " + field + " not in request data. Mandatory fields are " + str(mandatoryFieldsByDataType)}
            return json.dumps(message)

    db[datatype].insert_one(requestData)
    message = {"message": "Patient record successfully created"}
    return json.dumps(message)

@app.route('/v1/patient/datatype/<datatype>/caseId/<caseId>', methods=['GET'])
def read_patient_record_by_caseid(datatype, caseId):
    if is_data_type_invalid(datatype):
        message = {"message": "Data type is invalid. Valid data types are: " + ', '.join(validDataTypes)}
        return json.dumps(message)
    
    data = read_data_from_db(datatype, caseId)
    if data == "[]":
        message = {"message": "Case ID does not exist"}
        return json.dumps(message)
    
    return data

@app.route('/v1/patient/datatype/<datatype>/caseId/<caseId>', methods=['PUT'])
def update_patient_record_by_caseid(datatype, caseId):
    if is_data_type_invalid(datatype):
        message = {"message": "Data type is invalid. Valid data types are: " + ', '.join(validDataTypes)}
        return json.dumps(message)

    requestData = request.json
    if requestData is None:
        message = {"message": "Request is invalid. Body is empty"}
        return json.dumps(message)

    if datatype == "clinical":
        db[datatype].update_one({"submitter_id" : caseId}, { "$set": requestData })
    else:
        db[datatype].update_one({"Case ID" : caseId}, { "$set": requestData })
    message = {"message": "Patient record successfully updated"}
    return json.dumps(message)

@app.route('/v1/patient/datatype/<datatype>/caseId/<caseId>', methods=['DELETE'])
def delete_patient_records_by_caseid(datatype, caseId):
    if is_data_type_invalid(datatype):
        message = {"message": "Data type is invalid. Valid data types are: " + ', '.join(validDataTypes)}
        return json.dumps(message)

    if datatype == "clinical":
        result = db[datatype].delete_many({ "submitter_id": caseId })
    else:
        result = db[datatype].delete_many({ "Case ID": caseId })

    message = {"message": str(result.deleted_count) + " documents deleted."}
    return json.dumps(message)

@app.route('/v1/patient/predict/model/<chosenModel>/ageAtDiagnosis/<ageAtDiagnosis>/tumorStage/<tumorStage>', methods=['GET'])
def get_survival_time_prediction(chosenModel, ageAtDiagnosis, tumorStage):
    if chosenModel == "1":
        svm = model.createModel1()
    elif chosenModel == "2":
        svm = model.createModel2()
    else:
        message = {"message": "The chosen model does not exist. Possible choices: 1 or 2"}
        return json.dumps(message)

    if int(tumorStage) not in range(0, 11):
        message = {"message": "The given tumor stage does not exist. Possible choices are from 0 to 10"}
        return json.dumps(message)

    ageAtDiagnosisInDays = float(ageAtDiagnosis) * 365.242199
    data = np.array([[ageAtDiagnosisInDays, tumorStage]])
    data = model.normalize_data(data)
    prediction = svm.predict(data)

    message = {"message": "Survival time prediction: " + str(prediction) + ". Root-mean-square deviation: " + str(model.rmse)}
    return json.dumps(message)

def is_data_type_invalid(dataType):
    validDataTypes = ["Copy Number Variation", "Masked Copy Number Variation", "clinical", "miRNA Expression"]
    if dataType not in validDataTypes:
        return True

    return False

def read_data_from_db(collection, caseId):
    if collection == "clinical":
        listData = list(db[collection].find({"submitter_id" : caseId}))
    else:
        listData = list(db[collection].find({"Case ID" : caseId}))

    json_str = dumps(listData)

    return json_str

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)