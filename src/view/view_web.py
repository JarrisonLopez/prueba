import Flask 

from flask import Flask, Blueprint, render_template, request

blueprint = Blueprint("vista_empleados", __name__, "templates")

import sys
sys.path.append("src")

from model.Payroll_Logic import *
import controller.usercontroller as usercontroller

@blueprint.route("/")
def home():
    return render_template("index.html")

@blueprint.route("/nuevo")
def nuevo():
    return render_template("new-employee.html")

@blueprint.route("/crear-empleado")
def crear_empleado():
    empleado = Employee(
        firstname=request.args["firstname"], 
        surname=request.args["surname"], 
        idnumber=request.args["idnumber"], 
        mail=request.args["mail"]
    )
    usercontroller.insertar(empleado)
    return render_template("empleado.html", empleado=empleado, mensaje="Empleado insertado exitosamente!")

@blueprint.route("/empleado")
def buscar_empleado():
    idnumber = request.args["idnumber"]
    empleado = usercontroller.buscar_por_id(idnumber)
    return render_template("empleado.html", empleado=empleado)

@blueprint.route("/calcular-salario")
def calcular_salario():
    idnumber = request.args["idnumber"]
    empleado = usercontroller.buscar_por_id(idnumber)
    
    if empleado:
        try:
            accruals = Accruals(
                idnumber=idnumber,
                BasicSalary=request.args["BasicSalary"],
                WorkedDays=request.args["WorkedDays"],
                HolidayTimeWorked=request.args["HolidayTimeWorked"],
                ExtraDaylightHoursWorked=request.args["ExtraDaylightHoursWorked"],
                ExtraNightHoursWorked=request.args["ExtraNightHoursWorked"],
                HolidayExtraDaylightHoursWorked=request.args["HolidayExtraDaylightHoursWorked"],
                HolidayExtraNightHoursWorked=request.args["HolidayExtraNightHoursWorked"],
                DaysOfDisability=request.args["DaysOfDisability"],
                LeaveDays=request.args["LeaveDays"]
            )

            deductions = Deductions(
                idnumber=idnumber,
                accruals=accruals,
                HealthInsurancePercentage=request.args["HealthInsurancePercentage"],
                PensionContributionPercentage=request.args["PensionContributionPercentage"],
                PensionSolidarityFundContributionPercentage=request.args["PensionSolidarityFundContributionPercentage"]
            )

            salary_calculator = SalaryCalculator(accruals, deductions)
            net_salary = salary_calculator.calculate_net_salary()

            return render_template("salario.html", empleado=empleado, net_salary=net_salary)
        except NegativeSalary as e:
            return render_template("error.html", mensaje=str(e))
        except IllegalParameters as e:
            return render_template("error.html", mensaje=str(e))
    else:
        return render_template("error.html", mensaje="Empleado no encontrado.")
