from itertools import count
from flask import Blueprint, render_template, request, flash, jsonify
from sqlalchemy.sql.expression import true
from .models import Order, Confirmed
from . import db
import json
from flask import Blueprint, render_template, request, flash, redirect, url_for
from random import randint
import smtplib
from email.mime.text import MIMEText


views = Blueprint('views', __name__)


my_vote = {
    'hoodie': '',
    'sweater': '',
    'totebag': '',
    'colour': ''
}



@views.route('/', methods=['GET', 'POST'])
def webstore():

    if request.method == 'POST':

        session = request.get_json(force=True)

        """session = {
                    "email": "[redacted]",
                    "orders": [
                        {
                            "firstname": "John",
                            "lastname": "Doe",
                            "year": "S4",
                            "cart": {
                                "hoodie": [{"size": "M", "colour": "white"}, {"size": "S", "colour": "black"}],
                                "sweater": [{"size": "L", "colour": "white"}],
                                "totebag": 2
                            }
                        },
                        {
                            "firstname": "[redacted]",
                            "lastname": "[redacted]",
                            "year": "S7",
                            "cart": {
                                "hoodie": [{"size": "S", "colour": "black"}, {"size": "XL", "colour": "grey"}],
                                "sweater": [{"size": "M", "colour": "red"}],
                                "totebag": 0
                            }
                        }
                    ]
                }"""


        h_price = 25
        s_price = 20
        t_price = 7.5
        total_h_price = 0
        total_s_price = 0
        total_t_price = 0
        total_price = 0
        session_id = ''
        for i in range(7):
            session_id = session_id + str(randint(0, 9))

        
        email = session['email'].lower()
        associated_students = ''
        count = 0
        for i in session['orders']:
            if count == 0:
                associated_students = f'{associated_students}{i["firstname"]}-{i["lastname"]}/{i["year"]}'
            else:
                associated_students = (f'{associated_students},{i["firstname"]}-{i["lastname"]}/{i["year"]}')
            count += 1
        associated_carts = {}
        for i in session['orders']:
            associated_carts[f'{i["firstname"]}-{i["lastname"]}/{i["year"]}_cart'] = i["cart"]
            new_total_h_price = h_price * len(i['cart']['hoodie'])
            total_h_price += new_total_h_price
            
            new_total_s_price = s_price * len(i['cart']['sweater'])
            total_s_price += new_total_s_price

            new_total_t_price = t_price * i['cart']['totebag']
            total_t_price += new_total_t_price
        

        h_amm = total_h_price / h_price
        s_amm = total_s_price / s_price
        t_amm = total_t_price / t_price
        d_count = 0

        while h_amm != 0 and s_amm != 0 and t_amm != 0:
            d_count += 1
            h_amm -= 1
            s_amm -= 1
            t_amm -= 1
        
        discount = 2.5 * d_count
        total_price = total_h_price + total_s_price + total_t_price - discount
        

        new_order = Order(email=email, associated_students=associated_students, 
                           associated_carts=associated_carts , session_id=session_id)
        db.session.add(new_order)
        db.session.commit()



        load_data = db.Table('Order', db.metadata, autoload=True, autoload_with=db.engine)
        data = db.session.query(load_data).all()
        

        content = """
        <!DOCTYPE html>
        <html>
            <body>
                <br>
                <p>(Version française ci-dessous.)</p>
                <h1 style="color: #70AD47">Thank you for ordering from the Pupils' Committee!</h1>
                <p>Here's your order number:</p>
                <p style="font-size: 32px; font-weight: bold">%s</p>
                <p>Please take note of this number, as <u>you will need it when picking up your items</u>.</p>
                <hr>
                <p style="color: #C00000">Note that your order will not be processed before the payment has been made.</p>
                <p>For your order, please pay the amount of: <span style="font-weight: bold">%s €</span></p>
                <p>Payments are only accepted via a bank transfer to the following account:</p>
                <p>IBAN: LU64 0019 2555 5628 0000</p>
                <p>Account holder: APEEEL1</p>
                <p>In the bank transfer comments, <u>please write</u>:</p>
                <ul>
                    <li>Your order number</li>
                    <li>The name that was used to place the order</li>
                </ul>
                <hr>
                <p>Items will be available to be picked up in school as soon as possible in January/February 2022, however, delays may occur.</p>
                <p>If you have any questions, don't hesitate to send us a message to: <a href="mailto:merchorders@pupilscom-esl1.eu">merchorders@pupilscom-esl1.eu</a></p>
                <br><br><br><br><br>
                <h1 style="color: #70AD47">Merci pour votre commande auprès du Comité des Élèves !</h1>
                <p>Voici votre numéro de commande :</p>
                <p style="font-size: 32px; font-weight: bold">%s</p>
                <p>Assurez-vous de ne pas perdre ce numéro, car <u>vous en aurez besoin lors du retrait de vos articles</u>.</p>
                <p>Vous devriez avoir reçu un e-mail de confirmation de notre part. Si vous ne le trouvez pas, vérifier votre dossier spam.</p>
                <hr>
                <p style="color: #C00000">Votre commande ne sera pas traitée avant que le paiement n'ait été effectué.</p>
                <p>Pour votre commande, merci de transférer le montant de : <span style="font-weight: bold">%s €</span></p>
                <p>Les paiements sont acceptés uniquement par virement bancaire sur le compte suivant :</p>
                <p>IBAN : LU64 0019 2555 5628 0000</p>
                <p>Titulaire : APEEEL1</p>
                <p>Dans les commentaires du virement bancaire, <u>veuillez indiquer</u> :</p>
                <ul>
                    <li>Votre numéro de commande</li>
                    <li>Le nom avec lequel la commande a été passée</li>
                </ul>
                <hr>
                <p>Les articles seront disponibles pour être récupérés à l'école dès que possible en janvier/février 2022, cependant, des retards peuvent survenir.</p>
                <p>Si vous avez des questions, n'hésitez pas à nous envoyer un message à : <a href="mailto:merchorders@pupilscom-esl1.eu">merchorders@pupilscom-esl1.eu</a></p>
            </body>
        </html>
        """ % (session_id, total_price, session_id, total_price)

        def send(FROM,TO,SUBJECT,TEXT,SERVICE,PORT,USERNAME,PASSWORD):
            server = smtplib.SMTP(SERVICE, PORT)
            server.ehlo()
            server.starttls()
            server.login(USERNAME, PASSWORD)

            msg = MIMEText(TEXT, "html")
            msg["Subject"] = SUBJECT
            msg["From"] = FROM
            msg["To"] = TO

            server.sendmail(FROM,TO,msg.as_string())
            server.quit()

        send("\"Pupils' Committee\" <merchandiseorders@pupilscom-esl1.eu>",email,"Order confirmation & payment instructions",content,"smtp.zoho.eu",587,"merchandiseorders@pupilscom-esl1.eu","oEiQq&w#Y&1n")
        be_response = {'order_id': session_id, 'price': total_price}

        return jsonify(be_response)



    return render_template("index.html")

@views.route('/fr', methods=['GET'])
def webstoreFR():
    return render_template("index-fr.html")




@views.route('/delivery3279', methods=['GET', 'POST'])
def admin():

    load_data = db.Table('Order', db.metadata, autoload=True, autoload_with=db.engine)
    data = db.session.query(load_data).all()
    
    if request.method == 'POST':

        try:
            session_id = request.form.get('session-id')
            first_name = request.form.get('first-name')
            last_name = request.form.get('last-name')
            year = request.form.get('year1')
            collecting_status = request.form.get('status')

            print(collecting_status)


            s1 = ''
            s2 = ''
            s3 = ''
            s4 = ''
            s5 = ''
            s6 = ''
            s7 = ''
            ts = ''

            if year == 'S1':
                s1 = "selected"
            elif year == 'S2':
                s2 = "selected"
            elif year == 'S3':
                s3 = "selected"
            elif year == 'S4':
                s4 = "selected"
            elif year == 'S5':
                s5 = "selected"
            elif year == 'S6':
                s6 = "selected"
            elif year == 'S7':
                s7 = "selected"
            elif year == 'Teacher or Staff':
                ts = "selected"
            
            associated_students1 = f'{first_name}-{last_name}/{year}'



            if len(session_id) == 7:
                session_info = Order.query.filter_by(session_id=session_id).first()
            else:
                load_data = db.Table('Order', db.metadata, autoload=True, autoload_with=db.engine)
                data = db.session.query(load_data).all()
                for p in data:
                    param1 = p.associated_students.replace(' ', '').lower()
                    param2 = associated_students1.replace(' ', '').lower()
                    if param1 == param2:
                        session_info = Order.query.filter_by(associated_students=p.associated_students).first()
                        print(session_info.session_id)
                        break
            
            print(session_info.session_id)
            if collecting_status == '0':
                session_info.phone = 'UNCOMPLETED'
                db.session.commit()
            elif collecting_status == '1':
                session_info.phone = 'COMPLETED'
                db.session.commit()

            status = session_info.phone.lower()
            print(status)

            # Previous collecting system
            '''if status1 == 'on':
                curremail = session_info.email
                if len(curremail.split('@@@')) == 1:
                    session_info.email = curremail + '@@@completed'
                    db.session.commit()
                    
            if status2 == 'on':
                curremail = session_info.email
                if len(curremail.split('@@@')) > 1:
                    session_info.email = curremail.replace('@@@completed', '')
                    db.session.commit()
            
            if len(email.split('@@@')) > 1:
                email = "THIS ORDER IS ALREADY COMPLETED"'''

            email = session_info.email
            associated_students = session_info.associated_students
            carts = session_info.associated_carts


            separated_students = associated_students.split(',')
            first_names = []
            last_names = []
            years = []
            hoodies = []
            sweaters = []
            totebags = []
            orders = []
            seaprator = ''
            order_lenght=len(separated_students)
            
            main_count = 0
            for i in range(len(separated_students)):
                if main_count != 0:
                    seaprator = ':'
                first_names.append(separated_students[i].split('-')[0])
                last_names.append(separated_students[i].split('-')[1].split('/')[0])
                years.append(separated_students[i].split('-')[1].split('/')[1])

                pre_hoodies = []
                for h in carts[f'{first_names[i]}-{last_names[i]}/{years[i]}_cart']['hoodie']:
                    pre_hoodies.append(f'{h["size"]},{h["colour"]}')
                hoodies.append(pre_hoodies)
                
                pre_sweaters = []
                for s in carts[f'{first_names[i]}-{last_names[i]}/{years[i]}_cart']['sweater']:
                    pre_sweaters.append(f'{s["size"]},{s["colour"]}')
                sweaters.append(pre_sweaters)

                totebags.append(carts[f'{first_names[i]}-{last_names[i]}/{years[i]}_cart']['totebag'])
                main_count += 1

                also_owns = ''
                be_careful = {
                    '7078916':'9999999',
                    '7078856':'9999998',
                    '7078906':'9999997',
                    '7078759':'9999996+9999995',
                    '7078747':'9999994',
                    '7078716':'9999993',
                    '7078700':'9999992',
                    '7078709':'9999991',
                    '7078668':'9999990',
                    '7078652':'9999989',
                    '7078812':'9999988',
                    '7078635':'9999987+9999986+9999985',
                    '7078619':'9999984+9999983',
                    '7078811':'9999982',
                    '7078556':'9999981+9999980',
                    '7078593':'9999979+9999978',
                    '7078568':'9999977',
                    '7078558':'9999976',
                    '7078597':'9999975',
                    '7078526':'9999974',
                    '7078518':'9999973+9999972',
                    '7078603':'9999971',
                    '7078865':'9999970'
                }
                be_careful_list = ['7078916', '7078856', '7078906', '7078759', '7078747', '7078716', '7078700', '7078709', '7078668', '7078652', '7078812', '7078635', '7078619', '7078811', '7078556', '7078593', '7078568', '7078558', '7078597', '7078526', '7078518', '7078603', '7078865']
                if session_info.session_id in be_careful_list:
                    also_owns = f'ALSO OWNS: {be_careful[session_info.session_id]}'
            


            return render_template("delivery3279.html", order_lenght=order_lenght, email=email,
                                first_names=first_names, last_names=last_names, years=years, hoodies=hoodies,
                                sweaters=sweaters, totebags=totebags, previous_id=session_id, 
                                previous_first_name=first_name, previous_last_name=last_name, previous_year=year,
                                s1=s1,s2=s2,s3=s3,s4=s4,s5=s5,s6=s6,s7=s7,ts=ts, status=status, also_owns=also_owns)
            
        except:
            return render_template("delivery3279.html", order_lenght=0, email='', first_names=[],
                                last_names=[], years=[], hoodies=[], sweaters=[], totebags=0)


    
    return render_template("delivery3279.html", order_lenght=0, email='', first_names=[],
                                last_names=[], years=[], hoodies=[], sweaters=[], totebags=0, status='uncompleted')






@views.route('/statistics1231', methods=['GET'])
def statistics():

    # Add list of .JSONs extracted from the physical orders table
    '''  
    physical_orders = []
    for i in physical_orders:
        session_id = i['session_id']
        email = 'PHYSICAL ORDER, NO EMAIL WAS GIVEN'
        print(i)
        associated_students = f'{i["orders"][0]["firstname"]}-{i["orders"][0]["lastname"]}/{i["orders"][0]["year"]}'
        associated_carts = {}
        for x in i['orders']:
            associated_carts[f'{x["firstname"]}-{x["lastname"]}/{x["year"]}_cart'] = x["cart"]
        
        new_order = Order(email=email, associated_students=associated_students, 
                        associated_carts=associated_carts , session_id=session_id)
        db.session.add(new_order)
        db.session.commit()
      '''

    # Delete Orders by session_id
    '''  
    deleters = ['2643056', '9417906', '2791108', '9706484', '7490101', '3502521', '3138850', '8053875', '0527338', '7492123', '6770920', '5848092']
    for i in deleters:
        Order.query.filter(Order.session_id == i).delete()
        db.session.commit()
    '''

    # Reset collecting data
    '''
    load_data = db.Table('Order', db.metadata, autoload=True, autoload_with=db.engine)
    data = db.session.query(load_data).all()
    for p in data:
        x = p.session_id
        change = Order.query.filter_by(session_id=x).first()
        change.phone = 'UNCOMPLETED'
        db.session.commit()
    '''

    load_data = db.Table('Order', db.metadata, autoload=True, autoload_with=db.engine)
    data = db.session.query(load_data).all()
    num_of_orders = 0
    colected_h = {}
    colected_s = {}
    colected_t = 0


    for p in data:
        num_of_orders += 1

    for p in data:
        for i in p.associated_students.split(','):
            for x in p.associated_carts[f'{i}_cart']['hoodie']:
                new_hoodie = f"{x['colour']}:{x['size']}"
                if new_hoodie in colected_h:
                    colected_h[new_hoodie] += 1
                else:
                    colected_h[new_hoodie] = 1
    for p in data:
        for i in p.associated_students.split(','):
            for x in p.associated_carts[f'{i}_cart']['sweater']:
                new_sweater = f"{x['colour']}:{x['size']}"
                if new_sweater in colected_s:
                    colected_s[new_sweater] += 1
                else:
                    colected_s[new_sweater] = 1

    for p in data:
        for i in p.associated_students.split(','):
            new_totebag = p.associated_carts[f'{i}_cart']['totebag']
            colected_t += new_totebag
    



    
    return render_template("statistics1231.html", num_of_orders=num_of_orders, colected_h=colected_h, colected_s=colected_s, colected_t=colected_t)